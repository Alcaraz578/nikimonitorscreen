import socket
import pickle
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance
import threading
import io
import time
from tkinter import font as tkfont
from tkinter import ttk
import json
from datetime import datetime
import math
import random

class FuturisticParentMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GUARDIAN - Advanced Monitoring System")
        self.root.geometry("1280x800")
        
        # Set refined professional theme and colors
        self.bg_color = "#0F1A2B"  # Deep navy background
        self.secondary_bg = "#162A45"  # Slightly lighter background
        self.accent_primary = "#3A7BDB"  # Professional blue accent
        self.accent_secondary = "#E63E6D"  # Professional rose accent
        self.accent_tertiary = "#39B0CA"  # Professional teal accent
        self.accent_quaternary = "#5D3E8D"  # Professional purple accent
        self.text_color = "#F0F4F9"  # Soft white text
        self.secondary_text = "#A1B4CE"  # Light blue/gray text
        self.panel_bg = "#1C3048"  # Panel background
        self.highlight_color = "#2A4365"  # Highlight color
        
        # Custom fonts - more professional
        try:
            # Try to use professional system fonts if available
            self.title_font = tkfont.Font(family="Segoe UI", size=16, weight="bold")
            self.subtitle_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")
            self.normal_font = tkfont.Font(family="Segoe UI", size=10)
            self.small_font = tkfont.Font(family="Segoe UI", size=9)
            self.button_font = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        except:
            # Fall back to system default
            self.title_font = tkfont.Font(size=16, weight="bold")
            self.subtitle_font = tkfont.Font(size=12, weight="bold")
            self.normal_font = tkfont.Font(size=10)
            self.small_font = tkfont.Font(size=9)
            self.button_font = tkfont.Font(size=10, weight="bold")
        
        # Create custom styles for ttk widgets
        self.configure_styles()
        
        # Create canvas for the main background with gradient effect
        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create gradient background
        self.create_gradient_background()
        
        # Main container
        self.main_frame = tk.Frame(self.canvas, bg=self.bg_color)
        self.canvas.create_window(0, 0, anchor="nw", window=self.main_frame, width=1280, height=800)
        
        # Create futuristic header
        self.create_header()
        
        # Create main content area
        self.create_content_area()
        
        # Create control panel
        self.create_control_panel()
        
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
        
        # Start ambient animation
        self.start_ambient_animation()
        
        # Display sample data
        self.root.after(100, self.load_sample_data)
        
    def configure_styles(self):
        """Configure custom styles with professional appearance"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles - more professional
        style.configure("Accent.TButton", 
                        font=self.button_font, 
                        background=self.accent_primary, 
                        foreground="white",
                        padding=(12, 6))  # More balanced padding
        
        style.map("Accent.TButton",
                background=[('active', self.highlight_color)],
                relief=[('pressed', 'sunken')])
        
        style.configure("Warning.TButton", 
                        font=self.button_font, 
                        background=self.accent_secondary,
                        foreground="white",
                        padding=(12, 6))
        
        style.configure("Success.TButton", 
                        font=self.button_font, 
                        background=self.accent_tertiary,
                        foreground="white",
                        padding=(12, 6))
        
        # Configure treeview styles - more professional
        style.configure("Treeview", 
                        background=self.panel_bg,
                        foreground=self.text_color,
                        fieldbackground=self.panel_bg,
                        borderwidth=0)
        
        style.map("Treeview",
                background=[('selected', self.highlight_color)],
                foreground=[('selected', self.text_color)])
        
        style.configure("Treeview.Heading", 
                        background=self.highlight_color,
                        foreground=self.text_color,
                        relief="flat",
                        font=self.normal_font)
        
        # Configure entry styles - more professional
        style.configure("TEntry", 
                        background=self.panel_bg,
                        foreground=self.text_color,
                        fieldbackground=self.panel_bg,
                        insertcolor=self.text_color,
                        borderwidth=1)
    
    def create_gradient_background(self):
        """Create a refined gradient background with subtle grid"""
        # Create gradient background
        width, height = 1280, 800
        self.bg_image = Image.new('RGBA', (width, height), self.bg_color)
        draw = ImageDraw.Draw(self.bg_image)
        
        # Create subtle radial gradient
        for i in range(width + height):
            # More subtle gradient
            alpha = int(200 - i * 0.08) if i * 0.08 < 200 else 0
            if alpha > 0:
                draw.ellipse((0 - i, 0 - i, i, i), 
                            fill=(58, 123, 213, alpha//12))  # More subtle blue
                draw.ellipse((width - i, height - i, width + i, height + i), 
                            fill=(93, 62, 141, alpha//12))   # More subtle purple
        
        # Add refined noise texture (less dense)
        for _ in range(500):  # Reduced from 1000
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            alpha = random.randint(3, 15)  # More subtle particles
            draw.point((x, y), fill=(255, 255, 255, alpha))
        
        # Apply slight blur
        self.bg_image = self.bg_image.filter(ImageFilter.GaussianBlur(radius=15))
        
        # Convert to PhotoImage and display
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        
        # Add professional grid lines (thinner, more subtle)
        for i in range(0, width, 100):
            self.canvas.create_line(i, 0, i, height, fill=f"#{40:02x}{50:02x}{80:02x}", width=0.5)
        for i in range(0, height, 100):
            self.canvas.create_line(0, i, width, i, fill=f"#{40:02x}{50:02x}{80:02x}", width=0.5)
    
    def create_header(self):
        """Create futuristic curved header bar"""
        # Header frame
        self.header_height = 70
        self.header_frame = tk.Frame(self.main_frame, height=self.header_height)
        self.header_frame.pack(fill=tk.X)
        self.header_frame.pack_propagate(False)
        
        # Header canvas for curved design
        self.header_canvas = tk.Canvas(self.header_frame, 
                                     highlightthickness=0, 
                                     bg=self.bg_color)
        self.header_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create gradient header
        self.draw_curved_header()
        
        # App title in header
        self.header_canvas.create_text(40, 35, 
                                     text="GUARDIAN", 
                                     font=self.title_font, 
                                     fill="white", 
                                     anchor="w")
        
        self.header_canvas.create_text(210, 35, 
                                      text="Advanced Monitoring System", 
                                      font=self.normal_font, 
                                      fill=self.secondary_text, 
                                      anchor="w")
        
        # Status indicator in header
        self.connection_indicator = self.header_canvas.create_oval(1050, 35, 1070, 55, 
                                                                fill=self.accent_secondary, 
                                                                outline="")
        
        # Add glow effect to indicator
        self.header_canvas.create_oval(1048, 33, 1072, 57, 
                                     fill="", 
                                     outline=self.accent_secondary, 
                                     width=2)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Disconnected")
        self.status_text = self.header_canvas.create_text(1090, 45, 
                                                       text=self.status_var.get(), 
                                                       font=self.normal_font, 
                                                       fill="white", 
                                                       anchor="w")
    
    def draw_curved_header(self):
        """Draw curved gradient header"""
        width = self.root.winfo_width()
        height = self.header_height
        
        # Create gradient header image
        header_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(header_img)
        
        # Draw gradient
        for i in range(width):
            # Calculate gradient color - more professional
            r = int(58 + (58 - 45) * i / width)
            g = int(123 + (123 - 90) * i / width)
            b = int(219 + (219 - 180) * i / width)
            draw.line([(i, 0), (i, height)], fill=(r, g, b))
        
        # Apply curve at the bottom
        mask = Image.new('L', (width, height), 0)
        mask_draw = ImageDraw.Draw(mask)
        
        # Draw curve - more subtle
        mask_draw.rectangle((0, 0, width, height - 20), fill=255)
        for x in range(width):
            y_offset = int(8 * math.sin(math.pi * x / width))  # Less dramatic curve
            mask_draw.rectangle((x, height - 20, x + 1, height - 20 + y_offset), fill=255)
        
        # Apply mask
        header_img.putalpha(mask)
        
        # Apply slight blur for smoothness
        header_img = header_img.filter(ImageFilter.GaussianBlur(radius=1))
        
        # Convert to PhotoImage
        self.header_photo = ImageTk.PhotoImage(header_img)
        
        # Display header
        self.header_canvas.create_image(0, 0, image=self.header_photo, anchor="nw")
    
    def create_content_area(self):
        """Create main content area with screen view and apps list"""
        # Content frame
        self.content_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel for screen view
        self.create_screen_panel()
        
        # Right panel for applications and tabs
        self.create_apps_panel()
    
    def create_screen_panel(self):
        """Create left panel for screen view"""
        # Screen panel - left side (70% width)
        self.screen_panel = tk.Frame(self.content_frame, bg=self.bg_color)
        self.screen_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Canvas for screen view with curved border
        self.screen_canvas = tk.Canvas(self.screen_panel, 
                                     highlightthickness=0, 
                                     bg=self.bg_color)
        self.screen_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create curved panel for screen
        self.screen_frame_img = None  # Will hold the image for the frame
        self.screen_photo = None  # Will hold the photo for the screen content
        self.screen_item = None  # Will hold canvas item for screen content
        
        # Draw initial screen panel
        self.draw_screen_panel()
        
        # Screen title
        self.screen_canvas.create_text(30, 35, 
                                     text="LIVE VIEW", 
                                     font=self.subtitle_font, 
                                     fill="white", 
                                     anchor="w")
        
        # Add control dots - smaller, more refined
        self.screen_canvas.create_oval(self.screen_width - 150, 35, self.screen_width - 142, 43, 
                                     fill=self.accent_tertiary, outline="")
        self.screen_canvas.create_oval(self.screen_width - 130, 35, self.screen_width - 122, 43, 
                                     fill=self.accent_secondary, outline="")
        self.screen_canvas.create_oval(self.screen_width - 110, 35, self.screen_width - 102, 43, 
                                     fill=self.accent_primary, outline="")
        
        # Current window info at bottom
        self.view_label_text = "Current View: None"
        self.view_label = self.screen_canvas.create_text(30, self.screen_height - 30, 
                                                      text=self.view_label_text, 
                                                      font=self.normal_font, 
                                                      fill="white", 
                                                      anchor="w")
        
        # Activity meter
        self.draw_activity_meter()
    
    def draw_activity_meter(self):
        """Draw activity meter with professional styling"""
        # Background - more subtle rounded corners
        self.screen_canvas.create_rounded_rectangle(
            self.screen_width - 200, self.screen_height - 38,
            self.screen_width - 50, self.screen_height - 22,
            radius=4, fill=self.secondary_bg, outline=self.highlight_color)
        
        # Active part (will be updated) - professional gradient
        self.activity_meter = self.screen_canvas.create_rounded_rectangle(
            self.screen_width - 200, self.screen_height - 38,
            self.screen_width - 120, self.screen_height - 22,
            radius=4, fill=self.accent_tertiary, outline="")
        
        # Label - better positioned
        self.screen_canvas.create_text(
            self.screen_width - 125, self.screen_height - 30,
            text="ACTIVITY", font=self.small_font, fill=self.text_color)
    
    def draw_screen_panel(self):
        """Draw screen panel with professional styling"""
        # Get panel dimensions
        self.screen_width = self.screen_panel.winfo_width() 
        if self.screen_width < 100:
            self.screen_width = 800  
            
        self.screen_height = self.screen_panel.winfo_height()
        if self.screen_height < 100:
            self.screen_height = 600
        
        # Create rounded panel with more subtle corners
        panel_img = Image.new('RGBA', (self.screen_width, self.screen_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(panel_img)
        
        # Main panel background - more subtle transparency and refined color
        draw.rounded_rectangle(
            (0, 0, self.screen_width, self.screen_height), 
            radius=10,  # Reduced from 20 for more professional look
            fill=(28, 48, 72, 180))
        
        # Header bar - more professional gradient
        draw.rounded_rectangle(
            (0, 0, self.screen_width, 70),
            radius=10,
            fill=(58, 123, 219, 230))  # More transparent, professional blue
        
        # Bottom status bar - more professional
        draw.rounded_rectangle(
            (0, self.screen_height - 60, self.screen_width, self.screen_height),
            radius=(0, 0, 10, 10),  # Only round bottom corners, smaller radius
            fill=(30, 40, 70, 180))
        
        # Main screen area - cleaner look
        self.screen_area = (20, 80, self.screen_width - 20, self.screen_height - 70)
        draw.rounded_rectangle(
            self.screen_area,
            radius=6,  # Smaller radius for more professional look
            fill=(25, 35, 60, 140))  # Slightly more opaque for better contrast
        
        # Apply slight blur for a professional look
        panel_img = panel_img.filter(ImageFilter.GaussianBlur(radius=0.3))  # More subtle blur
        
        # Add a subtle border to enhance professionalism
        draw = ImageDraw.Draw(panel_img)
        draw.rounded_rectangle(
            (0, 0, self.screen_width, self.screen_height),
            radius=10,
            outline=(100, 140, 200, 40),  # Subtle border
            width=1)
        
        # Convert to PhotoImage
        self.screen_frame_img = ImageTk.PhotoImage(panel_img)
        
        # Display on canvas
        self.screen_frame = self.screen_canvas.create_image(
            0, 0, image=self.screen_frame_img, anchor="nw")
    
    def create_apps_panel(self):
        """Create right panel for applications and tabs"""
        # Apps panel - right side (30% width)
        self.apps_panel_width = 350  # Fixed width
        self.apps_panel = tk.Frame(self.content_frame, bg=self.bg_color, width=self.apps_panel_width)
        self.apps_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Canvas for apps panel with curved border
        self.apps_canvas = tk.Canvas(self.apps_panel, 
                                   highlightthickness=0, 
                                   bg=self.bg_color)
        self.apps_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Draw apps panel
        self.draw_apps_panel()
        
        # Create tabbed interface
        self.create_tab_interface()
        
        # Create apps list
        self.create_apps_list()
        
        # Create history tab content
        self.create_history_tab()
        
        # Create analytics panel
        self.create_analytics_panel()
    
    def draw_apps_panel(self):
        """Draw apps panel with curved borders"""
        # Get panel dimensions
        apps_width = self.apps_panel_width
        apps_height = 600  # Default height
        
        # Create rounded panel
        panel_img = Image.new('RGBA', (apps_width, apps_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(panel_img)
        
        # Main panel background
        draw.rounded_rectangle(
            (0, 0, apps_width, apps_height), 
            radius=10,  # More professional radius
            fill=(28, 48, 72, 180))  # More professional color
        
        # Tab bar
        draw.rounded_rectangle(
            (0, 0, apps_width, 50),
            radius=(10, 10, 0, 0),  # Only round top corners
            fill=(25, 35, 60, 220))  # Darker, more professional
        
        # Active tab
        draw.rounded_rectangle(
            (0, 0, apps_width // 2, 50),
            radius=(10, 10, 0, 0),  # Only round top corners
            fill=(58, 123, 219, 230))  # Professional blue
        
        # Apply slight blur for a modern look
        panel_img = panel_img.filter(ImageFilter.GaussianBlur(radius=0.3))  # More subtle blur
        
        # Add subtle border
        draw = ImageDraw.Draw(panel_img)
        draw.rounded_rectangle(
            (0, 0, apps_width, apps_height),
            radius=10,
            outline=(100, 140, 200, 40),  # Subtle border
            width=1)
        
        # Convert to PhotoImage
        self.apps_frame_img = ImageTk.PhotoImage(panel_img)
        
        # Display on canvas
        self.apps_frame = self.apps_canvas.create_image(
            0, 0, image=self.apps_frame_img, anchor="nw")
    
    def create_tab_interface(self):
        """Create tab interface on apps panel"""
        # Tab labels
        self.apps_canvas.create_text(
            self.apps_panel_width // 4, 25,
            text="APPLICATIONS", font=self.subtitle_font, fill="white")
        
        self.apps_canvas.create_text(
            self.apps_panel_width // 4 * 3, 25,
            text="HISTORY", font=self.normal_font, fill=self.secondary_text)
        
        # Make tabs clickable
        self.apps_canvas.tag_bind(
            self.apps_canvas.create_rectangle(
                0, 0, self.apps_panel_width // 2, 50,
                fill="", outline=""),
            "<Button-1>", lambda e: self.switch_tab("apps"))
        
        self.apps_canvas.tag_bind(
            self.apps_canvas.create_rectangle(
                self.apps_panel_width // 2, 0, self.apps_panel_width, 50,
                fill="", outline=""),
            "<Button-1>", lambda e: self.switch_tab("history"))
    
    def create_apps_list(self):
        """Create applications list area"""
        # Search bar - more professional
        search_bg = self.apps_canvas.create_rounded_rectangle(
            20, 70, self.apps_panel_width - 20, 110,
            radius=6, fill=self.panel_bg)  # Smaller radius
        
        # Search icon - more refined
        self.apps_canvas.create_oval(35, 90, 43, 98, outline=self.secondary_text, width=1)
        self.apps_canvas.create_line(41, 96, 48, 103, fill=self.secondary_text, width=1)
        
        # Search text
        self.apps_canvas.create_text(
            60, 90, text="Search applications...",
            font=self.normal_font, fill=self.secondary_text, anchor="w")
        
        # Container for app cards
        self.apps_container = tk.Frame(self.apps_canvas, bg=self.panel_bg)
        self.apps_container_window = self.apps_canvas.create_window(
            20, 130, window=self.apps_container,
            anchor="nw", width=self.apps_panel_width - 40, height=420)
        
        # Apps container will be populated with cards
    
    def create_history_tab(self):
        """Create history tab content (initially hidden)"""
        # Container for history tab
        self.history_container = tk.Frame(self.apps_canvas, bg=self.panel_bg)
        self.history_container_window = self.apps_canvas.create_window(
            20, 130, window=self.history_container,
            anchor="nw", width=self.apps_panel_width - 40, height=420)
        
        # Hide initially
        self.apps_canvas.itemconfigure(self.history_container_window, state="hidden")
        
        # Search bar for history
        self.history_search_frame = tk.Frame(self.history_container, bg=self.panel_bg)
        self.history_search_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.history_search_var = tk.StringVar()
        self.history_search_entry = ttk.Entry(
            self.history_search_frame, textvariable=self.history_search_var,
            font=self.normal_font)
        self.history_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.history_search_button = ttk.Button(
            self.history_search_frame, text="Search", style="Accent.TButton")
        self.history_search_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Create tree view for history
        columns = ('time', 'title', 'url')
        self.history_tree = ttk.Treeview(
            self.history_container, columns=columns, show='headings', height=15)
        
        # Define headings
        self.history_tree.heading('time', text='Time')
        self.history_tree.heading('title', text='Page Title')
        self.history_tree.heading('url', text='URL')
        
        # Define columns
        self.history_tree.column('time', width=70)
        self.history_tree.column('title', width=150)
        self.history_tree.column('url', width=120)
        
        # Add scrollbar
        self.history_scrollbar = ttk.Scrollbar(
            self.history_container, orient=tk.VERTICAL,
            command=self.history_tree.yview)
        self.history_tree.configure(yscroll=self.history_scrollbar.set)
        
        # Pack elements
        self.history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Highlight suspicious searches
        self.highlight_suspicious_patterns = [
            'game', 'minecraft', 'cheat', 'play', 'youtube', 'roblox', 'discord']
        
        # Configure tag appearance - more professional highlight
        self.history_tree.tag_configure(
            'suspicious', background=self.accent_secondary, foreground='white')
    
    def create_analytics_panel(self):
        """Create analytics panel below apps list"""
        # Analytics panel background - more professional
        analytics_bg = self.apps_canvas.create_rounded_rectangle(
            0, 560, self.apps_panel_width, 690,
            radius=8, fill=(28, 48, 72, 180))  # More professional color
        
        # Header bar - more professional
        analytics_header = self.apps_canvas.create_rounded_rectangle(
            0, 560, self.apps_panel_width, 600,
            radius=(8, 8, 0, 0), fill=self.accent_secondary)
        
        # Title
        self.apps_canvas.create_text(
            20, 580, text="ACTIVITY INSIGHTS",
            font=self.subtitle_font, fill="white", anchor="w")
        
        # Activity graph background - more professional
        graph_bg = self.apps_canvas.create_rounded_rectangle(
            20, 620, self.apps_panel_width - 20, 680,
            radius=6, fill=(25, 35, 60, 180))  # More professional
        
        # Draw activity graph
        self.draw_activity_graph()
        
        # Alert message - more professional
        self.apps_canvas.create_text(
            20, 700, text="Gaming activity detected in the last 15 minutes",
            font=self.small_font, fill=self.accent_secondary, anchor="w")
    
    def draw_activity_graph(self):
        """Draw activity graph in analytics panel"""
        # Sample data points for graph
        points = [
            (30, 670), (60, 650), (90, 660), (120, 630), (150, 645),
            (180, 620), (210, 635), (240, 610), (270, 600), (300, 620)
        ]
        
        # Draw connecting line - smoother
        self.apps_canvas.create_line(
            points, fill=self.accent_secondary, width=1.5, smooth=True)  # Thinner, more professional
        
        # Draw points - more professional
        for x, y in points:
            # Regular points - smaller for professional look
            self.apps_canvas.create_oval# Regular points - smaller for professional look
            self.apps_canvas.create_oval(
                x - 2, y - 2, x + 2, y + 2,  # Smaller points
                fill=self.accent_tertiary, outline="")
        
        # Highlight current point - more subtle highlight
        self.apps_canvas.create_oval(
            270 - 3, 600 - 3, 270 + 3, 600 + 3,  # Smaller highlight
            fill=self.accent_secondary, outline=self.text_color, width=0.5)  # Added subtle outline
    
    def create_control_panel(self):
        """Create bottom control panel"""
        # Control panel frame
        self.control_frame = tk.Frame(self.main_frame, bg=self.bg_color, height=80)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)
        
        # Canvas for control panel with curved border
        self.control_canvas = tk.Canvas(
            self.control_frame, highlightthickness=0, bg=self.bg_color, height=80)
        self.control_canvas.pack(fill=tk.X)
        
        # Draw control panel
        self.draw_control_panel()
        
        # Control buttons - improved proportions
        button_width = 160  # Slightly smaller for better proportions
        button_height = 36  # Slightly smaller for better proportions
        button_radius = 6   # Smaller radius for more professional look
        button_y = 22       # Better vertical centering
        
        # Start Monitoring button
        start_button_bg = self.control_canvas.create_rounded_rectangle(
            20, button_y, 20 + button_width, button_y + button_height,
            radius=button_radius, fill=self.accent_tertiary)
        
        self.control_canvas.create_text(
            20 + button_width // 2, button_y + button_height // 2,
            text="START MONITORING",
            font=self.button_font, fill="white")
        
        # Make button clickable
        self.control_canvas.tag_bind(
            start_button_bg, "<Button-1>", lambda e: self.start_server())
        
        # Stop Monitoring button
        stop_button_bg = self.control_canvas.create_rounded_rectangle(
            220, button_y, 220 + button_width, button_y + button_height,
            radius=button_radius, fill=self.accent_secondary)
        
        self.control_canvas.create_text(
            220 + button_width // 2, button_y + button_height // 2,
            text="STOP MONITORING",
            font=self.button_font, fill="white")
        
        # Make button clickable
        self.control_canvas.tag_bind(
            stop_button_bg, "<Button-1>", lambda e: self.stop_server())
        
        # Refresh Apps button
        refresh_button_bg = self.control_canvas.create_rounded_rectangle(
            420, button_y, 420 + button_width, button_y + button_height,
            radius=button_radius, fill=self.accent_quaternary)
        
        self.control_canvas.create_text(
            420 + button_width // 2, button_y + button_height // 2,
            text="REFRESH APPS LIST",
            font=self.button_font, fill="white")
        
        # Make button clickable
        self.control_canvas.tag_bind(
            refresh_button_bg, "<Button-1>", lambda e: self.request_windows_list())
        
        # Get History button - more professional outline button
        history_button_bg = self.control_canvas.create_rounded_rectangle(
            620, button_y, 620 + button_width, button_y + button_height,
            radius=button_radius, fill=self.panel_bg, outline=self.accent_primary, width=1)
        
        self.control_canvas.create_text(
            620 + button_width // 2, button_y + button_height // 2,
            text="GET SEARCH HISTORY",
            font=self.button_font, fill="white")
        
        # Make button clickable
        self.control_canvas.tag_bind(
            history_button_bg, "<Button-1>", lambda e: self.request_browser_history())
        
        # Pause Screen button - more professional outline button
        pause_button_bg = self.control_canvas.create_rounded_rectangle(
            820, button_y, 820 + button_width, button_y + button_height,
            radius=button_radius, fill=self.panel_bg, outline=self.accent_secondary, width=1)
        
        self.control_canvas.create_text(
            820 + button_width // 2, button_y + button_height // 2,
            text="PAUSE SCREEN",
            font=self.button_font, fill="white")
        
        # Make button clickable
        self.control_canvas.tag_bind(
            pause_button_bg, "<Button-1>", lambda e: self.pause_screen())
    
    def draw_control_panel(self):
        """Draw control panel with curved borders"""
        width = self.root.winfo_width() if self.root.winfo_width() > 100 else 1280
        height = 80
        
        # Create rounded panel - more professional
        panel_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(panel_img)
        
        # Main panel background - more professional
        draw.rounded_rectangle(
            (0, 0, width, height), 
            radius=8,  # Smaller radius for professional look
            fill=(28, 48, 72, 180))  # More professional color
        
        # Subtle gradient overlay
        for i in range(width):
            # More subtle gradient
            r = int(28 + (28 - 25) * i / width)
            g = int(48 + (48 - 43) * i / width)
            b = int(72 + (72 - 65) * i / width)
            alpha = 80 - i // 15 if i < 600 else 0  # More subtle fade
            
            if alpha > 0:
                draw.line([(i, 0), (i, height)], fill=(r, g, b, alpha))
        
        # Apply slight blur for a professional look
        panel_img = panel_img.filter(ImageFilter.GaussianBlur(radius=0.3))  # More subtle blur
        
        # Add subtle border
        draw = ImageDraw.Draw(panel_img)
        draw.rounded_rectangle(
            (0, 0, width, height),
            radius=8,
            outline=(100, 140, 200, 40),  # Subtle border
            width=1)
        
        # Convert to PhotoImage
        self.control_frame_img = ImageTk.PhotoImage(panel_img)
        
        # Display on canvas
        self.control_frame_item = self.control_canvas.create_image(
            0, 0, image=self.control_frame_img, anchor="nw")
    
    def load_sample_data(self):
        """Load sample data for demo purposes"""
        # Populate apps list with sample windows
        self.windows_list = list(self.sample_windows.values())
        self.update_apps_list()
        
        # Update browser history
        self.browser_history = self.sample_history
        self.update_history_list()
        
        # Create sample screen image
        self.create_sample_screen()
        
        # Update status
        self.update_status("Ready to connect", "orange")
    
    def create_sample_screen(self):
        """Create a sample screen image"""
        # Create a sample screen image
        width = int(self.screen_area[2] - self.screen_area[0])
        height = int(self.screen_area[3] - self.screen_area[1])
        
        # Create sample desktop - more professional look
        screen_img = Image.new('RGB', (width, height), (25, 35, 60))  # Darker, more professional
        draw = ImageDraw.Draw(screen_img)
        
        # Draw desktop background - more subtle grid
        for i in range(0, width, 40):  # Larger grid for cleaner look
            for j in range(0, height, 40):
                # Create grid - more subtle
                alpha = random.randint(10, 25)  # Less contrast
                draw.rectangle((i, j, i+38, j+38), 
                               fill=(30, 40, 70, alpha))
        
        # Draw some windows - more professional
        draw.rounded_rectangle((50, 50, 350, 250), radius=6,  # Smaller radius
                              fill=(58, 123, 219))  # Professional blue
        draw.rounded_rectangle((60, 80, 340, 240), radius=4,  # Smaller radius
                              fill=(240, 245, 250))  # Slightly off-white for better contrast
        draw.text((65, 60), "Minecraft", fill=(255, 255, 255))
        
        # Another window - more professional
        draw.rounded_rectangle((200, 150, 500, 350), radius=6,  # Smaller radius
                              fill=(240, 245, 250))  # Slightly off-white
        draw.rounded_rectangle((200, 150, 500, 180), radius=(6, 6, 0, 0),  # Only round top corners
                              fill=(220, 225, 235))  # Subtle title bar
        draw.text((210, 160), "Google Chrome", fill=(60, 60, 80))  # Darker text
        
        # Taskbar - more professional
        draw.rectangle((0, height-40, width, height), 
                      fill=(30, 40, 70))  # Darker, more professional
        
        # Add subtle highlight at top of taskbar
        draw.line((0, height-40, width, height-40), fill=(60, 80, 120, 100), width=1)
        
        # Start button - more professional
        draw.rounded_rectangle((10, height-35, 50, height-5), radius=4,  # Smaller radius
                              fill=(58, 123, 219))  # Professional blue
        
        # Clock - more professional
        current_time = datetime.now().strftime("%H:%M")
        draw.text((width-60, height-25), current_time, fill=(220, 225, 235))  # Slightly off-white
        
        # Convert to PhotoImage
        self.screen_photo = ImageTk.PhotoImage(screen_img)
        
        # Display on canvas
        self.screen_item = self.screen_canvas.create_image(
            self.screen_area[0], self.screen_area[1], 
            image=self.screen_photo, anchor="nw")
        
        # Update current view label
        self.view_label_text = "Current View: Minecraft"
        self.screen_canvas.itemconfig(self.view_label, text=self.view_label_text)
        
        # Update active window
        self.active_window_id = 1
    
    def start_ambient_animation(self):
        """Start refined ambient animation effects"""
        def update_animation():
            # More subtle pulse effect for connection indicator
            pulse_size = 1.5 * math.sin(time.time() * 2) + 1.5  # Less dramatic
            self.header_canvas.coords(
                self.connection_indicator,
                1050 - pulse_size, 35 - pulse_size, 
                1070 + pulse_size, 55 + pulse_size)
            
            # More subtle activity meter animation
            activity_width = 80 + 20 * math.sin(time.time() * 0.7)  # Slower, less extreme
            self.screen_canvas.coords(
                self.activity_meter,
                self.screen_width - 200, self.screen_height - 38,
                self.screen_width - 200 + activity_width, self.screen_height - 22)
            
            # Schedule next update
            self.root.after(50, update_animation)
        
        # Start animation
        update_animation()
    
    def update_status(self, status_text, color="red"):
        """Update connection status indicator"""
        self.status_var.set(status_text)
        self.header_canvas.itemconfig(self.status_text, text=status_text)
        
        if color == "green":
            fill_color = self.accent_tertiary
        elif color == "orange":
            fill_color = "#E9973E"  # Professional orange
        else:
            fill_color = self.accent_secondary
            
        self.header_canvas.itemconfig(self.connection_indicator, fill=fill_color)
    
    def update_apps_list(self):
        """Update applications list with current windows"""
        # Clear existing app cards
        for widget in self.apps_container.winfo_children():
            widget.destroy()
        
        # Create cards for each app - more professional cards
        for i, window in enumerate(self.windows_list):
            # Create app card with subtle border
            card = tk.Frame(self.apps_container, bg=self.panel_bg, bd=1, 
                          relief="solid", highlightbackground="#3A5175", highlightthickness=1)
            card.pack(fill=tk.X, pady=4, padx=2)  # Better spacing
            
            # Add circular icon
            icon_canvas = tk.Canvas(card, width=36, height=36,  # Smaller icon
                                   bg=self.panel_bg, highlightthickness=0)
            icon_canvas.pack(side=tk.LEFT, padx=8)  # Better spacing
            
            # Determine icon color based on app type - more professional colors
            if "chrome" in window["process"].lower():
                icon_color = "#4285F4"  # Google blue
            elif "java" in window["process"].lower():
                icon_color = "#27AE60"  # Professional green
            elif "discord" in window["process"].lower():
                icon_color = "#5865F2"  # Discord brand color
            else:
                icon_color = self.accent_primary
            
            # Draw icon - smaller, more refined
            icon_canvas.create_oval(4, 4, 32, 32, fill=icon_color, outline="")
            
            # Add app info with better spacing
            info_frame = tk.Frame(card, bg=self.panel_bg)
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)
            
            # App title - better font
            title_label = tk.Label(info_frame, text=window["title"],
                                 font=self.normal_font, bg=self.panel_bg,
                                 fg=self.text_color, anchor="w", justify=tk.LEFT)
            title_label.pack(fill=tk.X, anchor="w", pady=(3, 0))  # Better spacing
            
            # Process name - more subdued
            process_label = tk.Label(info_frame, text=window["process"],
                                  font=self.small_font, bg=self.panel_bg,
                                  fg=self.secondary_text, anchor="w", justify=tk.LEFT)
            process_label.pack(fill=tk.X, anchor="w")
            
            # View button - more professional
            view_button = ttk.Button(card, text="View", style="Accent.TButton",
                                   command=lambda wid=window["id"]: self.view_application(wid))
            view_button.pack(side=tk.RIGHT, padx=8, pady=4)  # Better spacing
    
    def update_history_list(self):
        """Update browser history list"""
        # Clear existing entries
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Insert new history data
        for entry in self.browser_history:
            # Check if entry matches suspicious patterns
            is_suspicious = any(pattern.lower() in entry["url"].lower() or 
                              pattern.lower() in entry["title"].lower() 
                              for pattern in self.highlight_suspicious_patterns)
            
            # Insert with appropriate tag
            if is_suspicious:
                self.history_tree.insert('', tk.END, values=(
                    entry["time"], entry["title"], entry["url"]), tags=('suspicious',))
            else:
                self.history_tree.insert('', tk.END, values=(
                    entry["time"], entry["title"], entry["url"]))
    
    def switch_tab(self, tab_name):
        """Switch between apps and history tabs"""
        if tab_name == "apps":
            # Show apps tab
            self.apps_canvas.itemconfigure(self.apps_container_window, state="normal")
            self.apps_canvas.itemconfigure(self.history_container_window, state="hidden")
            
            # Update tab styling
            self.apps_canvas.itemconfigure(
                self.apps_canvas.create_text(
                    self.apps_panel_width // 4, 25,
                    text="APPLICATIONS", font=self.subtitle_font, fill="white"),
                state="normal")
            
            self.apps_canvas.itemconfigure(
                self.apps_canvas.create_text(
                    self.apps_panel_width // 4 * 3, 25,
                    text="HISTORY", font=self.normal_font, fill=self.secondary_text),
                state="normal")
            
        elif tab_name == "history":
            # Show history tab
            self.apps_canvas.itemconfigure(self.apps_container_window, state="hidden")
            self.apps_canvas.itemconfigure(self.history_container_window, state="normal")
            
            # Update tab styling
            self.apps_canvas.itemconfigure(
                self.apps_canvas.create_text(
                    self.apps_panel_width // 4, 25,
                    text="APPLICATIONS", font=self.normal_font, fill=self.secondary_text),
                state="normal")
            
            self.apps_canvas.itemconfigure(
                self.apps_canvas.create_text(
                    self.apps_panel_width // 4 * 3, 25,
                    text="HISTORY", font=self.subtitle_font, fill="white"),
                state="normal")
    
    def view_application(self, window_id):
        """Request view of specific application"""
        if self.server_running and self.client_socket:
            # Send view command to client
            try:
                command = {"command": "view_window", "window_id": window_id}
                self.client_socket.send(pickle.dumps(command))
                
                # Update active window ID
                self.active_window_id = window_id
                window_title = "Unknown"
                
                # Find window title
                for window in self.windows_list:
                    if window["id"] == window_id:
                        window_title = window["title"]
                        break
                
                # Update current view label
                self.view_label_text = f"Current View: {window_title}"
                self.screen_canvas.itemconfig(self.view_label, text=self.view_label_text)
                
            except Exception as e:
                print(f"Error sending view command: {e}")
        else:
            # Update with sample data for demo
            self.active_window_id = window_id
            
            # Find window title
            window_title = "Unknown"
            for window in self.windows_list:
                if window["id"] == window_id:
                    window_title = window["title"]
                    break
            
            # Update current view label
            self.view_label_text = f"Current View: {window_title}"
            self.screen_canvas.itemconfig(self.view_label, text=self.view_label_text)
    
    def pause_screen(self):
        """Pause or resume screen updates"""
        self.screen_paused = not self.screen_paused
        
        if self.server_running and self.client_socket:
            # Send pause command to client
            try:
                command = {"command": "pause_screen", "paused": self.screen_paused}
                self.client_socket.send(pickle.dumps(command))
            except Exception as e:
                print(f"Error sending pause command: {e}")
    
    def request_windows_list(self):
        """Request list of open windows from client"""
        if self.server_running and self.client_socket:
            # Send request command to client
            try:
                command = {"command": "get_windows"}
                self.client_socket.send(pickle.dumps(command))
            except Exception as e:
                print(f"Error sending windows request: {e}")
        else:
            # Use sample data for demo
            self.windows_list = list(self.sample_windows.values())
            self.update_apps_list()
    
    def request_browser_history(self):
        """Request browser history from client"""
        if self.server_running and self.client_socket:
            # Send request command to client
            try:
                command = {"command": "get_history"}
                self.client_socket.send(pickle.dumps(command))
            except Exception as e:
                print(f"Error sending history request: {e}")
        else:
            # Use sample data for demo
            self.browser_history = self.sample_history
            self.update_history_list()
            self.switch_tab("history")
    
    def start_server(self):
        """Start monitoring server"""
        if not self.server_running:
            # Start server in a separate thread
            server_thread = threading.Thread(target=self.run_server)
            server_thread.daemon = True
            server_thread.start()
            
            # Update status
            self.server_running = True
            self.update_status("Server started, waiting for connection...", "orange")
    
    def stop_server(self):
        """Stop monitoring server"""
        if self.server_running:
            # Close client connection if exists
            if self.client_socket:
                try:
                    command = {"command": "disconnect"}
                    self.client_socket.send(pickle.dumps(command))
                    self.client_socket.close()
                except:
                    pass
                finally:
                    self.client_socket = None
            
            # Close server socket
            if self.server_socket:
                try:
                    self.server_socket.close()
                except:
                    pass
                finally:
                    self.server_socket = None
            
            # Update status
            self.server_running = False
            self.update_status("Disconnected", "red")
    
    def run_server(self):
        """Run monitoring server in a separate thread"""
        try:
            # Create server socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.server_ip, self.server_port))
            self.server_socket.listen(1)
            
            print(f"Server started on {self.server_ip}:{self.server_port}")
            
            # Update status on UI thread
            self.root.after(0, lambda: self.update_status("Waiting for connection...", "orange"))
            
            # Accept client connection
            self.client_socket, addr = self.server_socket.accept()
            
            print(f"Connection from {addr}")
            
            # Update status on UI thread
            self.root.after(0, lambda: self.update_status(f"Connected to {addr[0]}", "green"))
            
            # Start receiving data
            self.receive_data()
            
        except Exception as e:
            print(f"Server error: {e}")
            # Update status on UI thread
            self.root.after(0, lambda: self.update_status("Server error", "red"))
            self.server_running = False
    
    def receive_data(self):
        """Receive and process data from client"""
        buffer_size = 4096
        data = b""
        
        while self.server_running and self.client_socket:
            try:
                # Receive chunk of data
                chunk = self.client_socket.recv(buffer_size)
                
                if not chunk:
                    # Connection closed
                    break
                
                # Add chunk to buffer
                data += chunk
                
                # Try to unpickle the data
                try:
                    # Check if we have complete data
                    obj = pickle.loads(data)
                    
                    # Process received object
                    self.process_received_data(obj)
                    
                    # Reset buffer
                    data = b""
                    
                except pickle.UnpicklingError:
                    # Incomplete data, continue receiving
                    pass
                
            except Exception as e:
                print(f"Error receiving data: {e}")
                break
        
        # Connection closed or error occurred
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
        
        # Update status on UI thread
        self.root.after(0, lambda: self.update_status("Disconnected", "red"))
        
        print("Connection closed")
    
    def process_received_data(self, data):
        """Process received data from client"""
        # Check data type
        if isinstance(data, dict):
            # Command response
            if "type" in data:
                data_type = data["type"]
                
                if data_type == "screenshot":
                    # Process screenshot
                    self.update_screenshot(data["data"])
                    
                elif data_type == "windows_list":
                    # Process windows list
                    self.windows_list = data["data"]
                    # Update UI on main thread
                    self.root.after(0, self.update_apps_list)
                    
                elif data_type == "browser_history":
                    # Process browser history
                    self.browser_history = data["data"]
                    # Update UI on main thread
                    self.root.after(0, self.update_history_list)
                    # Switch to history tab
                    self.root.after(0, lambda: self.switch_tab("history"))
    
    def update_screenshot(self, screenshot_data):
        """Update screenshot on UI"""
        if not self.screen_paused:
            try:
                # Convert bytes to image
                screen_bytes = io.BytesIO(screenshot_data)
                screen_img = Image.open(screen_bytes)
                
                # Resize to fit screen area
                width = int(self.screen_area[2] - self.screen_area[0])
                height = int(self.screen_area[3] - self.screen_area[1])
                screen_img = screen_img.resize((width, height), Image.LANCZOS)
                
                # Convert to PhotoImage
                self.screen_photo = ImageTk.PhotoImage(screen_img)
                
                # Update canvas item
                if self.screen_item:
                    self.screen_canvas.itemconfig(self.screen_item, image=self.screen_photo)
                else:
                    self.screen_item = self.screen_canvas.create_image(
                        self.screen_area[0], self.screen_area[1], 
                        image=self.screen_photo, anchor="nw")
            
            except Exception as e:
                print(f"Error updating screenshot: {e}")

# Add custom shape function to Canvas class
tk.Canvas.create_rounded_rectangle = lambda self, x1, y1, x2, y2, radius=25, **kwargs: self.create_polygon(
    x1+radius, y1,
    x2-radius, y1,
    x2, y1,
    x2, y1+radius,
    x2, y2-radius,
    x2, y2,
    x2-radius, y2,
    x1+radius, y2,
    x1, y2,
    x1, y2-radius,
    x1, y1+radius,
    x1, y1,
    smooth=True, **kwargs)

if __name__ == "__main__":
    root = tk.Tk()
    app = FuturisticParentMonitorApp(root)
    root.mainloop()
    