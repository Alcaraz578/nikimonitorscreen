import socket
import pickle
import tkinter as tk
from PIL import Image, ImageTk
import threading
import io
import time
from tkinter import font as tkfont
from tkinter import ttk

class ModernParentMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parent Monitoring System")
        self.root.geometry("1280x800")
        
        # Set modern theme and colors
        self.bg_color = "#F0F2F5"
        self.accent_color = "#3498DB"
        self.text_color = "#2C3E50"
        self.secondary_color = "#7F8C8D"
        self.highlight_color = "#E3F2FD"
        self.warning_color = "#E74C3C"
        self.success_color = "#2ECC71"
        
        # Custom fonts
        self.title_font = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self.subtitle_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")
        self.normal_font = tkfont.Font(family="Segoe UI", size=10)
        self.small_font = tkfont.Font(family="Segoe UI", size=9)
        
        # Configure styles for ttk widgets
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure ttk button styles
        style.configure("TButton", font=self.normal_font, background=self.accent_color)
        style.configure("Accent.TButton", background=self.accent_color)
        style.configure("Success.TButton", background=self.success_color)
        style.configure("Warning.TButton", background=self.warning_color)
        
        # Main container with padding
        self.main_frame = tk.Frame(root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top header bar
        self.header_frame = tk.Frame(self.main_frame, bg=self.accent_color, height=60)
        self.header_frame.pack(fill=tk.X)
        self.header_frame.pack_propagate(False)
        
        # App title in header
        tk.Label(self.header_frame, text="Parent Monitoring System", 
                font=("Segoe UI", 18, "bold"), bg=self.accent_color, fg="white").pack(side=tk.LEFT, padx=20, pady=10)
        
        # Status indicator in header
        self.status_frame = tk.Frame(self.header_frame, bg=self.accent_color)
        self.status_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        self.connection_indicator = tk.Canvas(self.status_frame, width=15, height=15, 
                                            bg=self.accent_color, highlightthickness=0)
        self.connection_indicator.pack(side=tk.LEFT, padx=(0, 10))
        self.connection_indicator.create_oval(2, 2, 13, 13, fill="#E74C3C", tags="indicator")
        
        self.status_var = tk.StringVar()
        self.status_var.set("Disconnected")
        self.status_label = tk.Label(self.status_frame, textvariable=self.status_var, 
                                   font=self.normal_font, bg=self.accent_color, fg="white")
        self.status_label.pack(side=tk.LEFT)
        
        # Create main content frame with padding
        self.content_frame = tk.Frame(self.main_frame, bg=self.bg_color, padx=20, pady=20)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for screen display (uses 70% of width)
        self.left_panel = tk.Frame(self.content_frame, bg=self.bg_color)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Screen view panel with title
        self.view_frame = tk.LabelFrame(self.left_panel, text="Screen View", 
                                      font=self.subtitle_font, bg=self.bg_color, fg=self.text_color,
                                      padx=10, pady=10)
        self.view_frame.pack(fill=tk.BOTH, expand=True)
        
        # Screen display with border
        self.screen_frame = tk.Frame(self.view_frame, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        self.screen_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Screen label for the main display
        self.screen_label = tk.Label(self.screen_frame, bg="#333333", text="No screen capture yet", 
                                  fg="#FFFFFF", font=self.normal_font)
        self.screen_label.pack(fill=tk.BOTH, expand=True)
        
        # Current window info
        self.window_info_frame = tk.Frame(self.left_panel, bg=self.bg_color, height=40)
        self.window_info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.view_label = tk.Label(self.window_info_frame, text="Current View: None", 
                                 font=self.normal_font, bg=self.bg_color, fg=self.text_color)
        self.view_label.pack(side=tk.LEFT)
        
        # Right panel for windows/apps list (uses 30% of width)
        self.right_panel = tk.Frame(self.content_frame, bg=self.bg_color, width=350)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(20, 0))
        
        # Apps list panel with title
        self.apps_frame = tk.LabelFrame(self.right_panel, text="Open Applications", 
                                      font=self.subtitle_font, bg=self.bg_color, fg=self.text_color,
                                      padx=10, pady=10)
        self.apps_frame.pack(fill=tk.BOTH, expand=True)
        
        # Search box for filtering apps
        self.search_frame = tk.Frame(self.apps_frame, bg=self.bg_color)
        self.search_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, 
                                    font=self.normal_font)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.search_button = ttk.Button(self.search_frame, text="Search", style="TButton")
        self.search_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Windows list with scrollbar
        self.windows_list_frame = tk.Frame(self.apps_frame, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        self.windows_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollable container for window buttons
        self.windows_canvas = tk.Canvas(self.windows_list_frame, bg="#FFFFFF", highlightthickness=0)
        self.windows_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for windows list
        self.windows_scrollbar = ttk.Scrollbar(self.windows_list_frame, orient=tk.VERTICAL,
                                             command=self.windows_canvas.yview)
        self.windows_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.windows_canvas.configure(yscrollcommand=self.windows_scrollbar.set)
        
        # Frame inside canvas for buttons
        self.windows_container = tk.Frame(self.windows_canvas, bg="#FFFFFF")
        self.windows_canvas_window = self.windows_canvas.create_window((0, 0), 
                                                                     window=self.windows_container,
                                                                     anchor=tk.NW)
        
        # Configure canvas resize
        self.windows_container.bind("<Configure>", 
                                  lambda e: self.windows_canvas.configure(
                                      scrollregion=self.windows_canvas.bbox("all")))
        self.windows_canvas.bind("<Configure>", 
                               lambda e: self.windows_canvas.itemconfig(
                                   self.windows_canvas_window, width=e.width))
        
        # Bottom control panel
        self.control_panel = tk.Frame(self.main_frame, bg=self.accent_color, height=70)
        self.control_panel.pack(side=tk.BOTTOM, fill=tk.X)
        self.control_panel.pack_propagate(False)
        
        # Left side controls
        self.left_controls = tk.Frame(self.control_panel, bg=self.accent_color)
        self.left_controls.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Start monitoring button
        self.connect_button = tk.Button(self.left_controls, text="Start Monitoring", 
                                      font=self.normal_font, bg=self.success_color, fg="white",
                                      padx=15, pady=8, relief=tk.FLAT, bd=0,
                                      command=self.start_server)
        self.connect_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Stop monitoring button
        self.disconnect_button = tk.Button(self.left_controls, text="Stop Monitoring",
                                         font=self.normal_font, bg=self.warning_color, fg="white",
                                         padx=15, pady=8, relief=tk.FLAT, bd=0,
                                         command=self.stop_server,
                                         state=tk.DISABLED)
        self.disconnect_button.pack(side=tk.LEFT, padx=10)
        
        # Refresh apps list button
        self.refresh_button = tk.Button(self.left_controls, text="Refresh Apps List",
                                      font=self.normal_font, bg="#9B59B6", fg="white",
                                      padx=15, pady=8, relief=tk.FLAT, bd=0,
                                      command=self.request_windows_list)
        self.refresh_button.pack(side=tk.LEFT, padx=10)
        
        # Right side controls
        self.right_controls = tk.Frame(self.control_panel, bg=self.accent_color)
        self.right_controls.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Pause screen button
        self.pause_button = tk.Button(self.right_controls, text="Pause Screen",
                                    font=self.normal_font, bg="#FF9800", fg="white",
                                    padx=15, pady=8, relief=tk.FLAT, bd=0,
                                    command=self.pause_screen)
        self.pause_button.pack(side=tk.RIGHT)
        
        # Server settings
        self.server_ip = "0.0.0.0"  # Listen on all interfaces
        self.server_port = 5555
        
        # Server status
        self.server_running = False
        self.client_socket = None
        self.server_socket = None
        self.screen_paused = False
        self.windows_list = []
        self.active_window_id = None
        
        # Initialize with some sample applications
        self.sample_windows = {
            1: {"title": "Minecraft", "process": "javaw.exe", "id": 1},
            2: {"title": "Google - Google Chrome", "process": "chrome.exe", "id": 2},
            3: {"title": "Discord", "process": "Discord.exe", "id": 3},
            4: {"title": "Notepad", "process": "notepad.exe", "id": 4},
            5: {"title": "File Explorer", "process": "explorer.exe", "id": 5}
        }
        
        # Display sample data
        self.root.after(100, self.load_sample_data)
        
    def load_sample_data(self):
        # Just for demo purposes
        self.update_windows_list(self.sample_windows)
        
        # Load sample screen image
        sample_bg = Image.new('RGB', (800, 500), color='#333333')
        photo = ImageTk.PhotoImage(sample_bg)
        self.screen_label.config(image=photo)
        self.screen_label.image = photo
        
    def start_server(self):
        if not self.server_running:
            self.server_thread = threading.Thread(target=self.run_server)
            self.server_thread.daemon = True
            self.server_running = True
            self.server_thread.start()
            
            # Update UI
            self.status_var.set("Listening for connection...")
            self.connection_indicator.itemconfig("indicator", fill="#F39C12")  # Yellow for listening
            self.connect_button.config(state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL)
    
    def stop_server(self):
        self.server_running = False
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()
            
        # Update UI
        self.status_var.set("Disconnected")
        self.connection_indicator.itemconfig("indicator", fill="#E74C3C")  # Red for disconnected
        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)
        
    def run_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.server_ip, self.server_port))
            self.server_socket.listen(1)
            self.server_socket.settimeout(1.0)  # Add timeout for accept
            
            while self.server_running:
                try:
                    self.client_socket, addr = self.server_socket.accept()
                    
                    # Update UI from main thread
                    self.root.after(0, lambda: self.update_connection_status(f"Connected to {addr[0]}"))
                    
                    # Start receiving data
                    self.receive_thread = threading.Thread(target=self.receive_data)
                    self.receive_thread.daemon = True
                    self.receive_thread.start()
                    
                    # Request windows list immediately
                    self.root.after(1000, self.request_windows_list)
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.server_running:
                        self.root.after(0, lambda: self.update_connection_status(f"Connection error: {str(e)}"))
                    break
                    
        except Exception as e:
            self.root.after(0, lambda: self.update_connection_status(f"Server error: {str(e)}"))
        finally:
            if self.server_socket:
                self.server_socket.close()
            self.server_running = False
            self.root.after(0, lambda: self.connect_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.disconnect_button.config(state=tk.DISABLED))
    
    def update_connection_status(self, status_text):
        self.status_var.set(status_text)
        if "Connected" in status_text:
            self.connection_indicator.itemconfig("indicator", fill="#2ECC71")  # Green for connected
        elif "error" in status_text:
            self.connection_indicator.itemconfig("indicator", fill="#E74C3C")  # Red for error
    
    def receive_data(self):
        while self.server_running and self.client_socket:
            try:
                # Read message type (1 byte)
                msg_type = self.client_socket.recv(1)
                if not msg_type:
                    break
                
                # Read data size (8 bytes)
                data_size_bytes = self.client_socket.recv(8)
                if not data_size_bytes:
                    break
                
                data_size = int.from_bytes(data_size_bytes, byteorder='big')
                
                # Read the actual data
                data = b""
                while len(data) < data_size:
                    chunk = self.client_socket.recv(min(4096, data_size - len(data)))
                    if not chunk:
                        break
                    data += chunk
                
                # Process the data based on message type
                if msg_type == b'\x01':  # Screen capture
                    self.process_screen_capture(data)
                elif msg_type == b'\x02':  # Windows list
                    self.process_windows_list(data)
                
            except Exception as e:
                if self.server_running:
                    self.root.after(0, lambda: self.update_connection_status(f"Error receiving data: {str(e)}"))
                break
        
        # Connection closed
        self.root.after(0, lambda: self.update_connection_status("Disconnected"))
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
    
    def process_screen_capture(self, data):
        try:
            # Convert the data to an image and display it
            image = Image.open(io.BytesIO(data))
            
            # Resize image to fit the label if needed
            label_width = self.screen_label.winfo_width()
            label_height = self.screen_label.winfo_height()
            
            if label_width > 1 and label_height > 1:
                image = image.resize((label_width, label_height), Image.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            
            # Update the UI from the main thread
            self.root.after(0, lambda: self.update_screen_display(photo))
                
        except Exception as e:
            if self.server_running:
                self.root.after(0, lambda: self.update_connection_status(f"Error processing screen: {str(e)}"))
    
    def update_screen_display(self, photo):
        self.screen_label.config(image=photo)
        self.screen_label.image = photo  # Keep a reference
    
    def process_windows_list(self, data):
        try:
            # Deserialize the windows list
            windows_data = pickle.loads(data)
            
            # Update the UI from the main thread
            self.root.after(0, lambda: self.update_windows_list(windows_data))
                
        except Exception as e:
            if self.server_running:
                self.root.after(0, lambda: self.update_connection_status(f"Error processing apps list: {str(e)}"))
    
    def update_windows_list(self, windows_data):
        # Clear existing windows list
        self.clear_windows_list()
        
        # Create a new window button for each window
        for window_id, window_info in windows_data.items():
            window_title = window_info['title']
            window_process = window_info['process']
            
            # Create a app card frame
            card_frame = tk.Frame(self.windows_container, bg="white", bd=1, relief=tk.SOLID)
            card_frame.pack(fill=tk.X, padx=5, pady=5, ipady=5)
            
            # Create app icon frame
            icon_color = self.get_icon_color(window_process)
            icon_frame = tk.Frame(card_frame, bg=icon_color, width=40, height=40)
            icon_frame.pack(side=tk.LEFT, padx=10, pady=10)
            icon_frame.pack_propagate(False)
            
            # App icon text (first letter of process)
            icon_text = window_process[0].upper() if window_process else "?"
            icon_label = tk.Label(icon_frame, text=icon_text, 
                                font=("Segoe UI", 16, "bold"), bg=icon_color, fg="white")
            icon_label.pack(fill=tk.BOTH, expand=True)
            
            # App info frame
            info_frame = tk.Frame(card_frame, bg="white")
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)
            
            # App title
            title_label = tk.Label(info_frame, text=window_title, bg="white", 
                                 fg=self.text_color, font=self.normal_font, anchor=tk.W,
                                 justify=tk.LEFT)
            title_label.pack(fill=tk.X, anchor=tk.W)
            
            # App process name
            process_label = tk.Label(info_frame, text=window_process, bg="white",
                                   fg=self.secondary_color, font=self.small_font, anchor=tk.W,
                                   justify=tk.LEFT)
            process_label.pack(fill=tk.X, anchor=tk.W)
            
            # Store window information
            self.windows_list.append((window_id, card_frame))
            
            # Make the entire card clickable
            card_frame.bind("<Button-1>", lambda e, wid=window_id: self.select_window(wid))
            card_frame.bind("<Enter>", lambda e, frame=card_frame: self.on_hover_enter(frame))
            card_frame.bind("<Leave>", lambda e, frame=card_frame, wid=window_id: self.on_hover_leave(frame, wid))
            
            # Make all child widgets clickable too
            for child in card_frame.winfo_children():
                child.bind("<Button-1>", lambda e, wid=window_id: self.select_window(wid))
                child.bind("<Enter>", lambda e, frame=card_frame: self.on_hover_enter(frame))
                child.bind("<Leave>", lambda e, frame=card_frame, wid=window_id: self.on_hover_leave(frame, wid))
                
                if isinstance(child, tk.Frame):
                    for grandchild in child.winfo_children():
                        grandchild.bind("<Button-1>", lambda e, wid=window_id: self.select_window(wid))
                        grandchild.bind("<Enter>", lambda e, frame=card_frame: self.on_hover_enter(frame))
                        grandchild.bind("<Leave>", lambda e, frame=card_frame, wid=window_id: self.on_hover_leave(frame, wid))
            
            # Highlight active window if any
            if self.active_window_id == window_id:
                card_frame.config(bg=self.highlight_color)
                info_frame.config(bg=self.highlight_color)
                title_label.config(bg=self.highlight_color)
                process_label.config(bg=self.highlight_color)
            
            # Special highlight for Minecraft
            if "minecraft" in window_title.lower() or "minecraft" in window_process.lower():
                card_frame.config(bd=2, relief=tk.RAISED)
                title_label.config(fg="#E74C3C", font=("Segoe UI", 10, "bold"))
    
    def get_icon_color(self, process_name):
        # Generate a color based on the process name
        colors = {
            'chrome': "#4285F4",
            'firefox': "#FF9500",
            'edge': "#0078D7",
            'notepad': "#1ABC9C",
            'word': "#2B579A",
            'excel': "#217346",
            'powerpoint': "#D24726",
            'outlook': "#0078D4",
            'teams': "#6264A7",
            'explorer': "#FFD700",
            'minecraft': "#5BBD2B",
            'javaw': "#5BBD2B",
            'discord': "#7289DA",
            'steam': "#171A21"
        }
        
        for key in colors:
            if key in process_name.lower():
                return colors[key]
        
        # Default colors for other processes
        default_colors = ["#3498DB", "#9B59B6", "#E74C3C", "#16A085", "#27AE60", "#D35400", "#2980B9"]
        
        # Generate a consistent color based on the process name
        index = sum(ord(c) for c in process_name) % len(default_colors)
        return default_colors[index]
    
    def on_hover_enter(self, frame):
        if frame.cget("bg") != self.highlight_color:
            frame.config(bg="#F5F5F5")
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Frame) and not widget.winfo_children()[0].cget("bg") in [self.accent_color, "#5BBD2B", "#4285F4"]:
                    widget.config(bg="#F5F5F5")
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label):
                            child.config(bg="#F5F5F5")

    def on_hover_leave(self, frame, window_id):
        if window_id != self.active_window_id:
            frame.config(bg="white")
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Frame) and not widget.winfo_children()[0].cget("bg") in [self.accent_color, "#5BBD2B", "#4285F4"]:
                    widget.config(bg="white")
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label):
                            child.config(bg="white")
    
    def clear_windows_list(self):
        for widget in self.windows_container.winfo_children():
            widget.destroy()
        self.windows_list = []
    
    def select_window(self, window_id):
        # Update active window ID
        self.active_window_id = window_id
        
        # Update UI to highlight selected window
        for wid, frame in self.windows_list:
            if wid == window_id:
                frame.config(bg=self.highlight_color)
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Frame) and not widget.winfo_children()[0].cget("bg") in [self.accent_color, "#5BBD2B", "#4285F4"]:
                        widget.config(bg=self.highlight_color)
                        for child in widget.winfo_children():
                            if isinstance(child, tk.Label):
                                child.config(bg=self.highlight_color)
            else:
                frame.config(bg="white")
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Frame) and not widget.winfo_children()[0].cget("bg") in [self.accent_color, "#5BBD2B", "#4285F4"]:
                        widget.config(bg="white")
                        for child in widget.winfo_children():
                            if isinstance(child, tk.Label):
                                child.config(bg="white")
        
        # Send command to client to focus on this window (if connected)
        if self.client_socket and self.server_running:
            try:
                command = b'\x01' + window_id.to_bytes(8, byteorder='big')
                self.client_socket.sendall(command)
            except Exception as e:
                self.update_connection_status(f"Error selecting window: {str(e)}")
        
        # Update view label with window title
        for window_id, window_info in self.sample_windows.items():
            if window_id == self.active_window_id:
                self.view_label.config(text=f"Current View: {window_info['title']}")
                break
    
    def request_windows_list(self):
        if self.client_socket and self.server_running:
            try:
                # Send command to request windows list
                command = b'\x02'
                self.client_socket.sendall(command)
                self.update_connection_status("Refreshing applications list...")
            except Exception as e:
                self.update_connection_status(f"Error requesting apps list: {str(e)}")
    
    def pause_screen(self):
        if self.client_socket and self.server_running:
            try:
                # Toggle pause state
                self.screen_paused = not self.screen_paused
                
                # Send pause command to client
                command = b'\x03' + (b'\x01' if self.screen_paused else b'\x00')
                self.client_socket.sendall(command)
                
                # Update button text and color
                if self.screen_paused:
                    self.pause_button.config(text="Resume Screen", bg=self.success_color)
                    self.update_connection_status("Screen paused - Message displayed to student")
                else:
                    self.pause_button.config(text="Pause Screen", bg="#FF9800")
                    self.update_connection_status("Screen resumed")
                    
                # Show a sample of the pause screen
                if self.screen_paused:
                    self.show_pause_sample()
                
            except Exception as e:
                self.update_connection_status(f"Error toggling screen pause: {str(e)}")
        else:
            # For demo purposes, show the pause screen sample
            self.screen_paused = not self.screen_paused
            if self.screen_paused:
                self.pause_button.config(text="Resume Screen", bg=self.success_color)
                self.show_pause_sample()
            else:
                self.pause_button.config(text="Pause Screen", bg="#FF9800")
                # Restore sample screen
                self.load_sample_data()
                
    def show_pause_sample(self):
        # Create a sample pause screen
        width, height = 800, 500  # Adjust to match your actual screen size
        pause_img = Image.new('RGB', (width, height), color='#777777')
        
        # Convert to PhotoImage for display
        photo = ImageTk.PhotoImage(pause_img)
        self.screen_label.config(image=photo)
        self.screen_label.image = photo  # Keep a reference
        
        # Add message overlay
        self.screen_label.config(compound=tk.CENTER, 
                              text="Nice try, but not good enough!",
                              font=("Impact", 36), fg="#FF0000")

def main():
    root = tk.Tk()
    app = ModernParentMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()