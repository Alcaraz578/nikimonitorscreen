import socket
import pickle
import tkinter as tk
from PIL import Image, ImageTk
import threading
import io
import time
from tkinter import font as tkfont
from tkinter import ttk

class ParentMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parent Monitoring App")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f5f5f5")
        
        # Set theme and colors
        self.bg_color = "#f5f5f5"
        self.accent_color = "#1976D2"
        self.text_color = "#212121"
        self.secondary_color = "#757575"
        self.highlight_color = "#BBDEFB"
        self.warning_color = "#F44336"
        
        # Custom fonts
        self.title_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")
        self.normal_font = tkfont.Font(family="Segoe UI", size=10)
        self.small_font = tkfont.Font(family="Segoe UI", size=9)
        
        # Configure styles
        style = ttk.Style()
        style.configure("TButton", font=self.normal_font)
        style.configure("Accent.TButton", background=self.accent_color)
        style.configure("Warning.TButton", background=self.warning_color)
        
        # Create main container with padding
        self.main_frame = tk.Frame(root, bg=self.bg_color, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with title
        self.header_frame = tk.Frame(self.main_frame, bg=self.bg_color, pady=5)
        self.header_frame.pack(fill=tk.X)
        
        tk.Label(self.header_frame, text="Parent Monitoring Dashboard", 
                font=("Segoe UI", 16, "bold"), bg=self.bg_color, fg=self.accent_color).pack(side=tk.LEFT)
        
        # Create main container
        self.main_container = tk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL, 
                                         bg=self.bg_color, sashwidth=4, sashrelief=tk.RAISED)
        self.main_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left panel - Main screen display
        self.left_panel = tk.Frame(self.main_container, bg=self.bg_color)
        self.main_container.add(self.left_panel, weight=3)
        
        # Screen frame with border
        self.screen_frame = tk.Frame(self.left_panel, bg=self.accent_color, bd=2)
        self.screen_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Label showing current view
        self.view_label = tk.Label(self.left_panel, text="Current View: Full Screen", 
                                font=self.title_font, bg=self.bg_color, fg=self.text_color)
        self.view_label.pack(anchor=tk.W, padx=5, pady=(5, 0))
        
        # Screen label for the main display
        self.screen_label = tk.Label(self.screen_frame, bg="#333333")
        self.screen_label.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Window list
        self.right_panel = tk.Frame(self.main_container, bg=self.bg_color, width=250)
        self.main_container.add(self.right_panel, weight=1)
        
        # Windows list header
        tk.Label(self.right_panel, text="Open Applications", font=self.title_font,
               bg=self.bg_color, fg=self.text_color).pack(fill=tk.X, padx=5, pady=(0, 10))
        
        # Windows list frame with border and scrollbar
        self.windows_list_frame = tk.Frame(self.right_panel, bg=self.accent_color, bd=1)
        self.windows_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                
        # Scrollable container for window buttons
        self.windows_canvas = tk.Canvas(self.windows_list_frame, bg="white", highlightthickness=0)
        self.windows_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for windows list
        self.windows_scrollbar = ttk.Scrollbar(self.windows_list_frame, orient=tk.VERTICAL,
                                           command=self.windows_canvas.yview)
        self.windows_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.windows_canvas.configure(yscrollcommand=self.windows_scrollbar.set)
        
        # Frame inside canvas for buttons
        self.windows_container = tk.Frame(self.windows_canvas, bg="white")
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
        
        # Sample windows (will be populated from actual data)
        self.windows_list = []
        self.active_window_id = None
        
        # Status bar
        self.status_frame = tk.Frame(self.main_frame, bg="#e0e0e0", height=22)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(5, 0))
        
        self.status_var = tk.StringVar()
        self.status_var.set("Waiting for connection...")
        self.status_bar = tk.Label(self.status_frame, textvariable=self.status_var, 
                                bg="#e0e0e0", fg=self.secondary_color, 
                                font=self.small_font, anchor=tk.W, padx=10)
        self.status_bar.pack(fill=tk.X)
        
        # Control panel
        self.control_frame = tk.Frame(self.main_frame, bg=self.bg_color, height=50, pady=10)
        self.control_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Connection button
        self.connect_button = tk.Button(self.control_frame, text="Start Monitoring", 
                                      font=self.normal_font, bg=self.accent_color, fg="white",
                                      padx=15, pady=5, relief=tk.FLAT,
                                      command=self.start_server)
        self.connect_button.pack(side=tk.LEFT, padx=5)
        
        # Disconnect button
        self.disconnect_button = tk.Button(self.control_frame, text="Stop Monitoring",
                                         font=self.normal_font, bg=self.warning_color, fg="white",
                                         padx=15, pady=5, relief=tk.FLAT,
                                         command=self.stop_server)
        self.disconnect_button.pack(side=tk.LEFT, padx=5)
        
        # Refresh windows list button
        self.refresh_button = tk.Button(self.control_frame, text="Refresh Apps List",
                                      font=self.normal_font, bg="#4CAF50", fg="white",
                                      padx=15, pady=5, relief=tk.FLAT,
                                      command=self.request_windows_list)
        self.refresh_button.pack(side=tk.LEFT, padx=5)
        
        # Pause screen button - NEW
        self.pause_button = tk.Button(self.control_frame, text="Pause Screen",
                                    font=self.normal_font, bg="#FF9800", fg="white",
                                    padx=15, pady=5, relief=tk.FLAT,
                                    command=self.pause_screen)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        # Server settings
        self.server_ip = "0.0.0.0"  # Listen on all interfaces
        self.server_port = 5555
        
        # Server status
        self.server_running = False
        self.client_socket = None
        self.server_socket = None
        self.screen_paused = False
        
    def start_server(self):
        if not self.server_running:
            self.server_thread = threading.Thread(target=self.run_server)
            self.server_thread.daemon = True
            self.server_running = True
            self.server_thread.start()
            self.status_var.set("Server started. Waiting for connection...")
            self.connect_button.config(state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL)
    
    def stop_server(self):
        self.server_running = False
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()
        self.status_var.set("Server stopped")
        self.clear_windows_list()
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
                    self.status_var.set(f"Connected to {addr[0]}:{addr[1]}")
                    
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
                        self.status_var.set(f"Connection error: {str(e)}")
                    break
                    
        except Exception as e:
            self.status_var.set(f"Server error: {str(e)}")
        finally:
            if self.server_socket:
                self.server_socket.close()
            self.server_running = False
            self.root.after(0, lambda: self.connect_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.disconnect_button.config(state=tk.DISABLED))
    
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
                    self.status_var.set(f"Error receiving data: {str(e)}")
                break
        
        # Connection closed
        self.status_var.set("Connection closed")
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
                self.status_var.set(f"Error processing screen capture: {str(e)}")
    
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
                self.status_var.set(f"Error processing windows list: {str(e)}")
    
    def update_windows_list(self, windows_data):
        # Clear existing windows list
        self.clear_windows_list()
        
        # Create a new window button for each window
        for window_id, window_info in windows_data.items():
            window_title = window_info['title']
            window_process = window_info['process']
            
            # Create a button frame
            btn_frame = tk.Frame(self.windows_container, bg="white", cursor="hand2")
            btn_frame.pack(fill=tk.X, padx=3, pady=3)
            
            # Create inner frame with border for hover effect
            inner_frame = tk.Frame(btn_frame, bg="white", bd=1, relief=tk.GROOVE, padx=5, pady=5)
            inner_frame.pack(fill=tk.X)
            
            # Process icon
            icon_frame = tk.Frame(inner_frame, bg=self.accent_color, width=30, height=30)
            icon_frame.pack(side=tk.LEFT, padx=(0, 10))
            icon_frame.pack_propagate(False)
            
            icon_label = tk.Label(icon_frame, text=window_process[0].upper(), 
                               bg=self.accent_color, fg="white", font=("Segoe UI", 12, "bold"))
            icon_label.pack(fill=tk.BOTH, expand=True)
            
            # Window info frame
            info_frame = tk.Frame(inner_frame, bg="white")
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Window title (truncated if too long)
            title_text = window_title
            if len(title_text) > 25:
                title_text = title_text[:22] + "..."
                
            title_label = tk.Label(info_frame, text=title_text, bg="white", 
                                fg=self.text_color, font=self.normal_font, anchor=tk.W)
            title_label.pack(fill=tk.X, anchor=tk.W)
            
            # Process name
            process_label = tk.Label(info_frame, text=window_process, bg="white",
                                  fg=self.secondary_color, font=self.small_font, anchor=tk.W)
            process_label.pack(fill=tk.X, anchor=tk.W)
            
            # Store the window information
            self.windows_list.append((window_id, btn_frame, inner_frame))
            
            # Make the entire frame clickable
            for widget in [btn_frame, inner_frame, icon_frame, icon_label, info_frame, title_label, process_label]:
                widget.bind("<Button-1>", lambda e, wid=window_id: self.select_window(wid))
                # Add hover effect
                widget.bind("<Enter>", lambda e, f=inner_frame: self.on_hover_enter(f))
                widget.bind("<Leave>", lambda e, f=inner_frame, wid=window_id: self.on_hover_leave(f, wid))
            
            # Highlight active window if any
            if self.active_window_id and window_id == self.active_window_id:
                inner_frame.config(bg=self.highlight_color)
                info_frame.config(bg=self.highlight_color)
                title_label.config(bg=self.highlight_color)
                process_label.config(bg=self.highlight_color)
    
    def on_hover_enter(self, frame):
        if frame.cget("bg") != self.highlight_color:
            frame.config(bg="#f5f5f5")
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Frame) and widget.winfo_children()[0].cget("bg") != self.accent_color:
                    widget.config(bg="#f5f5f5")
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label):
                            child.config(bg="#f5f5f5")

    def on_hover_leave(self, frame, window_id):
        if window_id != self.active_window_id:
            frame.config(bg="white")
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Frame) and widget.winfo_children()[0].cget("bg") != self.accent_color:
                    widget.config(bg="white")
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label):
                            child.config(bg="white")
    
    def clear_windows_list(self):
        # Destroy all window buttons
        for window_id, btn_frame, _ in self.windows_list:
            btn_frame.destroy()
        self.windows_list = []
    
    def select_window(self, window_id):
        if self.client_socket and self.server_running:
            try:
                # Update active window ID
                self.active_window_id = window_id
                
                # Update UI to highlight selected window
                for wid, _, frame in self.windows_list:
                    if wid == window_id:
                        frame.config(bg=self.highlight_color)
                        for widget in frame.winfo_children():
                            if isinstance(widget, tk.Frame) and widget.winfo_children()[0].cget("bg") != self.accent_color:
                                widget.config(bg=self.highlight_color)
                                for child in widget.winfo_children():
                                    if isinstance(child, tk.Label):
                                        child.config(bg=self.highlight_color)
                    else:
                        frame.config(bg="white")
                        for widget in frame.winfo_children():
                            if isinstance(widget, tk.Frame) and widget.winfo_children()[0].cget("bg") != self.accent_color:
                                widget.config(bg="white")
                                for child in widget.winfo_children():
                                    if isinstance(child, tk.Label):
                                        child.config(bg="white")
                
                # Send command to client to focus on this window
                command = b'\x01' + window_id.to_bytes(8, byteorder='big')
                self.client_socket.sendall(command)
                
                # Update view label
                for wid, _, _ in self.windows_list:
                    if wid == window_id:
                        for _, window_info in windows_data.items():
                            if window_info['id'] == wid:
                                self.view_label.config(text=f"Current View: {window_info['title']}")
                                break
                
                self.status_var.set(f"Viewing window: {window_id}")
                
            except Exception as e:
                self.status_var.set(f"Error selecting window: {str(e)}")
    
    def request_windows_list(self):
        if self.client_socket and self.server_running:
            try:
                # Send command to request windows list
                command = b'\x02'
                self.client_socket.sendall(command)
                
                self.status_var.set("Refreshing applications list...")
                
            except Exception as e:
                self.status_var.set(f"Error requesting windows list: {str(e)}")
    
    def pause_screen(self):
        if self.client_socket and self.server_running:
            try:
                # Toggle pause state
                self.screen_paused = not self.screen_paused
                
                # Send pause command to client
                command = b'\x03' + (b'\x01' if self.screen_paused else b'\x00')
                self.client_socket.sendall(command)
                
                # Update button text
                if self.screen_paused:
                    self.pause_button.config(text="Resume Screen", bg="#4CAF50")
                    self.status_var.set("Screen paused. Showing message to student.")
                else:
                    self.pause_button.config(text="Pause Screen", bg="#FF9800")
                    self.status_var.set("Screen resumed.")
                
            except Exception as e:
                self.status_var.set(f"Error toggling screen pause: {str(e)}")

def main():
    root = tk.Tk()
    app = ParentMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()