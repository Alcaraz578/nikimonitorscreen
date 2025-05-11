def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """Create a rounded rectangle on a canvas with single radius value"""
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    
    # Convert fill color if it's a tuple (for compatibility between PIL and tkinter)
    if 'fill' in kwargs and isinstance(kwargs['fill'], tuple):
        r, g, b = kwargs['fill'][:3]
        kwargs['fill'] = f'#{r:02x}{g:02x}{b:02x}'
    
    # Convert outline color if it's a tuple
    if 'outline' in kwargs and isinstance(kwargs['outline'], tuple):
        r, g, b = kwargs['outline'][:3]
        kwargs['outline'] = f'#{r:02x}{g:02x}{b:02x}'
        
    return canvas.create_polygon(points, smooth=True, **kwargs)
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
        
        # Set refined professional theme and colors - upgraded for maximum visual impact
        self.bg_color = "#0A1520"  # Deeper, richer navy
        self.secondary_bg = "#12243A"  # Darker secondary
        self.accent_primary = "#2563EB"  # More vibrant blue
        self.accent_secondary = "#DC2626"  # Bolder red
        self.accent_tertiary = "#0EA5E9"  # Brighter teal
        self.accent_quaternary = "#7C3AED"  # Richer purple
        self.text_color = "#F8FAFC"  # Crisp white text
        self.secondary_text = "#94A3B8"  # More refined gray
        self.panel_bg = "#1E293B"  # Deeper panel background
        self.highlight_color = "#334155"  # Darker highlight
        
        # Custom fonts - more professional and modern
        try:
            # Try to use professional system fonts if available
            self.title_font = tkfont.Font(family="SF Pro Display", size=16, weight="bold")
            self.subtitle_font = tkfont.Font(family="SF Pro Display", size=12, weight="bold")
            self.normal_font = tkfont.Font(family="SF Pro Text", size=10)
            self.small_font = tkfont.Font(family="SF Pro Text", size=9)
            self.button_font = tkfont.Font(family="SF Pro Text", size=10, weight="bold")
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
        """Configure custom styles with ultra-professional appearance"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles - premium modern
        style.configure("Accent.TButton", 
                        font=self.button_font, 
                        background=self.accent_primary, 
                        foreground="white",
                        padding=(14, 8))  # Slightly larger for premium feel
        
        style.map("Accent.TButton",
                background=[('active', '#1e40af'), ('pressed', '#1e3a8a')],
                relief=[('pressed', 'sunken')])
        
        style.configure("Warning.TButton", 
                        font=self.button_font, 
                        background=self.accent_secondary,
                        foreground="white",
                        padding=(14, 8))
                        
        style.map("Warning.TButton",
                background=[('active', '#b91c1c'), ('pressed', '#991b1b')],
                relief=[('pressed', 'sunken')])
        
        style.configure("Success.TButton", 
                        font=self.button_font, 
                        background=self.accent_tertiary,
                        foreground="white",
                        padding=(14, 8))
                        
        style.map("Success.TButton",
                background=[('active', '#0369a1'), ('pressed', '#0c4a6e')],
                relief=[('pressed', 'sunken')])
        
        # Configure outline button styles
        style.configure("OutlineAccent.TButton", 
                        font=self.button_font, 
                        background=self.panel_bg,
                        foreground=self.text_color,
                        padding=(14, 8),
                        borderwidth=1)
                        
        style.map("OutlineAccent.TButton",
                background=[('active', self.highlight_color)],
                foreground=[('active', self.accent_primary)],
                relief=[('pressed', 'sunken')])
        
        # Configure treeview styles - premium
        style.configure("Treeview", 
                        background=self.panel_bg,
                        foreground=self.text_color,
                        fieldbackground=self.panel_bg,
                        borderwidth=0,
                        rowheight=28)  # Increased for premium look
        
        style.map("Treeview",
                background=[('selected', self.accent_primary)],
                foreground=[('selected', self.text_color)])
        
        style.configure("Treeview.Heading", 
                        background=self.highlight_color,
                        foreground=self.text_color,
                        relief="flat",
                        font=self.normal_font,
                        padding=6)  # Added padding for premium look
        
        # Configure entry styles - premium glass effect
        style.configure("TEntry", 
                        background=self.panel_bg,
                        foreground=self.text_color,
                        fieldbackground=self.panel_bg,
                        insertcolor=self.text_color,
                        borderwidth=1,
                        padding=8)  # Added padding for premium look
    
    def create_gradient_background(self):
        """Create a refined gradient background with subtle grid"""
        # Create gradient background
        width, height = 1280, 800
        self.bg_image = Image.new('RGBA', (width, height), self.bg_color)
        draw = ImageDraw.Draw(self.bg_image)
        
        # Create enhanced radial gradient with higher quality
        for i in range(0, width + height, 2):  # Smaller steps for smoother gradient
            # More sophisticated gradient with multiple color points
            alpha_base = int(180 - i * 0.06) if i * 0.06 < 180 else 0
            if alpha_base > 0:
                # Primary accent gradient from top left
                draw.ellipse((0 - i, 0 - i, i, i), 
                            fill=(37, 99, 235, alpha_base//8))  # Refined blue glow
                
                # Secondary accent gradient from bottom right
                draw.ellipse((width - i, height - i, width + i, height + i), 
                            fill=(124, 58, 237, alpha_base//9))  # Refined purple glow
                
                # Third accent point for added dimension
                if i % 3 == 0:  # Only some iterations for performance
                    draw.ellipse((width//2 - i//2, 0 - i//3, width//2 + i//2, i//3), 
                                fill=(14, 165, 233, alpha_base//15))  # Subtle cyan highlight
        
        # Add professional noise texture (more refined, less dense)
        for _ in range(400):  # Reduced density
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            size = random.randint(1, 2)  # Vary the size for depth
            alpha = random.randint(2, 10)  # More subtle particles
            
            # Vary the color slightly for a more dynamic feel
            color_variant = random.randint(-20, 20)
            r = min(255, max(0, 255 + color_variant))
            g = min(255, max(0, 255 + color_variant))
            b = min(255, max(0, 255 + color_variant))
            
            draw.rectangle((x, y, x+size, y+size), fill=(r, g, b, alpha))
        
        # Apply sophisticated blur with multiple passes
        self.bg_image = self.bg_image.filter(ImageFilter.GaussianBlur(radius=20))
        
        # Add subtle vignette effect for depth
        vignette = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        vignette_draw = ImageDraw.Draw(vignette)
        
        # Create radial gradient for vignette
        for i in range(0, max(width, height), 4):
            alpha = int(i * 0.15) if i * 0.15 < 60 else 60  # Max 60 alpha (subtle)
            vignette_draw.ellipse((width//2 - i, height//2 - i, width//2 + i, height//2 + i), 
                                fill=(0, 0, 0, 0), outline=(0, 0, 0, alpha))
        
        # Apply vignette
        self.bg_image = Image.alpha_composite(self.bg_image.convert('RGBA'), vignette)
        
        # Convert to PhotoImage and display
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        
        # Add professional grid lines (thinner, more refined)
        for i in range(0, width, 80):  # Wider spacing
            self.canvas.create_line(i, 0, i, height, fill=f"#{30:02x}{40:02x}{60:02x}", width=0.5, dash=(4, 4))  # Dashed line
        for i in range(0, height, 80):
            self.canvas.create_line(0, i, width, i, fill=f"#{30:02x}{40:02x}{60:02x}", width=0.5, dash=(4, 4))  # Dashed line
    
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
        """Draw curved gradient header with professional glossy effect"""
        width = self.root.winfo_width()
        height = self.header_height
        
        # Create gradient header image
        header_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(header_img)
        
        # Draw sophisticated gradient
        for i in range(width):
            # Calculate gradient color - modern professional scheme
            progress = i / width
            
            # Use a multi-stop gradient for a more professional look
            if progress < 0.3:
                # Start with deeper blue
                r = int(37 + (99 - 37) * progress / 0.3)
                g = int(99 + (109 - 99) * progress / 0.3)
                b = int(235 + (239 - 235) * progress / 0.3)
            elif progress < 0.7:
                # Transition to brighter mid tone
                midpoint = (progress - 0.3) / 0.4
                r = int(99 + (79 - 99) * midpoint)
                g = int(109 + (128 - 109) * midpoint)
                b = int(239 + (248 - 239) * midpoint)
            else:
                # End with deeper accent
                endpoint = (progress - 0.7) / 0.3
                r = int(79 + (99 - 79) * endpoint)
                g = int(128 + (139 - 128) * endpoint)
                b = int(248 + (255 - 248) * endpoint)
                
            draw.line([(i, 0), (i, height)], fill=(r, g, b, 230))
        
        # Apply curve at the bottom - more refined
        mask = Image.new('L', (width, height), 0)
        mask_draw = ImageDraw.Draw(mask)
        
        # Draw curve - subtle with perfect bezier-like quality
        mask_draw.rectangle((0, 0, width, height - 15), fill=255)
        
        # More natural curved bottom with sine curve
        for x in range(width):
            # Use sine function for more natural curve
            curve_height = int(6 * math.sin(math.pi * x / width * 1.5 + 0.2) + 7)
            mask_draw.rectangle((x, height - 15, x + 1, height - 15 + curve_height), fill=255)
        
        # Add subtle highlight for glossy effect at top
        for i in range(10):
            # Decreasing alpha for gradient highlight
            highlight_alpha = 60 - i * 6
            y_pos = 6 + i
            draw.line([(0, y_pos), (width, y_pos)], fill=(255, 255, 255, highlight_alpha))
        
        # Apply mask
        header_img.putalpha(mask)
        
        # Apply slight blur for smoothness
        header_img = header_img.filter(ImageFilter.GaussianBlur(radius=0.7))
        
        # Convert to PhotoImage
        self.header_photo = ImageTk.PhotoImage(header_img)
        
        # Display header
        self.header_canvas.create_image(0, 0, image=self.header_photo, anchor="nw")
        
        # Add subtle divider line at bottom
        self.header_canvas.create_line(
            0, height-1, width, height-1, 
            fill=f"#{255:02x}{255:02x}{255:02x}", 
            width=1,
            dash=(2, 2),
            stipple="gray25"
        )
    
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
        """Draw activity meter with premium glossy styling"""
        # Premium background with depth effect - outer glow
        self.screen_canvas.create_rounded_rectangle(
            self.screen_width - 210, self.screen_height - 43,
            self.screen_width - 40, self.screen_height - 17,
            radius=13, fill=None, outline=self.highlight_color)
            
        # Main background - inset with glass effect
        self.screen_canvas.create_rounded_rectangle(
            self.screen_width - 205, self.screen_height - 40,
            self.screen_width - 45, self.screen_height - 20,
            radius=10, fill=self.secondary_bg, outline=self.highlight_color)
        
        # Activity indicator (will be updated) - premium gradient
        self.activity_meter = self.screen_canvas.create_rounded_rectangle(
            self.screen_width - 205, self.screen_height - 40,
            self.screen_width - 125, self.screen_height - 20,
            radius=10, fill=self.accent_tertiary, outline="")
        
        # Add glossy highlight to the activity meter
        self.activity_highlight = self.screen_canvas.create_rounded_rectangle(
            self.screen_width - 205, self.screen_height - 40,
            self.screen_width - 125, self.screen_height - 30,
            radius=5, fill=None, outline=self.text_color, width=0.5)
        
        # Label with premium styling
        self.screen_canvas.create_text(
            self.screen_width - 125, self.screen_height - 30,
            text="ACTIVITY", font=self.small_font, fill=self.text_color)
            
        # Premium dot indicators
        dot_positions = [
            (self.screen_width - 185, "#DC2626"),  # Red alert
            (self.screen_width - 165, "#2563EB"),  # Blue normal
            (self.screen_width - 145, "#0EA5E9"),  # Cyan low
        ]
        
        for x_pos, color in dot_positions:
            # Create dot with glow effect
            self.screen_canvas.create_oval(
                x_pos - 3, self.screen_height - 54,
                x_pos + 3, self.screen_height - 48,
                fill=color, outline="")
                
            # Add subtle glow
            self.screen_canvas.create_oval(
                x_pos - 4, self.screen_height - 55,
                x_pos + 4, self.screen_height - 47,
                fill="", outline=color, width=0.5)
    
    def draw_screen_panel(self):
        """Draw screen panel with premium professional styling"""
        # Get panel dimensions
        self.screen_width = self.screen_panel.winfo_width() 
        if self.screen_width < 100:
            self.screen_width = 800  
            
        self.screen_height = self.screen_panel.winfo_height()
        if self.screen_height < 100:
            self.screen_height = 600
        
        # Create premium rounded panel
        panel_img = Image.new('RGBA', (self.screen_width, self.screen_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(panel_img)
        
        # Main panel background - premium dark glass effect
        draw.rounded_rectangle(
            (0, 0, self.screen_width, self.screen_height), 
            radius=12,  # Premium rounded corners
            fill=(20, 30, 50, 210))  # More contrasting, premium dark
        
        # Add subtle glass-like highlight at the top
        for i in range(6):
            highlight_alpha = 25 - i * 4
            highlight_y = 4 + i
            draw.line(
                [(10, highlight_y), (self.screen_width - 10, highlight_y)],
                fill=(255, 255, 255, highlight_alpha))
        
        # Header bar - premium gradient
        # Create gradient manually for more control
        header_height = 70
        for i in range(self.screen_width):
            # Calculate gradient position
            pos = i / self.screen_width
            
            # Multi-stop gradient for more premium look
            if pos < 0.4:
                # Start with primary accent
                r = int(37 + (59 - 37) * pos / 0.4)
                g = int(99 + (130 - 99) * pos / 0.4)
                b = int(235 + (246 - 235) * pos / 0.4)
            else:
                # Transition to secondary tone
                r = int(59 + (76 - 59) * (pos - 0.4) / 0.6)
                g = int(130 + (110 - 130) * (pos - 0.4) / 0.6)
                b = int(246 + (225 - 246) * (pos - 0.4) / 0.6)
                
            # Draw vertical line of the gradient
            for j in range(header_height):
                # Add vertical gradient as well
                alpha = 230 - (j * 30 // header_height)
                draw.point((i, j), fill=(r, g, b, alpha))
        
        # Ensure smooth rounded corners for header
        draw.rounded_rectangle(
            (0, 0, self.screen_width, header_height),
            radius=12,
            fill=None,  # No fill, just outline
            outline=(60, 120, 240, 100),  # Subtle outline
            width=1)
        
        # Bottom status bar - premium gradient glass effect
        status_bar_height = 60
        for i in range(self.screen_width):
            # Calculate gradient position
            pos = i / self.screen_width
            
            # Multi-stop gradient for premium look
            if pos < 0.3:
                r, g, b = 30, 40, 70
            elif pos < 0.7:
                r = int(30 + (40 - 30) * (pos - 0.3) / 0.4)
                g = int(40 + (50 - 40) * (pos - 0.3) / 0.4)
                b = int(70 + (90 - 70) * (pos - 0.3) / 0.4)
            else:
                r = int(40 + (50 - 40) * (pos - 0.7) / 0.3)
                g = int(50 + (60 - 50) * (pos - 0.7) / 0.3)
                b = int(90 + (110 - 90) * (pos - 0.7) / 0.3)
                
            # Draw vertical line with gradient
            for j in range(status_bar_height):
                y_pos = self.screen_height - status_bar_height + j
                # Add vertical gradient
                alpha = 180 + (j * 20 // status_bar_height)
                draw.point((i, y_pos), fill=(r, g, b, alpha))
        
        # Ensure smooth rounded corners for status bar
        draw.rounded_rectangle(
            (0, self.screen_height - status_bar_height, self.screen_width, self.screen_height),
            radius=12,
            fill=None,  # No fill, just outline
            outline=(60, 120, 240, 40),  # Subtle outline
            width=1)
        
        # Main screen area - premium inset glass effect
        self.screen_area = (20, 80, self.screen_width - 20, self.screen_height - 70)
        
        # Draw inner shadow for inset effect
        shadow_width = 2
        for i in range(shadow_width):
            alpha = 80 - (i * 80 // shadow_width)
            draw.rounded_rectangle(
                (self.screen_area[0] + i, 
                 self.screen_area[1] + i, 
                 self.screen_area[2] - i, 
                 self.screen_area[3] - i),
                radius=8,
                fill=None,
                outline=(0, 0, 0, alpha),
                width=1)
        
        # Main screen background - premium glass effect
        draw.rounded_rectangle(
            self.screen_area,
            radius=8,  # Premium rounded corners
            fill=(15, 25, 45, 180))  # Darker for better contrast
        
        # Add inner highlight for depth
        highlight_width = 1
        for i in range(highlight_width):
            alpha = 40 - (i * 40 // highlight_width)
            offset = i + 1
            draw.rounded_rectangle(
                (self.screen_area[0] + offset, 
                 self.screen_area[1] + offset, 
                 self.screen_area[2] - offset, 
                 self.screen_area[3] - offset),
                radius=8 - offset if 8 - offset > 0 else 1,
                fill=None,
                outline=(255, 255, 255, alpha),
                width=1)
        
        # Apply refined blur for professional polish
        panel_img = panel_img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Add subtle overall depth with a refined border
        draw = ImageDraw.Draw(panel_img)
        draw.rounded_rectangle(
            (0, 0, self.screen_width, self.screen_height),
            radius=12,
            fill=None,
            outline=(100, 140, 255, 30),  # Subtle blue glow
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
        """Draw apps panel with premium glass effect and modern design"""
        # Get panel dimensions
        apps_width = self.apps_panel_width
        apps_height = 600  # Default height
        
        # Create premium rounded panel
        panel_img = Image.new('RGBA', (apps_width, apps_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(panel_img)
        
        # Main panel background - premium dark glass effect
        draw.rounded_rectangle(
            (0, 0, apps_width, apps_height), 
            radius=12,  # Premium rounded corners
            fill=(20, 30, 50, 210))  # Premium dark
        
        # Add subtle glass-like horizontal highlight
        for i in range(4):
            highlight_alpha = 20 - i * 5
            highlight_y = 4 + i
            draw.line(
                [(10, highlight_y), (apps_width - 10, highlight_y)],
                fill=(255, 255, 255, highlight_alpha))
        
        # Tab bar with multi-stop gradient
        for i in range(apps_width):
            pos = i / apps_width
            
            # Multi-stop gradient
            if pos < 0.3:
                r = int(25 + (30 - 25) * pos / 0.3)
                g = int(35 + (40 - 35) * pos / 0.3)
                b = int(60 + (70 - 60) * pos / 0.3)
            else:
                r = int(30 + (35 - 30) * (pos - 0.3) / 0.7)
                g = int(40 + (45 - 40) * (pos - 0.3) / 0.7)
                b = int(70 + (80 - 70) * (pos - 0.3) / 0.7)
                
            # Draw vertical gradient for tab bar
            for j in range(50):  # 50px height
                alpha = 220 - (j * 40 // 50)  # Vertical gradient
                draw.point((i, j), fill=(r, g, b, alpha))
        
        # Ensure rounded corners for tab bar
        draw.rounded_rectangle(
            (0, 0, apps_width, 50),
            radius=12,  # Premium rounded corners
            fill=None,
            outline=(60, 80, 120, 40),
            width=1)
        
        # Active tab with premium gradient effect
        for i in range(apps_width // 2):
            pos = i / (apps_width // 2)
            
            # Multi-stop gradient for premium effect
            if pos < 0.3:
                r = int(37 + (45 - 37) * pos / 0.3)
                g = int(99 + (110 - 99) * pos / 0.3)
                b = int(235 + (245 - 235) * pos / 0.3)
            else:
                r = int(45 + (60 - 45) * (pos - 0.3) / 0.7)
                g = int(110 + (135 - 110) * (pos - 0.3) / 0.7)
                b = int(245 + (255 - 245) * (pos - 0.3) / 0.7)
                
            # Draw vertical gradient for active tab
            for j in range(50):  # 50px height
                alpha = 230 - (j * 30 // 50)  # Vertical gradient
                draw.point((i, j), fill=(r, g, b, alpha))
        
        # Ensure rounded corners for active tab
        draw.rounded_rectangle(
            (0, 0, apps_width // 2, 50),
            radius=12,  # Premium rounded corners
            fill=None,
            outline=(100, 150, 255, 60),
            width=1)
        
        # Apply refined blur for professional polish
        panel_img = panel_img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Add subtle glow border
        draw = ImageDraw.Draw(panel_img)
        draw.rounded_rectangle(
            (0, 0, apps_width, apps_height),
            radius=12,
            fill=None,
            outline=(100, 140, 255, 30),  # Subtle blue glow
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
            radius=8, fill=self.accent_secondary)  # Changed from (8, 8, 0, 0) to single value
        
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
        """Draw premium control panel with curved borders and glass effect"""
        width = self.root.winfo_width() if self.root.winfo_width() > 100 else 1280
        height = 80
        
        # Create premium rounded panel
        panel_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(panel_img)
        
        # Main panel background - premium dark glass effect
        draw.rounded_rectangle(
            (0, 0, width, height), 
            radius=12,  # Premium rounded corners
            fill=(20, 30, 50, 210))  # More contrasting, premium dark
        
        # Add subtle glass-like horizontal highlight
        for i in range(4):
            highlight_alpha = 20 - i * 5
            highlight_y = 4 + i
            draw.line(
                [(10, highlight_y), (width - 10, highlight_y)],
                fill=(255, 255, 255, highlight_alpha))
        
        # Create premium gradient overlay
        for i in range(width):
            # Calculate position
            pos = i / width
            
            # Use multi-stop gradient for premium look
            if pos < 0.3:
                r, g, b = 30, 40, 60
            elif pos < 0.7:
                r = int(30 + (35 - 30) * (pos - 0.3) / 0.4)
                g = int(40 + (45 - 40) * (pos - 0.3) / 0.4)
                b = int(60 + (70 - 60) * (pos - 0.3) / 0.4)
            else:
                r = int(35 + (40 - 35) * (pos - 0.7) / 0.3)
                g = int(45 + (50 - 45) * (pos - 0.7) / 0.3)
                b = int(70 + (80 - 70) * (pos - 0.7) / 0.3)
                
            # Apply with depth-enhancing alpha gradient
            alpha = 100 - (i * 30 // width)
            
            if alpha > 0:
                draw.line([(i, 0), (i, height)], fill=(r, g, b, alpha))
        
        # Apply premium blur effect
        panel_img = panel_img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Add subtle glow border
        draw = ImageDraw.Draw(panel_img)
        draw.rounded_rectangle(
            (0, 0, width, height),
            radius=12,
            fill=None,
            outline=(100, 140, 255, 30),  # Subtle blue glow
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
        """Create an ultra-premium professional sample screen image"""
        # Create a sample screen image
        width = int(self.screen_area[2] - self.screen_area[0])
        height = int(self.screen_area[3] - self.screen_area[1])
        
        # Create premium desktop background with sophisticated gradient
        screen_img = Image.new('RGB', (width, height), (15, 25, 45))
        draw = ImageDraw.Draw(screen_img)
        
        # Create luxury gradient background with depth
        for y in range(height):
            # Vertical gradient for premium depth
            progress = y / height
            
            # Multi-stop gradient for ultra-premium look
            if progress < 0.3:
                r = int(15 + (18 - 15) * progress / 0.3)
                g = int(25 + (30 - 25) * progress / 0.3)
                b = int(45 + (55 - 45) * progress / 0.3)
            elif progress < 0.7:
                r = int(18 + (20 - 18) * (progress - 0.3) / 0.4)
                g = int(30 + (35 - 30) * (progress - 0.3) / 0.4)
                b = int(55 + (65 - 55) * (progress - 0.3) / 0.4)
            else:
                r = int(20 + (22 - 20) * (progress - 0.7) / 0.3)
                g = int(35 + (38 - 35) * (progress - 0.7) / 0.3)
                b = int(65 + (70 - 65) * (progress - 0.7) / 0.3)
                
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add ultra-premium subtle grid
        for i in range(0, width, 40):
            # Vertical grid lines
            line_color = (30, 45, 80, 20)  # Very subtle
            for y in range(0, height, 4):  # Dotted line effect
                if y % 8 == 0:
                    draw.point((i, y), fill=line_color)
        
        for j in range(0, height, 40):
            # Horizontal grid lines
            for x in range(0, width, 4):  # Dotted line effect
                if x % 8 == 0:
                    draw.point((x, j), fill=line_color)
        
        # Add premium vignette effect for depth
        for i in range(40):
            alpha = int(i * 1.5)
            # Draw concentric rectangles with increasing darkness
            draw.rectangle(
                (i, i, width-i, height-i), 
                fill=None, 
                outline=(0, 0, 0, alpha))
        
        # Create translucent overlay for windows area
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Draw premium looking windows with sophisticated content
        
        # Main app window - Minecraft with premium styling
        main_window = self.draw_premium_window(
            overlay_draw, 40, 40, 550, 350, 
            "Minecraft 1.19 Premium Edition", "#62B47A", 
            game_window=True)
        
        # Add reflection effect to main window
        for i in range(30):
            alpha = int(150 - i * 5)
            if alpha > 0:
                # Draw highlight line with decreasing opacity
                overlay_draw.line(
                    (40 + i, 40 + i, 550 - i, 40 + i),
                    fill=(255, 255, 255, alpha))
        
        # Browser window with modern design
        browser_window = self.draw_premium_window(
            overlay_draw, 170, 120, 650, 420, 
            "Google Chrome - Educational Research", "#4285F4",
            browser=True, url="www.khanacademy.org/math/geometry")
        
        # Productivity app window - more professional look
        docs_window = self.draw_premium_window(
            overlay_draw, 390, 60, 740, 280, 
            "Research Notes - Document", "#0D6EFD", 
            doc_window=True)
        
        # Add ultra-modern taskbar with glass effect
        taskbar_height = 40
        overlay_draw.rectangle(
            (0, height-taskbar_height, width, height),
            fill=(10, 20, 35, 220))
            
        # Add glass highlight
        overlay_draw.line(
            (0, height-taskbar_height, width, height-taskbar_height),
            fill=(100, 150, 255, 40), width=1)
        
        # Add start button with premium look
        start_width = 45
        overlay_draw.rounded_rectangle(
            (10, height-taskbar_height+5, 10+start_width, height-5),
            radius=4,
            fill=(37, 99, 235))
            
        # Windows logo
        overlay_draw.rectangle(
            (15, height-taskbar_height+15, 25, height-taskbar_height+25),
            fill=(255, 255, 255))
        overlay_draw.rectangle(
            (27, height-taskbar_height+15, 37, height-taskbar_height+25),
            fill=(255, 255, 255))
        overlay_draw.rectangle(
            (15, height-taskbar_height+27, 25, height-taskbar_height+37),
            fill=(255, 255, 255))
        overlay_draw.rectangle(
            (27, height-taskbar_height+27, 37, height-taskbar_height+37),
            fill=(255, 255, 255))
            
        # Taskbar app icons with premium styling
        icons = [
            {"color": "#4285F4", "pos": 70, "letter": "C"},   # Chrome
            {"color": "#62B47A", "pos": 120, "letter": "M"},  # Minecraft
            {"color": "#0D6EFD", "pos": 170, "letter": "D"},  # Documents
            {"color": "#5865F2", "pos": 220, "letter": "D"},  # Discord
            {"color": "#EA4335", "pos": 270, "letter": "G"},  # Gmail
        ]
        
        icon_size = 30
        icon_y = height - taskbar_height + (taskbar_height - icon_size) // 2
        
        for icon in icons:
            # Base shape
            overlay_draw.rounded_rectangle(
                (icon["pos"], icon_y, icon["pos"]+icon_size, icon_y+icon_size),
                radius=6,
                fill=icon["color"])
                
            # Add highlight for 3D effect
            overlay_draw.line(
                (icon["pos"]+3, icon_y+3, icon["pos"]+icon_size-3, icon_y+3),
                fill=(255, 255, 255, 100))
                
            # Add icon letter
            text_x = icon["pos"] + icon_size//2
            text_y = icon_y + icon_size//2
            overlay_draw.text(
                (text_x, text_y),
                icon["letter"],
                fill=(255, 255, 255),
                anchor="mm")
        
        # Add clock with premium styling
        current_time = datetime.now().strftime("%H:%M")
        
        # Clock background
        overlay_draw.rounded_rectangle(
            (width-80, icon_y, width-15, icon_y+icon_size),
            radius=4,
            fill=(30, 40, 70, 180))
            
        # Clock text
        overlay_draw.text(
            (width-48, icon_y+icon_size//2),
            current_time,
            fill=(240, 240, 240),
            anchor="mm")
            
        # Add system tray icons
        tray_icons = [
            {"pos": width-100, "color": (240, 240, 240)},  # WiFi
            {"pos": width-130, "color": (240, 240, 240)},  # Volume
            {"pos": width-160, "color": (240, 240, 240)},  # Battery
        ]
        
        for icon in tray_icons:
            # Simple dot for system tray icons
            overlay_draw.ellipse(
                (icon["pos"], icon_y+12, icon["pos"]+6, icon_y+18),
                fill=icon["color"])
        
        # Compose the image
        screen_img = Image.alpha_composite(screen_img.convert('RGBA'), overlay)
        
        # Convert to PhotoImage
        self.screen_photo = ImageTk.PhotoImage(screen_img)
        
        # Display on canvas
        self.screen_item = self.screen_canvas.create_image(
            self.screen_area[0], self.screen_area[1], 
            image=self.screen_photo, anchor="nw")
        
        # Update current view label
        self.view_label_text = "Current View: Minecraft 1.19 Premium Edition"
        self.screen_canvas.itemconfig(self.view_label, text=self.view_label_text)
        
        # Update active window
        self.active_window_id = 1
    
    def draw_premium_window(self, draw, x, y, width, height, title, color, 
                            browser=False, game_window=False, doc_window=False, url=None):
        """Draw an ultra-premium looking window for the sample screen"""
        # Window border with subtle shadow
        shadow_color = (0, 0, 0, 30)
        
        # Draw shadow first for depth
        for i in range(5):
            alpha = 30 - i * 5
            if alpha > 0:
                draw.rounded_rectangle(
                    (x+i, y+i, width+i, height+i),
                    radius=10,
                    fill=None,
                    outline=(0, 0, 0, alpha))
        
        # Main window background - ultra-premium white
        draw.rounded_rectangle(
            (x, y, width, height),
            radius=8,
            fill=(245, 248, 250, 250))
        
        # Window title bar with premium gradient
        title_height = 30
        
        # Create gradient manually for ultra-premium look
        rgb_color = self._ensure_rgb_color(color)
        
        # Draw title bar
        draw.rounded_rectangle(
            (x, y, width, y+title_height),
            radius=8,
            fill=rgb_color)
        
        # Make sure bottom corners of title bar aren't rounded
        draw.rectangle(
            (x, y+title_height-8, width, y+title_height),
            fill=rgb_color)
        
        # Window title with shadow for depth
        text_color = (255, 255, 255)
        # Text shadow
        draw.text((x+11, y+9), title, fill=(0, 0, 0, 100))
        # Text
        draw.text((x+10, y+8), title, fill=text_color)
        
        # Window controls with premium style
        controls = [
            {"color": (255, 75, 75), "offset": 20},    # Close
            {"color": (255, 205, 65), "offset": 40},   # Minimize
            {"color": (80, 205, 75), "offset": 60},    # Maximize
        ]
        
        for control in controls:
            # Create control button with shadow for depth
            draw.ellipse(
                (width-control["offset"]-1, y+9, 
                 width-control["offset"]+13, y+23),
                fill=(0, 0, 0, 30))
                
            draw.ellipse(
                (width-control["offset"], y+8, 
                 width-control["offset"]+14, y+22),
                fill=control["color"])
                
            # Add highlight for 3D effect
            draw.arc(
                (width-control["offset"]+3, y+11, 
                 width-control["offset"]+11, y+19),
                start=0, end=180,
                fill=(255, 255, 255, 150))
        
        # Window content based on type
        if browser:
            self._draw_premium_browser_content(draw, x, y, width, height, title_height, url)
        elif game_window:
            self._draw_premium_game_content(draw, x, y, width, height, title_height)
        elif doc_window:
            self._draw_premium_document_content(draw, x, y, width, height, title_height)
        else:
            self._draw_premium_default_content(draw, x, y, width, height, title_height)
            
        return (x, y, width, height)
    
    def _draw_premium_browser_content(self, draw, x, y, width, height, title_height, url):
        """Draw premium browser content"""
        # Tab bar with premium styling
        tab_bar_height = 36
        tab_y = y + title_height
        
        # Tab bar background
        draw.rectangle(
            (x, tab_y, width, tab_y + tab_bar_height),
            fill=(235, 238, 240))
            
        # Active tab
        tab_width = 160
        draw.rounded_rectangle(
            (x+10, tab_y+4, x+10+tab_width, tab_y + tab_bar_height),
            radius=6,
            fill=(245, 248, 250))
            
        # Tab text
        draw.text(
            (x+25, tab_y+18),
            "Khan Academy",
            fill=(70, 80, 90))
            
        # Address bar with premium styling
        address_y = tab_y + tab_bar_height + 5
        address_height = 30
        
        # Address bar background
        draw.rounded_rectangle(
            (x+10, address_y, width-10, address_y + address_height),
            radius=15,
            fill=(240, 240, 240))
            
        # Security icon
        draw.ellipse(
            (x+20, address_y+8, x+28, address_y+22),
            fill=(80, 180, 80))
            
        # URL
        if url:
            draw.text(
                (x+35, address_y+15),
                url,
                fill=(40, 50, 60))
        
        # Content area
        content_y = address_y + address_height + 10
        
        # Header banner
        draw.rectangle(
            (x+10, content_y, width-10, content_y+60),
            fill=(2, 119, 189))
            
        draw.text(
            (x+30, content_y+30),
            "Khan Academy - Geometry Lesson",
            fill=(255, 255, 255))
            
        # Content boxes
        box_spacing = 15
        box_width = (width - x - 30) // 2 - box_spacing
        
        # Left content column
        left_x = x + 15
        
        # Navigation menu
        draw.rounded_rectangle(
            (left_x, content_y+70, left_x + box_width, content_y+200),
            radius=4,
            fill=(240, 240, 245))
            
        # Menu items
        menu_items = ["Home", "Courses", "Geometry", "Triangles", "Circles", "Quadrilaterals"]
        for i, item in enumerate(menu_items):
            item_y = content_y + 85 + i * 20
            
            # Highlight active item
            if i == 3:
                draw.rectangle(
                    (left_x+5, item_y-2, left_x + box_width-5, item_y+14),
                    fill=(220, 225, 255))
            
            draw.text(
                (left_x+15, item_y),
                item,
                fill=(60, 70, 80))
        
        # Right content - main area
        right_x = left_x + box_width + box_spacing
        
        # Main content box
        draw.rounded_rectangle(
            (right_x, content_y+70, right_x + box_width, content_y+240),
            radius=4,
            fill=(250, 250, 255))
            
        # Content title
        draw.text(
            (right_x+15, content_y+85),
            "Properties of Triangles",
            fill=(40, 50, 60))
            
        # Content text lines
        text_lines = ["A triangle is a polygon with", "three edges and three vertices.", 
                      "The sum of the angles in a", "triangle is 180 degrees."]
                      
        for i, line in enumerate(text_lines):
            draw.text(
                (right_x+15, content_y+110 + i*18),
                line,
                fill=(70, 80, 90))
                
        # Simple triangle diagram
        draw.polygon(
            [(right_x+60, content_y+190), 
             (right_x+120, content_y+190), 
             (right_x+90, content_y+150)],
            fill=(180, 200, 255),
            outline=(100, 120, 240))
    
    def _draw_premium_game_content(self, draw, x, y, width, height, title_height):
        """Draw premium game content"""
        content_y = y + title_height
        
        # Game background - dark texture
        draw.rectangle(
            (x, content_y, width, height),
            fill=(40, 50, 40))
            
        # Add texture pattern
        for i in range(0, width-x, 4):
            for j in range(0, height-content_y, 4):
                if (i + j) % 8 == 0:
                    draw.point(
                        (x + i, content_y + j),
                        fill=(30, 40, 30))
        
        # Game title
        title_y = content_y + 40
        
        # Title shadow
        draw.text(
            (x + (width-x)//2, title_y+2),
            "MINECRAFT",
            fill=(0, 0, 0, 150),
            anchor="mm")
            
        # Title text
        draw.text(
            (x + (width-x)//2, title_y),
            "MINECRAFT",
            fill=(220, 220, 220),
            anchor="mm")
            
        # Menu buttons
        buttons = [
            "Single Player", "Multiplayer", "Minecraft Marketplace", 
            "Options", "Quit Game"
        ]
        
        button_width = 200
        button_height = 36
        button_x = x + (width-x)//2 - button_width//2
        
        for i, text in enumerate(buttons):
            button_y = title_y + 70 + i * (button_height + 10)
            
            # Button shadow
            draw.rounded_rectangle(
                (button_x+2, button_y+2, button_x + button_width+2, button_y + button_height+2),
                radius=4,
                fill=(0, 0, 0, 100))
                
            # Button background
            draw.rounded_rectangle(
                (button_x, button_y, button_x + button_width, button_y + button_height),
                radius=4,
                fill=(60, 125, 60) if i == 0 else (80, 80, 80))
                
            # Button text
            draw.text(
                (button_x + button_width//2, button_y + button_height//2),
                text,
                fill=(240, 240, 240),
                anchor="mm")
                
        # Bottom text
        draw.text(
            (x + (width-x)//2, height - 20),
            "Copyright Mojang Studios",
            fill=(200, 200, 200),
            anchor="mm")
    
    def _draw_premium_document_content(self, draw, x, y, width, height, title_height):
        """Draw premium document content"""
        content_y = y + title_height
        
        # Toolbar
        toolbar_height = 30
        draw.rectangle(
            (x, content_y, width, content_y + toolbar_height),
            fill=(240, 240, 245))
            
        # Toolbar buttons
        tools = ["File", "Edit", "View", "Insert", "Format", "Tools", "Help"]
        current_x = x + 10
        
        for tool in tools:
            # Button text
            draw.text(
                (current_x, content_y + toolbar_height//2),
                tool,
                fill=(70, 80, 90),
                anchor="lm")
                
            # Update x position
            current_x += len(tool) * 8 + 15
            
        # Document content area
        doc_y = content_y + toolbar_height
        
        # Document background
        draw.rectangle(
            (x, doc_y, width, height),
            fill=(255, 255, 255))
            
        # Document title
        title_y = doc_y + 30
        draw.text(
            (x + 40, title_y),
            "Research Notes: Geometric Principles",
            fill=(20, 20, 20))
            
        # Horizontal rule
        draw.line(
            (x + 40, title_y + 20, width - 40, title_y + 20),
            fill=(200, 200, 200),
            width=1)
            
        # Document paragraphs
        para_y = title_y + 40
        
        paragraphs = [
            "The study of geometry involves understanding the properties,",
            "measurement, and relationships of points, lines, angles, surfaces,",
            "and solids. Key concepts include:",
            "",
            "1. Triangle properties - sum of angles equals 180 degrees",
            "2. Circle principles - all points equidistant from center",
            "3. Pythagorean theorem - relationship in right triangles",
            "",
            "Further research will explore applications in architecture and",
            "engineering, where these principles form the foundation of design."
        ]
        
        for i, para in enumerate(paragraphs):
            draw.text(
                (x + 40, para_y + i * 18),
                para,
                fill=(40, 40, 40))
                
        # Add document editor elements
        
        # Scrollbar
        scrollbar_width = 12
        draw.rectangle(
            (width - scrollbar_width, doc_y, width, height),
            fill=(240, 240, 245))
            
        # Scroll thumb
        draw.rounded_rectangle(
            (width - scrollbar_width + 2, doc_y + 20, width - 2, doc_y + 80),
            radius=3,
            fill=(180, 180, 190))
        
    def _draw_premium_default_content(self, draw, x, y, width, height, title_height):
        """Draw default premium window content"""
        content_y = y + title_height
        
        # Sidebar
        sidebar_width = 80
        draw.rectangle(
            (x, content_y, x + sidebar_width, height),
            fill=(245, 245, 250))
            
        # Sidebar icons
        icon_y_positions = [content_y + 20, content_y + 60, content_y + 100, content_y + 140]
        
        for i, pos_y in enumerate(icon_y_positions):
            # Icon background
            icon_color = (220, 220, 230) if i % 2 == 0 else (200, 200, 220)
            
            draw.rounded_rectangle(
                (x + 20, pos_y, x + 60, pos_y + 30),
                radius=4,
                fill=icon_color)
        
        # Main content
        content_x = x + sidebar_width
        
        # Grid of items
        grid_size = 70
        grid_margin = 15
        grid_cols = (width - content_x - grid_margin) // (grid_size + grid_margin)
        grid_rows = (height - content_y - grid_margin) // (grid_size + grid_margin)
        
        for row in range(grid_rows):
            for col in range(grid_cols):
                item_x = content_x + grid_margin + col * (grid_size + grid_margin)
                item_y = content_y + grid_margin + row * (grid_size + grid_margin)
                
                # Item background with slight variation
                hue_variation = (row * grid_cols + col) * 20 % 60
                
                # Item box
                draw.rounded_rectangle(
                    (item_x, item_y, item_x + grid_size, item_y + grid_size),
                    radius=4,
                    fill=(240 - hue_variation, 245, 250))
    
    def _ensure_rgb_color(self, color):
        """Convert hex color to RGB tuple if needed"""
        if isinstance(color, str) and color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            return (r, g, b)
        return color
    
    def start_ambient_animation(self):
        """Start sophisticated ambient animation effects for ultra-premium look and feel"""
        # Animation variables for smooth transitions
        self.animation_values = {
            "pulse_phase": 0,           # For connection indicator
            "activity_phase": 0,        # For activity meter
            "activity_width": 80,       # Base activity width
            "activity_target": 120,     # Target width
            "highlight_alpha": 0,       # For highlight effects
            "highlight_dir": 1,         # Direction of highlight change
            "notification_alpha": 0,    # For notification effects
            "notification_dir": 1,      # Direction of alpha change
            "scan_line_pos": 0,         # Position for scan line effect
            "meter_dots_opacity": 50,   # Opacity for activity dots
            "scanner_effect": 0,        # Scanner effect position
            "scanner_dir": 1,           # Scanner direction
            "glow_phase": 0,            # Phase for premium glow effects
            "pulse_colors": [           # Premium color palette for effects
                (37, 99, 235),          # Primary blue
                (14, 165, 233),         # Cyan blue
                (124, 58, 237),         # Purple
                (31, 80, 150)           # Deep blue
            ]
        }
        
        def update_animation():
            # Update animation phases
            self.animation_values["pulse_phase"] = (self.animation_values["pulse_phase"] + 0.04) % (2 * math.pi)
            self.animation_values["activity_phase"] = (self.animation_values["activity_phase"] + 0.03) % (2 * math.pi)
            self.animation_values["scan_line_pos"] = (self.animation_values["scan_line_pos"] + 1) % self.screen_height
            self.animation_values["glow_phase"] = (self.animation_values["glow_phase"] + 0.02) % (2 * math.pi)
            
            # Premium scanner effect
            self.animation_values["scanner_effect"] += 2 * self.animation_values["scanner_dir"]
            if self.animation_values["scanner_effect"] > 100:
                self.animation_values["scanner_dir"] = -1
            elif self.animation_values["scanner_effect"] < 0:
                self.animation_values["scanner_dir"] = 1
                
            # Add premium scanner effect to main screen
            if random.random() < 0.01:  # Occasionally show scanner
                scanner_pos = int(self.screen_area[0] + 
                               self.animation_values["scanner_effect"] / 100 * 
                               (self.screen_area[2] - self.screen_area[0]))
                
                # Create vertical scanner line
                scan_line = self.screen_canvas.create_line(
                    scanner_pos, self.screen_area[1],
                    scanner_pos, self.screen_area[3],
                    fill=f"#{37:02x}{99:02x}{235:02x}",
                    width=2,
                    stipple="gray50")
                    
                # Schedule deletion
                self.root.after(100, lambda line=scan_line: self.screen_canvas.delete(line))
            
            # More sophisticated pulse effect for connection indicator using dual sine waves
            pulse_size = 1.8 * math.sin(self.animation_values["pulse_phase"]) + 0.5 * math.sin(self.animation_values["pulse_phase"] * 2.3) + 1.0
            self.header_canvas.coords(
                self.connection_indicator,
                1050 - pulse_size, 35 - pulse_size, 
                1070 + pulse_size, 55 + pulse_size)
            
            # Advanced activity meter animation with easing
            # Calculate target based on time
            if random.random() < 0.01:  # Occasionally change the target
                self.animation_values["activity_target"] = random.randint(60, 160)
                
            # Smooth transition to target
            current = self.animation_values["activity_width"]
            target = self.animation_values["activity_target"]
            self.animation_values["activity_width"] += (target - current) * 0.05
            
            # Apply sine wave motion for more organic movement
            activity_width = self.animation_values["activity_width"] + 5 * math.sin(self.animation_values["activity_phase"])
            
            # Update meter position
            self.screen_canvas.coords(
                self.activity_meter,
                self.screen_width - 205, self.screen_height - 40,
                self.screen_width - 205 + activity_width, self.screen_height - 20)
                
            # Update highlight position to match
            self.screen_canvas.coords(
                self.activity_highlight,
                self.screen_width - 205, self.screen_height - 40,
                self.screen_width - 205 + activity_width, self.screen_height - 30)
            
            # Animate activity dots with pulsing effect
            dot_positions = [
                (self.screen_width - 185, "#DC2626", 0),      # Red
                (self.screen_width - 165, "#2563EB", 2.1),    # Blue with phase shift
                (self.screen_width - 145, "#0EA5E9", 4.2)     # Cyan with phase shift
            ]
            
            # Update dot opacities
            self.animation_values["meter_dots_opacity"] = 30 + int(20 * math.sin(self.animation_values["pulse_phase"]))
            
            for i, (x_pos, color, phase_shift) in enumerate(dot_positions):
                # Calculate individual pulse for each dot
                dot_pulse = math.sin(self.animation_values["pulse_phase"] + phase_shift) * 0.5 + 0.5
                
                # Pulse size based on activity level
                if i == 0:  # Red dot shows warning based on activity
                    dot_size = 2.5 + 1.5 * dot_pulse if activity_width > 120 else 2
                elif i == 1:  # Blue dot pulses on medium activity
                    dot_size = 2.5 + 1.5 * dot_pulse if 80 < activity_width <= 120 else 2
                else:  # Cyan dot pulses on low activity
                    dot_size = 2.5 + 1.5 * dot_pulse if activity_width <= 80 else 2
                
            # Ultra-premium screen border glow effect
            glow_color_idx = int(self.animation_values["glow_phase"] * 2) % len(self.animation_values["pulse_colors"])
            next_idx = (glow_color_idx + 1) % len(self.animation_values["pulse_colors"])
            
            # Interpolate between colors for smooth transition
            progress = (self.animation_values["glow_phase"] * 2) % 1.0
            r = int(self.animation_values["pulse_colors"][glow_color_idx][0] * (1-progress) + 
                    self.animation_values["pulse_colors"][next_idx][0] * progress)
            g = int(self.animation_values["pulse_colors"][glow_color_idx][1] * (1-progress) + 
                    self.animation_values["pulse_colors"][next_idx][1] * progress)
            b = int(self.animation_values["pulse_colors"][glow_color_idx][2] * (1-progress) + 
                    self.animation_values["pulse_colors"][next_idx][2] * progress)
            
            # Create subtle glow around screen
            if not hasattr(self, 'screen_glow'):
                # Create initial glow
                self.screen_glow = self.screen_canvas.create_rectangle(
                    self.screen_area[0] - 2, self.screen_area[1] - 2,
                    self.screen_area[2] + 2, self.screen_area[3] + 2,
                    outline=f"#{r:02x}{g:02x}{b:02x}",
                    width=2)
            else:
                # Update glow color
                self.screen_canvas.itemconfig(
                    self.screen_glow, 
                    outline=f"#{r:02x}{g:02x}{b:02x}")
            
            # Update scan line effect - subtle line that passes over the screen
            if self.animation_values["scan_line_pos"] % 200 < 30:
                scan_y = self.animation_values["scan_line_pos"] % 200
                scan_alpha = int(150 - scan_y * 5)
                if scan_alpha > 0:
                    # Create temporary scan line - use regular RGB without alpha
                    scan_line = self.screen_canvas.create_line(
                        self.screen_area[0], self.screen_area[1] + scan_y,
                        self.screen_area[2], self.screen_area[1] + scan_y,
                        fill=f"#{100:02x}{160:02x}{255:02x}",  # Removed alpha channel
                        width=1,
                        stipple=self._get_stipple_pattern(scan_alpha))  # Use stipple for transparency
                    # Schedule deletion
                    self.root.after(30, lambda line=scan_line: self.screen_canvas.delete(line))
            
            # Schedule next update
            self.root.after(30, update_animation)
        
        # Start animation
        update_animation()
    
    def _get_stipple_pattern(self, opacity):
        """Return appropriate stipple pattern based on opacity"""
        if opacity < 20:
            return "gray12"
        elif opacity < 40:
            return "gray25"
        elif opacity < 60:
            return "gray50"
        elif opacity < 80:
            return "gray75"
        else:
            return ""  # No stipple (solid)
    
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
        """Update applications list with modern premium cards"""
        # Clear existing app cards
        for widget in self.apps_container.winfo_children():
            widget.destroy()
        
        # Create cards for each app - premium design
        for i, window in enumerate(self.windows_list):
            # Create premium app card with glass effect
            card = tk.Frame(self.apps_container, bg=self.panel_bg, bd=0, 
                          highlightbackground=self.highlight_color, highlightthickness=1)
            card.pack(fill=tk.X, pady=6, padx=4)  # Better spacing
            
            # Add drop shadow effect
            shadow_frame = tk.Frame(card, bg=self.panel_bg, height=3)
            shadow_frame.pack(side=tk.BOTTOM, fill=tk.X)
            
            # Add inner frame with glass effect
            inner_frame = tk.Frame(card, bg=self.panel_bg, padx=4, pady=4)
            inner_frame.pack(fill=tk.BOTH, expand=True)
            
            # Add circular icon with premium styling
            icon_size = 40  # Slightly larger for premium look
            icon_canvas = tk.Canvas(inner_frame, width=icon_size, height=icon_size,
                                   bg=self.panel_bg, highlightthickness=0)
            icon_canvas.pack(side=tk.LEFT, padx=8, pady=4)  # Better spacing
            
            # Determine icon color based on app type - premium brand colors
            if "chrome" in window["process"].lower():
                icon_color = "#4285F4"  # Google blue
                accent_color = "#EA4335"  # Google red
                icon_letter = "C"
            elif "java" in window["process"].lower():
                icon_color = "#007396"  # Java blue
                accent_color = "#ED8B00"  # Java orange 
                icon_letter = "J"
            elif "discord" in window["process"].lower():
                icon_color = "#5865F2"  # Discord brand color
                accent_color = "#EB459E"  # Discord secondary
                icon_letter = "D"
            elif "minecraft" in window["title"].lower():
                icon_color = "#62B47A"  # Minecraft green
                accent_color = "#986C3C"  # Minecraft brown
                icon_letter = "M"
            elif "explorer" in window["process"].lower():
                icon_color = "#0078D7"  # Explorer blue
                accent_color = "#107C10"  # Windows green
                icon_letter = "E"
            elif "notepad" in window["process"].lower():
                icon_color = "#FFB900"  # Yellow
                accent_color = "#00B4F0"  # Cyan
                icon_letter = "N"
            else:
                icon_color = self.accent_primary
                accent_color = self.accent_tertiary
                icon_letter = window["process"][0].upper()
            
            # Draw premium icon with gradient effect and glow
            # Outer circle for glow
            icon_canvas.create_oval(0, 0, icon_size, icon_size, 
                                   fill="", outline=accent_color, width=1)
            
            # Main circle
            icon_canvas.create_oval(4, 4, icon_size-4, icon_size-4, 
                                   fill=icon_color, outline="")
            
            # Add app initial for better identification
            icon_canvas.create_text(icon_size//2, icon_size//2, 
                                   text=icon_letter, 
                                   fill="white", 
                                   font=self.subtitle_font)
            
            # Inner highlight for 3D effect
            icon_canvas.create_arc(8, 8, icon_size-8, icon_size-8, 
                                  start=45, extent=180, 
                                  outline="white", style="arc", width=1)
            
            # Add app info with better spacing
            info_frame = tk.Frame(inner_frame, bg=self.panel_bg)
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
            
            # App title - better font and styling
            title_label = tk.Label(info_frame, text=window["title"],
                                 font=self.normal_font, bg=self.panel_bg,
                                 fg=self.text_color, anchor="w", justify=tk.LEFT,
                                 padx=2, pady=2)
            title_label.pack(fill=tk.X, anchor="w", pady=(4, 1))
            
            # Process name - more refined styling
            process_frame = tk.Frame(info_frame, bg=self.panel_bg)
            process_frame.pack(fill=tk.X, anchor="w", pady=(0, 2))
            
            process_indicator = tk.Canvas(process_frame, width=6, height=6, 
                                        bg=self.panel_bg, highlightthickness=0)
            process_indicator.pack(side=tk.LEFT, padx=(0, 4), pady=2)
            process_indicator.create_oval(0, 0, 6, 6, fill=accent_color, outline="")
            
            process_label = tk.Label(process_frame, text=window["process"],
                                  font=self.small_font, bg=self.panel_bg,
                                  fg=self.secondary_text, anchor="w", justify=tk.LEFT)
            process_label.pack(side=tk.LEFT, fill=tk.X)
            
            # View button with modern styling
            view_button = ttk.Button(inner_frame, text="View", style="Accent.TButton",
                                   command=lambda wid=window["id"]: self.view_application(wid))
            view_button.pack(side=tk.RIGHT, padx=8, pady=6)
    
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
tk.Canvas.create_rounded_rectangle = create_rounded_rectangle
if __name__ == "__main__":
    root = tk.Tk()
    app = FuturisticParentMonitorApp(root)
    root.mainloop()
    