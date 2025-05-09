import socket
import pickle
import tkinter as tk
from PIL import Image, ImageTk
import threading
import io
import time

class ParentMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parent Monitoring App")
        self.root.geometry("1024x768")
        
        # Create main container
        self.main_container = tk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Main screen display
        self.left_panel = tk.Frame(self.main_container)
        self.main_container.add(self.left_panel, weight=3)
        
        # Screen label for the main display
        self.screen_label = tk.Label(self.left_panel, bg="#333333")
        self.screen_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Right panel - Window list
        self.right_panel = tk.Frame(self.main_container, bg="#e0e0e0", width=200)
        self.main_container.add(self.right_panel, weight=1)
        
        # Windows list label
        tk.Label(self.right_panel, text="Open Windows", font=("Arial", 12, "bold"),
                bg="#e0e0e0").pack(fill=tk.X, padx=5, pady=10)
        
        # Container for window buttons
        self.windows_container = tk.Frame(self.right_panel, bg="#e0e0e0")
        self.windows_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sample windows (will be populated from actual data)
        self.windows_list = []
        self.active_window_id = None
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Waiting for connection...")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Control panel
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        # Connection button
        self.connect_button = tk.Button(self.control_frame, text="Start Monitoring", 
                                      command=self.start_server, bg="#4CAF50", fg="white")
        self.connect_button.pack(side=tk.LEFT, padx=5)
        
        # Disconnect button
        self.disconnect_button = tk.Button(self.control_frame, text="Stop Monitoring", 
                                         command=self.stop_server, bg="#f44336", fg="white")
        self.disconnect_button.pack(side=tk.LEFT, padx=5)
        
        # Refresh windows list button
        self.refresh_button = tk.Button(self.control_frame, text="Refresh Windows List", 
                                      command=self.request_windows_list, bg="#2196F3", fg="white")
        self.refresh_button.pack(side=tk.LEFT, padx=5)
        
        # Server settings
        self.server_ip = "0.0.0.0"  # Listen on all interfaces
        self.server_port = 5555
        
        # Server status
        self.server_running = False
        self.client_socket = None
        self.server_socket = None
        
    def start_server(self):
        if not self.server_running:
            self.server_thread = threading.Thread(target=self.run_server)
            self.server_thread.daemon = True
            self.server_running = True
            self.server_thread.start()
            self.status_var.set("Server started. Waiting for connection...")
    
    def stop_server(self):
        self.server_running = False
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()
        self.status_var.set("Server stopped")
        
        # Clear windows list
        self.clear_windows_list()
    
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
            
            # Create a button frame with icon and text
            btn_frame = tk.Frame(self.windows_container, bg="#f0f0f0", bd=1, relief=tk.RAISED)
            btn_frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Process icon (you could use actual icons in a real app)
            icon_label = tk.Label(btn_frame, text=window_process[0].upper(), 
                               bg="#4285f4", fg="white", width=2, height=1)
            icon_label.pack(side=tk.LEFT, padx=5, pady=5)
            
            # Window title (truncated if too long)
            title_text = window_title
            if len(title_text) > 25:
                title_text = title_text[:22] + "..."
                
            title_label = tk.Label(btn_frame, text=title_text, bg="#f0f0f0", anchor=tk.W)
            title_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            # Store the window information and create a command to select this window
            self.windows_list.append((window_id, btn_frame))
            
            # Make the entire frame clickable
            btn_frame.bind("<Button-1>", lambda e, wid=window_id: self.select_window(wid))
            title_label.bind("<Button-1>", lambda e, wid=window_id: self.select_window(wid))
            icon_label.bind("<Button-1>", lambda e, wid=window_id: self.select_window(wid))
            
            # Highlight active window if any
            if self.active_window_id and window_id == self.active_window_id:
                btn_frame.config(bg="#e1f5fe")
                title_label.config(bg="#e1f5fe")
    
    def clear_windows_list(self):
        # Destroy all window buttons
        for window_id, btn_frame in self.windows_list:
            btn_frame.destroy()
        self.windows_list = []
    
    def select_window(self, window_id):
        if self.client_socket and self.server_running:
            try:
                # Update active window ID
                self.active_window_id = window_id
                
                # Update UI to highlight selected window
                for wid, btn_frame in self.windows_list:
                    if wid == window_id:
                        btn_frame.config(bg="#e1f5fe")
                        for child in btn_frame.winfo_children():
                            if isinstance(child, tk.Label) and child.cget("text") != child.cget("text").upper():
                                child.config(bg="#e1f5fe")
                    else:
                        btn_frame.config(bg="#f0f0f0")
                        for child in btn_frame.winfo_children():
                            if isinstance(child, tk.Label) and child.cget("text") != child.cget("text").upper():
                                child.config(bg="#f0f0f0")
                
                # Send command to client to focus on this window
                command = b'\x01' + window_id.to_bytes(8, byteorder='big')
                self.client_socket.sendall(command)
                
                self.status_var.set(f"Selected window: {window_id}")
                
            except Exception as e:
                self.status_var.set(f"Error selecting window: {str(e)}")
    
    def request_windows_list(self):
        if self.client_socket and self.server_running:
            try:
                # Send command to request windows list
                command = b'\x02'
                self.client_socket.sendall(command)
                
                self.status_var.set("Requested windows list...")
                
            except Exception as e:
                self.status_var.set(f"Error requesting windows list: {str(e)}")

def main():
    root = tk.Tk()
    app = ParentMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()