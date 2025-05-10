import socket
import pickle
import tkinter as tk
from PIL import Image, ImageTk
import threading
import io
import time
from tkinter import font as tkfont
from tkinter import ttk
import json
from datetime import datetime

class ModernParentMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parent Monitoring System")
        self.root.geometry("1280x800")
        
        # Set modern theme and colors - updated to match the image theme
        self.bg_color = "#14142B"  # Dark blue background
        self.accent_color = "#4361EE"  # Brighter blue accent
        self.secondary_accent = "#F72585"  # Pink accent
        self.text_color = "#FFFFFF"  # White text
        self.secondary_color = "#A0A0C0"  # Light purple/gray
        self.highlight_color = "#2E2E5A"  # Slightly lighter blue for highlights
        self.warning_color = "#F72585"  # Pink for warnings
        self.success_color = "#4CC9F0"  # Cyan for success
        
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
        self.connection_indicator.create_oval(2, 2, 13, 13, fill=self.warning_color, tags="indicator")
        
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
        self.screen_frame = tk.Frame(self.view_frame, bg=self.highlight_color, bd=1, relief=tk.SOLID)
        self.screen_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Screen label for the main display
        self.screen_label = tk.Label(self.screen_frame, bg="#111122", text="No screen capture yet", 
                                  fg=self.secondary_color, font=self.normal_font)
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
        
        # Notebook for tabs (Apps, Search History, etc.)
        self.notebook = ttk.Notebook(self.right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Apps tab
        self.apps_tab = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.apps_tab, text="Applications")
        
        # Search History tab
        self.history_tab = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.history_tab, text="Browser History")
        
        # Apps list panel with title
        self.apps_frame = tk.LabelFrame(self.apps_tab, text="Open Applications", 
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
        self.windows_list_frame = tk.Frame(self.apps_frame, bg=self.highlight_color, bd=1, relief=tk.SOLID)
        self.windows_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollable container for window buttons
        self.windows_canvas = tk.Canvas(self.windows_list_frame, bg=self.highlight_color, highlightthickness=0)
        self.windows_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for windows list
        self.windows_scrollbar = ttk.Scrollbar(self.windows_list_frame, orient=tk.VERTICAL,
                                             command=self.windows_canvas.yview)
        self.windows_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.windows_canvas.configure(yscrollcommand=self.windows_scrollbar.set)
        
        # Frame inside canvas for buttons
        self.windows_container = tk.Frame(self.windows_canvas, bg=self.highlight_color)
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
        
        # Setup search history tab
        self.setup_history_tab()
        
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
                                      font=self.normal_font, bg="#7209B7", fg="white",
                                      padx=15, pady=8, relief=tk.FLAT, bd=0,
                                      command=self.request_windows_list)
        self.refresh_button.pack(side=tk.LEFT, padx=10)

        # Get history button
        self.history_button = tk.Button(self.left_controls, text="Get Search History",
                                      font=self.normal_font, bg="#3F37C9", fg="white",
                                      padx=15, pady=8, relief=tk.FLAT, bd=0,
                                      command=self.request_browser_history)
        self.history_button.pack(side=tk.LEFT, padx=10)
        
        # Right side controls
        self.right_controls = tk.Frame(self.control_panel, bg=self.accent_color)
        self.right_controls.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Pause screen button
        self.pause_button = tk.Button(self.right_controls, text="Pause Screen",
                                    font=self.normal_font, bg="#F72585", fg="white",
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
        self.browser_history = []
        
        # Initialize with some sample applications
        self.sample_windows = {
            1: {"title": "Minecraft", "process": "javaw.exe", "id": 1},
            2: {"title": "Google - Google Chrome", "process": "chrome.exe", "id": 2},
            3: {"title": "Discord", "process": "Discord.exe", "id": 3},
            4: {"title": "Notepad", "process": "notepad.exe", "id": 4},
            5: {"title": "File Explorer", "process": "explorer.exe", "id": 5}
        }
        
        # Sample browser history
        self.sample_history = [
            {"time": "14:32:05", "url": "www.minecraft.net/community", "title": "Minecraft Community | Minecraft"},
            {"time": "14:28:12", "url": "www.google.com/search?q=minecraft+diamond+locations", "title": "minecraft diamond locations - Google Search"},
            {"time": "14:25:30", "url": "www.youtube.com/watch?v=dQw4w9WgXcQ", "title": "How to Beat Minecraft Fast - YouTube"},
            {"time": "14:15:22", "url": "www.google.com/search?q=homework+answers", "title": "homework answers - Google Search"},
            {"time": "14:10:15", "url": "www.roblox.com/games", "title": "Games - Roblox"},
            {"time": "13:58:40", "url": "www.discord.com", "title": "Discord | Your Place to Talk and Hang Out"},
            {"time": "13:45:12", "url": "www.google.com/search?q=math+homework+solver", "title": "math homework solver - Google Search"},
            {"time": "13:30:05", "url": "www.google.com", "title": "Google"}
        ]
        
        # Display sample data
        self.root.after(100, self.load_sample_data)
        
    def setup_history_tab(self):
        # History frame setup
        self.history_frame = tk.LabelFrame(self.history_tab, text="Browser History", 
                                         font=self.subtitle_font, bg=self.bg_color, fg=self.text_color,
                                         padx=10, pady=10)
        self.history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Search box for history
        self.history_search_frame = tk.Frame(self.history_frame, bg=self.bg_color)
        self.history_search_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.history_search_var = tk.StringVar()
        self.history_search_entry = ttk.Entry(self.history_search_frame, textvariable=self.history_search_var, 
                                            font=self.normal_font)
        self.history_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.history_search_button = ttk.Button(self.history_search_frame, text="Search", 
                                              style="TButton")
        self.history_search_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # History list with scrollbar
        self.history_list_frame = tk.Frame(self.history_frame, bg=self.highlight_color, bd=1, relief=tk.SOLID)
        self.history_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create tree view for history
        columns = ('time', 'title', 'url')
        self.history_tree = ttk.Treeview(self.history_list_frame, columns=columns, show='headings')
        
        # Define headings
        self.history_tree.heading('time', text='Time')
        self.history_tree.heading('title', text='Page Title')
        self.history_tree.heading('url', text='URL')
        
        # Define columns
        self.history_tree.column('time', width=70)
        self.history_tree.column('title', width=150)
        self.history_tree.column('url', width=200)
        
        # Add scrollbar
        self.history_scrollbar = ttk.Scrollbar(self.history_list_frame, orient=tk.VERTICAL, 
                                             command=self.history_tree.yview)
        self.history_tree.configure(yscroll=self.history_scrollbar.set)
        
        # Pack elements
        self.history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Highlight suspicious searches
        self.highlight_suspicious_patterns = ['game', 'minecraft', 'cheat', 'play', 'youtube', 'roblox', 'discord']
    
    def load_sample_data(self):
        # Load windows list
        self.update_windows_list(self.sample_windows)
        
        # Load search history
        self.update_browser_history(self.sample_history)
        
        # Load sample screen image - create gradient background
        width, height = 800, 500
        sample_bg = self.create_gradient_image(width, height, "#111122", "#222244")
        
        # Add minecraft logo/interface simulation
        # This is a simplified representation, not an actual logo
        photo = ImageTk.PhotoImage(sample_bg)
        self.screen_label.config(image=photo)
        self.screen_label.image = photo  # Keep a reference
        
    def create_gradient_image(self, width, height, color1, color2):
        """Create a gradient image from color1 to color2"""
        base = Image.new('RGB', (width, height), color1)
        
        # Create a gradient overlay
        for y in range(height):
            for x in range(width):
                # Calculate gradient color
                ratio = y / height
                r = int((1 - ratio) * int(color1[1:3], 16) + ratio * int(color2[1:3], 16))
                g = int((1 - ratio) * int(color1[3:5], 16) + ratio * int(color2[3:5], 16))
                b = int((1 - ratio) * int(color1[5:7], 16) + ratio * int(color2[5:7], 16))
                
                base.putpixel((x, y), (r, g, b))
                
        return base
        
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
        self.connection_indicator.itemconfig("indicator", fill=self.warning_color)  # Red for disconnected
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
            self.connection_indicator.itemconfig("indicator", fill=self.success_color)  # Cyan for connected
        elif "error" in status_text:
            self.connection_indicator.itemconfig("indicator", fill=self.warning_color)  # Red for error
    
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
                elif msg_type == b'\x03':  # Browser history
                    self.process_browser_history(data)
                
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
    
    def process_browser_history(self, data):
        try:
            # Deserialize the browser history
            history_data = pickle.loads(data)
            
            # Update the UI from the main thread
            self.root.after(0, lambda: self.update_browser_history(history_data))
                
        except Exception as e:
            if self.server_running:
                self.root.after(0, lambda: self.update_connection_status(f"Error processing browser history: {str(e)}"))
    
    def update_windows_list(self, windows_data):
        # Clear existing windows list
        self.clear_windows_list()
        
        # Create a new window button for each window
        for window_id, window_info in windows_data.items():
            window_title = window_info['title']
            window_process = window_info['process']
            
            # Create a app card frame
            card_frame = tk.Frame(self.windows_container, bg=self.highlight_color, bd=1, relief=tk.SOLID)
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
            info_frame = tk.Frame(card_frame, bg=self.highlight_color)
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)
            
            # App title
            title_label = tk.Label(info_frame, text=window_title, bg=self.highlight_color, 
                                 fg=self.text_color, font=self.normal_font, anchor=tk.W,
                                 justify=tk.LEFT)
            title_label.pack(fill=tk.X, anchor=tk.W)
            
            # App process name
            process_label = tk.Label(info_frame, text=window_process, bg=self.highlight_color,
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
                self.highlight
                self.highlight_active_window(card_frame, True)
    
    def clear_windows_list(self):
        # Clear all widgets from windows container
        for child in self.windows_container.winfo_children():
            child.destroy()
        self.windows_list = []
    
    def get_icon_color(self, process_name):
        # Get a deterministic color based on process name
        process_name = process_name.lower()
        
        # Predefined colors for common applications
        colors = {
            "chrome": "#4285F4",  # Google blue
            "firefox": "#FF9400",  # Firefox orange
            "explorer": "#0078D7",  # Windows blue
            "discord": "#7289DA",  # Discord purple
            "javaw": "#5cb85c",  # Green for Minecraft
            "notepad": "#1e88e5",  # Blue for Notepad
            "msedge": "#0078D7",  # Edge blue
        }
        
        # Check for matches
        for app, color in colors.items():
            if app in process_name:
                return color
        
        # Generate a color based on the first letter
        if process_name:
            hash_value = hash(process_name[0].lower())
            # Generate colors in a nice range (avoid too light or too dark)
            r = (hash_value & 0xFF) % 128 + 64
            g = ((hash_value >> 8) & 0xFF) % 128 + 64
            b = ((hash_value >> 16) & 0xFF) % 128 + 64
            return f"#{r:02x}{g:02x}{b:02x}"
        
        return self.accent_color  # Default fallback
    
    def select_window(self, window_id):
        # Handle window selection
        self.active_window_id = window_id
        
        # Update all window frames to remove highlights from others
        for wid, frame in self.windows_list:
            if wid == window_id:
                self.highlight_active_window(frame, True)
                
                # Request screenshot for the selected window
                self.request_window_screenshot(window_id)
                
                # Update current view label
                for w_id, info in self.sample_windows.items():
                    if w_id == window_id:
                        self.view_label.config(text=f"Current View: {info['title']}")
                        break
            else:
                self.highlight_active_window(frame, False)
    
    def highlight_active_window(self, frame, is_active):
        # Highlight the active window
        if is_active:
            frame.config(bg=self.accent_color)
            for child in frame.winfo_children():
                if isinstance(child, tk.Frame) and not child.winfo_children()[0].cget("text").isalpha():
                    # Skip the icon frame
                    continue
                child.config(bg=self.accent_color)
                
                for grandchild in child.winfo_children():
                    if isinstance(grandchild, tk.Label):
                        grandchild.config(bg=self.accent_color)
        else:
            frame.config(bg=self.highlight_color)
            for child in frame.winfo_children():
                if isinstance(child, tk.Frame) and child.winfo_children() and not child.winfo_children()[0].cget("text").isalpha():
                    # Skip the icon frame
                    continue
                child.config(bg=self.highlight_color)
                
                for grandchild in child.winfo_children():
                    if isinstance(grandchild, tk.Label):
                        grandchild.config(bg=self.highlight_color)
    
    def on_hover_enter(self, frame):
        # Highlight on hover
        if self.active_window_id is None or frame not in [f for _, f in self.windows_list if _ == self.active_window_id]:
            frame.config(bg="#3E3E7E")  # Slightly lighter than highlight color
            for child in frame.winfo_children():
                if isinstance(child, tk.Frame) and child.winfo_children() and not child.winfo_children()[0].cget("text").isalpha():
                    # Skip the icon frame
                    continue
                child.config(bg="#3E3E7E")
                
                for grandchild in child.winfo_children():
                    if isinstance(grandchild, tk.Label):
                        grandchild.config(bg="#3E3E7E")
    
    def on_hover_leave(self, frame, window_id):
        # Remove highlight on mouse leave, but keep for active window
        if window_id != self.active_window_id:
            frame.config(bg=self.highlight_color)
            for child in frame.winfo_children():
                if isinstance(child, tk.Frame) and child.winfo_children() and not child.winfo_children()[0].cget("text").isalpha():
                    # Skip the icon frame
                    continue
                child.config(bg=self.highlight_color)
                
                for grandchild in child.winfo_children():
                    if isinstance(grandchild, tk.Label):
                        grandchild.config(bg=self.highlight_color)
    
    def update_browser_history(self, history_data):
        # Clear current history
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add new history items
        for item in history_data:
            # Check if the entry contains suspicious terms
            is_suspicious = False
            for pattern in self.highlight_suspicious_patterns:
                if pattern.lower() in item['url'].lower() or pattern.lower() in item['title'].lower():
                    is_suspicious = True
                    break
            
            item_id = self.history_tree.insert('', tk.END, values=(item['time'], item['title'], item['url']))
            
            # Highlight suspicious entries
            if is_suspicious:
                self.history_tree.item(item_id, tags=('suspicious',))
        
        # Configure tag appearance
        self.history_tree.tag_configure('suspicious', background=self.warning_color, foreground='white')
    
    def request_windows_list(self):
        if self.client_socket and self.server_running:
            try:
                # Send request for windows list (message type 0x02)
                request = b'\x02' + (0).to_bytes(8, byteorder='big')
                self.client_socket.sendall(request)
            except:
                # If not connected to client, use sample data
                self.update_windows_list(self.sample_windows)
        else:
            # If not connected to client, use sample data
            self.update_windows_list(self.sample_windows)
    
    def request_window_screenshot(self, window_id):
        if self.client_socket and self.server_running:
            try:
                # Send request for specific window screenshot (message type 0x01)
                request = b'\x01' + window_id.to_bytes(8, byteorder='big')
                self.client_socket.sendall(request)
            except Exception as e:
                self.update_connection_status(f"Error requesting screenshot: {str(e)}")
    
    def request_browser_history(self):
        if self.client_socket and self.server_running:
            try:
                # Send request for browser history (message type 0x03)
                request = b'\x03' + (0).to_bytes(8, byteorder='big')
                self.client_socket.sendall(request)
            except:
                # If not connected to client, use sample data
                self.update_browser_history(self.sample_history)
        else:
            # If not connected to client, use sample data
            self.update_browser_history(self.sample_history)
    
    def pause_screen(self):
        self.screen_paused = not self.screen_paused
        if self.screen_paused:
            self.pause_button.config(text="Resume Screen")
        else:
            self.pause_button.config(text="Pause Screen")
            # Request current window again if not paused
            if self.active_window_id is not None:
                self.request_window_screenshot(self.active_window_id)

def main():
    root = tk.Tk()
    app = ModernParentMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()