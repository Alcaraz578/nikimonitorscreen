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
        
        # Create a frame for the screen display
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a label to display the screen captures
        self.screen_label = tk.Label(self.frame)
        self.screen_label.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Waiting for connection...")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Control panel
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        # Connection button
        self.connect_button = tk.Button(self.control_frame, text="Start Monitoring", command=self.start_server)
        self.connect_button.pack(side=tk.LEFT, padx=5)
        
        # Disconnect button
        self.disconnect_button = tk.Button(self.control_frame, text="Stop Monitoring", command=self.stop_server)
        self.disconnect_button.pack(side=tk.LEFT, padx=5)
        
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
    
    def run_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.server_ip, self.server_port))
            self.server_socket.listen(1)
            
            while self.server_running:
                try:
                    self.client_socket, addr = self.server_socket.accept()
                    self.status_var.set(f"Connected to {addr[0]}:{addr[1]}")
                    self.receive_screen()
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
    
    def receive_screen(self):
        try:
            data_size = b""
            while len(data_size) < 8:
                packet = self.client_socket.recv(8 - len(data_size))
                if not packet:
                    return
                data_size += packet
            
            data_size = int.from_bytes(data_size, byteorder='big')
            
            # Receive the screen data
            screen_data = b""
            while len(screen_data) < data_size:
                packet = self.client_socket.recv(min(4096, data_size - len(screen_data)))
                if not packet:
                    return
                screen_data += packet
            
            # Convert the data to an image and display it
            image = Image.open(io.BytesIO(screen_data))
            photo = ImageTk.PhotoImage(image)
            self.screen_label.config(image=photo)
            self.screen_label.image = photo
            
            # Continue receiving screens
            if self.server_running:
                self.root.after(10, self.receive_screen)
                
        except Exception as e:
            if self.server_running:
                self.status_var.set(f"Error receiving screen: {str(e)}")
            if self.client_socket:
                self.client_socket.close()

def main():
    root = tk.Tk()
    app = ParentMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()