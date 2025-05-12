import socket
import pickle
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance, ImageFont
import threading
import io
import time
from tkinter import font as tkfont
from tkinter import ttk
import json
from datetime import datetime
import math
import random
from tkinter import messagebox

# Simple class to simulate object methods
class SimpleObject:
    """A simple class to simulate object methods for canvas objects."""
    pass

# Helper function to draw rounded rectangles on canvas
def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
    """Create a rounded rectangle on a canvas"""
    points = [
        x1+radius, y1,
        x1+radius, y1,
        x2-radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1+radius,
        x1, y1
    ]
    return self.create_polygon(points, **kwargs, smooth=True)

# Monkey-patch the Canvas class to add the create_rounded_rectangle method
tk.Canvas.create_rounded_rectangle = create_rounded_rectangle

class FuturisticParentMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OVERSIGHT - Child Activity Monitor")
        self.root.geometry("1320x800")  # Increased width from 1280 to 1320
        
        # Set up a sophisticated design system
        # A dual color scheme that supports both light and dark mode
        self.is_dark_mode = True  # Default to dark mode
        
        # Modern Color System
        self.setup_color_scheme()
        
        # Initialize view label text
        self.view_label_text = "Current View: None"
        
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
        
        # Set default current tab to 'apps' to prevent tab switching errors
        self.current_tab = "apps"
        
        # Load fonts for a more modern typography system
        self._load_fonts()
        
        # Configure styles for widgets
        self.configure_styles()
        
        # Create the main background with a subtle pattern
        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create a sophisticated background
        self.create_background()
        
        # Main container with shadow and inset
        self.main_frame = tk.Frame(self.canvas, bg=self.colors.bg)
        self.canvas.create_window(10, 10, anchor="nw", window=self.main_frame, width=1300, height=780)  # Increased width from 1260 to 1300
        
        # Create professional header with branding
        self.create_header()
        
        # Create main content area with elegant layout
        self.create_content_area()
        
        # Create control panel with modern inputs
        self.create_control_panel()
        
        # Initialize with sample applications
        self.sample_windows = {
            1: {"title": "Minecraft", "process": "javaw.exe", "id": 1, "category": "games", "icon": "🎮"},
            2: {"title": "Google Chrome", "process": "chrome.exe", "id": 2, "category": "web", "icon": "🌐"},
            3: {"title": "Discord", "process": "Discord.exe", "id": 3, "category": "social", "icon": "💬"},
            4: {"title": "Microsoft Word", "process": "WINWORD.exe", "id": 4, "category": "productivity", "icon": "📝"},
            5: {"title": "File Explorer", "process": "explorer.exe", "id": 5, "category": "system", "icon": "📁"}
        }
        
        # Sample browser history with categories
        self.sample_history = [
            {"time": "14:32:05", "url": "www.minecraft.net/community", "title": "Minecraft Community | Minecraft", "category": "games"},
            {"time": "14:28:12", "url": "www.google.com/search?q=minecraft+diamond+locations", "title": "minecraft diamond locations - Google Search", "category": "games"},
            {"time": "14:25:30", "url": "www.youtube.com/watch?v=dQw4w9WgXcQ", "title": "How to Beat Minecraft Fast - YouTube", "category": "video"},
            {"time": "14:15:22", "url": "www.google.com/search?q=homework+answers", "title": "homework answers - Google Search", "category": "education"},
            {"time": "14:10:15", "url": "www.roblox.com/games", "title": "Games - Roblox", "category": "games"},
            {"time": "13:58:40", "url": "www.discord.com", "title": "Discord | Your Place to Talk and Hang Out", "category": "social"},
            {"time": "13:45:12", "url": "www.google.com/search?q=math+homework+solver", "title": "math homework solver - Google Search", "category": "education"},
            {"time": "13:30:05", "url": "www.google.com", "title": "Google", "category": "web"}
        ]
        
        # Start UI animations and transitions
        self.start_animations()
        
        # After all UI elements are created, load sample data and start animations
        self.root.after(100, self.load_sample_data)
        self.root.after(100, self.animate_activity_meter)
        
        # Do not call update_status here as it causes errors
        # self.root.after(500, lambda: self.update_status("Ready to connect", "orange"))
    
    def setup_color_scheme(self):
        """Set up a sophisticated color system that supports light/dark mode with accent colors"""
        # Create a color object to hold all colors
        class ColorSystem:
            def __init__(self, is_dark):
                # Base colors
                if is_dark:
                    # Dark mode - refined with deeper colors and better contrast
                    self.bg = "#050A10"  # Even deeper blue-black background
                    self.surface = "#0E1620"  # Deeper surface color
                    self.surface_2 = "#161E2A"  # Secondary surface with better contrast
                    self.surface_3 = "#1F2738"  # Tertiary surface for even better distinction
                    self.border = "#2A3648"  # More visible border for better definition
                    self.text = "#FFFFFF"  # Crisp white text
                    self.text_secondary = "#A8BCDB"  # Brighter secondary text for better readability
                    self.text_tertiary = "#667A95"  # Better contrast for tertiary text
                    self.divider = "#242F42"  # More visible dividers
                else:
                    # Light mode - refined with better contrast
                    self.bg = "#F8FAFD"  # Slightly bluer background for better depth
                    self.surface = "#FFFFFF"  # Pure white surface
                    self.surface_2 = "#F0F5FB"  # Slightly more blue tint for better hierarchy
                    self.surface_3 = "#E6EDF7"  # More distinct tertiary surface
                    self.border = "#C2D0E0"  # Stronger border for better definition
                    self.text = "#0A1629"  # Deeper text color for better contrast
                    self.text_secondary = "#3C547A"  # Stronger secondary text
                    self.text_tertiary = "#6A83A5"  # Better contrast for tertiary text
                    self.divider = "#D5E0ED"  # More visible dividers
                
                # Accent colors - refined with better pairing and vibrancy
                self.primary = "#5D4FFF"  # Slightly more vibrant violet blue
                self.primary_hover = "#7A6DFF"  # Lighter hover with more luminosity
                self.primary_active = "#4A3CE8"  # Darker active state with better contrast
                
                self.secondary = "#FF3366"  # More vibrant pink-red
                self.secondary_hover = "#FF5C85"  # Brighter hover state
                self.secondary_active = "#E02E5A"  # Deeper active state
                
                self.success = "#1FD395"  # More vibrant teal
                self.success_hover = "#3EEBA9"  # Brighter hover state
                self.success_active = "#18BA85"  # Deeper active state
                
                self.info = "#00A1FF"  # More vibrant blue
                self.info_hover = "#33B6FF"  # Brighter hover state
                self.info_active = "#0086E6"  # Deeper active state
                
                self.warning = "#FFAC00"  # More vibrant amber
                self.warning_hover = "#FFBF33"  # Brighter hover state
                self.warning_active = "#E69A00"  # Deeper active state
                
                # App category colors - refined for better distinction
                self.category_games = "#FF7943"
                self.category_web = "#38B6FF"
                self.category_social = "#C159E6"
                self.category_productivity = "#4DCC95"
                self.category_system = "#FFCA3A"
                self.category_education = "#6979F8"
                self.category_video = "#FF6B99"
                self.category_other = "#8D9CAD"
                
                # Transparent colors with alpha
                self.overlay_light = "#FFFFFF33"  # Light overlay (20%)
                self.overlay_medium = "#00000066"  # Medium overlay (40%)
                self.overlay_dark = "#000000AA"  # Dark overlay (67%)
                
                # Shadow colors with better depth
                self.shadow_light = "#00000022"  # Light shadow
                self.shadow_medium = "#00000044"  # Medium shadow
                self.shadow_dark = "#00000066"  # Dark shadow
                
                # New glass effect colors
                self.glass_light = "#FFFFFF0A"  # Very subtle white overlay
                self.glass_medium = "#FFFFFF14"  # Medium white overlay
                self.glass_dark = "#FFFFFF1A"  # Stronger white overlay
                
                # Gradient endpoints for buttons and UI elements
                self.gradient_start = "#6A5CFF"  # Slightly more saturated
                self.gradient_end = "#5549E8"    # Deeper endpoint
        
        # Initialize color system based on mode
        self.colors = ColorSystem(self.is_dark_mode)
        
        # Legacy compatibility - map new color system to old variables 
        # This ensures backward compatibility with any code not yet updated
        self.bg_color = self.colors.bg
        self.secondary_bg = self.colors.surface
        self.panel_bg = self.colors.surface_2
        self.accent_primary = self.colors.primary
        self.accent_secondary = self.colors.secondary
        self.accent_tertiary = self.colors.info
        self.accent_quaternary = self.colors.warning
        self.text_color = self.colors.text
        self.secondary_text = self.colors.text_secondary
        self.border_color = self.colors.border
        self.highlight_color = self.colors.surface_3
    
    def _load_fonts(self):
        """Set up a sophisticated typography system with modern fonts and proper sizing"""
        try:
            # Primary font: Inter for UI elements (or system alternative)
            self.font_primary = "Inter, SF Pro Display, Segoe UI, Roboto, Arial"
            
            # Secondary font: SF Mono or alternative for code/data
            self.font_mono = "SF Mono, Menlo, Consolas, Monaco, monospace"
            
            # Title fonts for display text, headers
            self.title_large = tkfont.Font(family=self.font_primary, size=28, weight="bold")
            self.title = tkfont.Font(family=self.font_primary, size=20, weight="bold")
            self.title_small = tkfont.Font(family=self.font_primary, size=16, weight="bold")
            
            # Subtitle fonts
            self.subtitle = tkfont.Font(family=self.font_primary, size=14, weight="bold")
            self.subtitle_small = tkfont.Font(family=self.font_primary, size=12, weight="bold")
            
            # Body text fonts
            self.body_large = tkfont.Font(family=self.font_primary, size=14)
            self.body = tkfont.Font(family=self.font_primary, size=12)
            self.body_small = tkfont.Font(family=self.font_primary, size=11)
            
            # Caption and small text
            self.caption = tkfont.Font(family=self.font_primary, size=10)
            self.caption_small = tkfont.Font(family=self.font_primary, size=9)
            
            # Button font
            self.button = tkfont.Font(family=self.font_primary, size=12, weight="bold")
            self.button_small = tkfont.Font(family=self.font_primary, size=11, weight="bold")
            
            # Monospace fonts for code or data
            self.mono_regular = tkfont.Font(family=self.font_mono, size=12)
            self.mono_small = tkfont.Font(family=self.font_mono, size=11)
            
            # Pillow fonts for image generation (fallback to default)
            self.pil_title = ImageFont.load_default()
            self.pil_body = ImageFont.load_default()
            self.pil_caption = ImageFont.load_default()
            
        except Exception as e:
            print(f"Font loading error: {e}")
            # Fallback to system fonts
            self.title_large = tkfont.Font(size=28, weight="bold")
            self.title = tkfont.Font(size=20, weight="bold")
            self.title_small = tkfont.Font(size=16, weight="bold")
            self.subtitle = tkfont.Font(size=14, weight="bold")
            self.subtitle_small = tkfont.Font(size=12, weight="bold")
            self.body_large = tkfont.Font(size=14)
            self.body = tkfont.Font(size=12)
            self.body_small = tkfont.Font(size=11)
            self.caption = tkfont.Font(size=10)
            self.caption_small = tkfont.Font(size=9)
            self.button = tkfont.Font(size=12, weight="bold")
            self.button_small = tkfont.Font(size=11, weight="bold")
            self.mono_regular = tkfont.Font(family="Courier", size=12)
            self.mono_small = tkfont.Font(family="Courier", size=11)
            self.pil_title = ImageFont.load_default()
            self.pil_body = ImageFont.load_default()
            self.pil_caption = ImageFont.load_default()
        
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _get_font_path(self, font_name):
        """Attempt to find a font file path."""
        # This is a simplified example; a more robust solution would search system font directories
        # or use a library like matplotlib.font_manager
        font_map = {
            "Inter": "Inter.ttf", # Assuming Inter.ttf is in the same directory or a known path
            "JetBrains Mono": "JetBrainsMono.ttf" # Assuming JetBrainsMono.ttf is available
        }
        return font_map.get(font_name, None) # Return None if not found, PIL will use a default

    def _ensure_rgb_color(self, color):
        """Ensure color is in RGB format"""
        if isinstance(color, str) and color.startswith('#'):
            return self._hex_to_rgb(color)
        return color
        
    def configure_styles(self):
        """Configure custom styles with modern, refined styling"""
        style = ttk.Style()
        style.theme_use('clam')  # Base theme
        
        # Common button properties
        button_padding = (16, 10)
        button_font = self.button
        
        # Primary button - clean, elegant design
        style.configure("Primary.TButton",
                        font=button_font,
                        background=self.colors.primary,
                        foreground="white",
                        padding=button_padding,
                        borderwidth=0,
                        relief="flat")
        
        style.map("Primary.TButton",
                background=[('active', self.colors.primary_hover), ('pressed', self.colors.primary_active)],
                foreground=[('active', 'white'), ('pressed', 'white')],
                relief=[('pressed', 'flat'), ('!pressed', 'flat')])
        
        # Secondary/Danger button
        style.configure("Danger.TButton",
                        font=button_font,
                        background=self.colors.secondary,
                        foreground="white",
                        padding=button_padding,
                        borderwidth=0,
                        relief="flat")
        
        style.map("Danger.TButton",
                background=[('active', self.colors.secondary_hover), ('pressed', self.colors.secondary_active)],
                foreground=[('active', 'white'), ('pressed', 'white')],
                relief=[('pressed', 'flat'), ('!pressed', 'flat')])
        
        # Success button
        style.configure("Success.TButton",
                        font=button_font,
                        background=self.colors.success,
                        foreground="white",
                        padding=button_padding,
                        borderwidth=0,
                        relief="flat")
        
        style.map("Success.TButton",
                background=[('active', self.colors.success_hover), ('pressed', self.colors.success_active)],
                foreground=[('active', 'white'), ('pressed', 'white')],
                relief=[('pressed', 'flat'), ('!pressed', 'flat')])
        
        # Info button
        style.configure("Info.TButton",
                        font=button_font,
                        background=self.colors.info,
                        foreground="white",
                        padding=button_padding,
                        borderwidth=0,
                        relief="flat")
        
        style.map("Info.TButton",
                background=[('active', self.colors.info_hover), ('pressed', self.colors.info_active)],
                foreground=[('active', 'white'), ('pressed', 'white')],
                relief=[('pressed', 'flat'), ('!pressed', 'flat')])
                
        # Outline Primary button
        style.configure("OutlinePrimary.TButton",
                        font=button_font,
                        background=self.colors.surface,
                        foreground=self.colors.primary,
                        padding=button_padding,
                        borderwidth=1,
                        relief="flat")
        
        style.map("OutlinePrimary.TButton",
                background=[('active', self.colors.overlay_light), ('pressed', self.colors.overlay_light)],
                foreground=[('active', self.colors.primary_hover), ('pressed', self.colors.primary_active)],
                relief=[('pressed', 'flat'), ('!pressed', 'flat')])
        
        # Ghost button - transparent with text only
        style.configure("Ghost.TButton",
                        font=button_font,
                        background=self.colors.surface,
                        foreground=self.colors.text_secondary,
                        padding=button_padding,
                        borderwidth=0,
                        relief="flat")
        
        style.map("Ghost.TButton",
                background=[('active', self.colors.surface_2), ('pressed', self.colors.surface_3)],
                foreground=[('active', self.colors.text), ('pressed', self.colors.text)],
                relief=[('pressed', 'flat'), ('!pressed', 'flat')])
                
        # Large buttons
        style.configure("Large.Primary.TButton",
                        font=self.title_small,
                        padding=(20, 12))
                
        # Small buttons
        style.configure("Small.Primary.TButton",
                        font=self.body_small,
                        padding=(10, 6))
        
        # Icon buttons
        style.configure("Icon.TButton",
                        font=self.body,
                        background=self.colors.surface,
                        foreground=self.colors.text_secondary,
                        padding=(8, 8),
                        borderwidth=0,
                        relief="flat")
                
        style.map("Icon.TButton",
                background=[('active', self.colors.surface_2), ('pressed', self.colors.surface_3)],
                foreground=[('active', self.colors.text), ('pressed', self.colors.text)],
                relief=[('pressed', 'flat'), ('!pressed', 'flat')])
        
        # Round buttons
        # Note: we'll implement these with Canvas for proper rounding
        
        # Treeview for lists - clean, modern style
        style.configure("Treeview",
                        background=self.colors.surface,
                        foreground=self.colors.text,
                        fieldbackground=self.colors.surface,
                        borderwidth=0,
                        rowheight=44)  # Taller rows for a more spacious look
        
        style.map("Treeview",
                background=[('selected', self.colors.surface_3)],
                foreground=[('selected', self.colors.text)])
        
        style.configure("Treeview.Heading",
                        background=self.colors.surface_2,
                        foreground=self.colors.text_secondary,
                        relief="flat",
                        font=self.subtitle_small,
                        padding=(12, 10))
        
        # Entry styling - clean, elegant inputs
        style.configure("TEntry",
                        background=self.colors.surface,
                        foreground=self.colors.text,
                        fieldbackground=self.colors.surface,
                        insertcolor=self.colors.primary,
                        borderwidth=1,
                        bordercolor=self.colors.border,
                        padding=12)
        
        style.map("TEntry",
                bordercolor=[('focus', self.colors.primary), ('active', self.colors.border)],
                fieldbackground=[('focus', self.colors.surface), ('active', self.colors.surface)],
                relief=[('focus', 'flat'), ('active', 'flat')])
        
        # Scrollbar styling - thin, elegant scrollbars
        scrollbar_width = 8
        style.configure("Vertical.TScrollbar",
                        background=self.colors.surface_2,
                        troughcolor=self.colors.surface,
                        gripcount=0,
                        arrowcolor=self.colors.text_tertiary,
                        bordercolor=self.colors.surface,
                        width=scrollbar_width)
        
        style.map("Vertical.TScrollbar",
                  background=[('active', self.colors.surface_3), ('!disabled', self.colors.surface_2)],
                  arrowcolor=[('active', self.colors.text_secondary), ('!disabled', self.colors.text_tertiary)])
        
        style.configure("Horizontal.TScrollbar",
                        background=self.colors.surface_2,
                        troughcolor=self.colors.surface,
                        gripcount=0,
                        arrowcolor=self.colors.text_tertiary,
                        bordercolor=self.colors.surface,
                        height=scrollbar_width)
        
        style.map("Horizontal.TScrollbar",
                  background=[('active', self.colors.surface_3), ('!disabled', self.colors.surface_2)],
                  arrowcolor=[('active', self.colors.text_secondary), ('!disabled', self.colors.text_tertiary)])
        
        # Tabs styling
        style.configure("TNotebook",
                        background=self.colors.surface,
                        borderwidth=0)
        
        style.configure("TNotebook.Tab",
                        background=self.colors.surface,
                        foreground=self.colors.text_tertiary,
                        borderwidth=0,
                        padding=(16, 8),
                        font=self.body_small)
        
        style.map("TNotebook.Tab",
                background=[('selected', self.colors.surface), ('active', self.colors.surface_2)],
                foreground=[('selected', self.colors.primary), ('active', self.colors.text_secondary)],
                expand=[('selected', [1, 1, 1, 0])])
    
    def create_background(self):
        """Create a sophisticated background with subtle pattern and glow effects"""
        width, height = 1320, 800  # Updated width from 1280 to 1320
        background = Image.new('RGBA', (width, height), self._hex_to_rgb(self.colors.bg) + (255,))
        draw = ImageDraw.Draw(background)
        
        # Create a subtle gradient overlay
        for y in range(height):
            # Calculate gradient opacity - stronger at top, fading toward bottom
            opacity = int(20 - (y / height) * 15)
            if opacity > 0:
                draw.line([(0, y), (width, y)], fill=self._hex_to_rgb(self.colors.surface) + (opacity,))
        
        # Add subtle grid pattern for a tech feel
        grid_spacing = 40
        grid_color = self._hex_to_rgb(self.colors.border) + (15,)  # Very subtle grid
        
        # Draw grid with dotted lines for a more refined look
        for x in range(0, width, grid_spacing):
            for y in range(0, height, 3):  # Draw dots every 3 pixels
                if y % 6 == 0:  # Skip every other dot for dotted line effect
                    draw.point((x, y), fill=grid_color)
        
        for y in range(0, height, grid_spacing):
            for x in range(0, width, 3):  # Draw dots every 3 pixels
                if x % 6 == 0:  # Skip every other dot for dotted line effect
                    draw.point((x, y), fill=grid_color)
        
        # Add subtle glow in top corners
        glow_size = 400
        glow_color = self._hex_to_rgb(self.colors.primary) + (0,)  # Start with transparent
        
        # Top left glow
        for i in range(glow_size, 0, -1):
            # Decreasing opacity as radius increases
            opacity = int(10 - i * 0.025)
            if opacity <= 0:
                continue
                
            glow_color_with_opacity = self._hex_to_rgb(self.colors.primary) + (opacity,)
            draw.ellipse([-i, -i, i, i], fill=glow_color_with_opacity)
        
        # Top right glow with secondary color
        for i in range(glow_size, 0, -1):
            opacity = int(10 - i * 0.025)
            if opacity <= 0:
                continue
                
            glow_color_with_opacity = self._hex_to_rgb(self.colors.secondary) + (opacity,)
            draw.ellipse([width - i, -i, width + i, i], fill=glow_color_with_opacity)
        
        # Convert and display
        self.bg_photo = ImageTk.PhotoImage(background)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        
    def create_shadow_image(self, width, height, radius=20, alpha=100):
        """Create a shadow image for adding depth to UI elements"""
        shadow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(shadow)
        
        # Draw rounded rectangle with semi-transparent black
        draw.rounded_rectangle([0, 0, width, height], radius=radius, fill=(0, 0, 0, alpha))
        
        # Apply gaussian blur
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius // 2))
        
        return shadow
    
    def create_frosted_panel(self, width, height, radius=15, opacity=230):
        """Create a frosted glass panel effect for modern UI"""
        panel = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(panel)
        
        # Base panel color with transparency
        panel_color = self._hex_to_rgb(self.colors.surface) + (opacity,)
        draw.rounded_rectangle([0, 0, width, height], radius=radius, fill=panel_color)
        
        # Add subtle highlight at top
        highlight_color = (255, 255, 255, 30)  # Very subtle white highlight
        draw.rounded_rectangle([1, 1, width-1, height//4], radius=radius, fill=None, outline=highlight_color)
        
        # Add subtle inner shadow at bottom
        shadow_color = (0, 0, 0, 20)  # Very subtle shadow
        draw.rounded_rectangle([2, height-height//4, width-2, height-2], radius=radius, fill=None, outline=shadow_color)
        
        return panel
    
    def start_animations(self):
        """Initialize and start UI animations"""
        # Animation properties
        self.animation_speed = 1.0  # Speed multiplier (1.0 = normal)
        self.animations = {}  # Store running animations
        
        # Setup animation tick
        self.last_frame_time = time.time()
        self.root.after(16, self.animation_tick)  # ~60fps
    
    def animation_tick(self):
        """Main animation loop"""
        current_time = time.time()
        dt = (current_time - self.last_frame_time) * self.animation_speed
        self.last_frame_time = current_time
        
        # Process all active animations
        animations_to_remove = []
        for anim_id, anim in self.animations.items():
            # Update animation progress
            anim['progress'] += dt / anim['duration']
            
            # Check if animation is complete
            if anim['progress'] >= 1.0:
                # Run completion callback if provided
                if anim['on_complete']:
                    anim['on_complete']()
                animations_to_remove.append(anim_id)
                continue
                
            # Calculate eased value
            eased_progress = self.ease_value(anim['progress'], anim['easing'])
            
            # Calculate current value
            if isinstance(anim['start'], (int, float)) and isinstance(anim['end'], (int, float)):
                current_value = anim['start'] + (anim['end'] - anim['start']) * eased_progress
            elif isinstance(anim['start'], tuple) and isinstance(anim['end'], tuple) and len(anim['start']) == len(anim['end']):
                # Handle tuple values (like coordinates)
                current_value = tuple(s + (e - s) * eased_progress for s, e in zip(anim['start'], anim['end']))
            else:
                current_value = anim['end'] if eased_progress > 0.5 else anim['start']
            
            # Update via callback
            anim['on_update'](current_value)
        
        # Remove completed animations
        for anim_id in animations_to_remove:
            del self.animations[anim_id]
        
        # Schedule next frame
        self.root.after(16, self.animation_tick)
    
    def animate(self, target_id, start, end, duration, on_update, easing="ease_out_quad", on_complete=None):
        """Start a new animation"""
        self.animations[target_id] = {
            'start': start,
            'end': end,
            'duration': duration,
            'progress': 0.0,
            'easing': easing,
            'on_update': on_update,
            'on_complete': on_complete
        }
        
    def ease_value(self, progress, easing_type):
        """Apply easing function to a progress value (0.0 to 1.0)"""
        if easing_type == "linear":
            return progress
        elif easing_type == "ease_in_quad":
            return progress * progress
        elif easing_type == "ease_out_quad":
            return 1 - (1 - progress) * (1 - progress)
        elif easing_type == "ease_in_out_quad":
            return 0.5 * (math.sin((progress - 0.5) * math.pi) + 1)
        elif easing_type == "ease_in_cubic":
            return progress * progress * progress
        elif easing_type == "ease_out_cubic":
            return 1 - math.pow(1 - progress, 3)
        elif easing_type == "ease_out_back":
            c1 = 1.70158
            c3 = c1 + 1
            return 1 + c3 * math.pow(progress - 1, 3) + c1 * math.pow(progress - 1, 2)
        elif easing_type == "ease_in_out_back":
            c1 = 1.70158
            c2 = c1 * 1.525
            if progress < 0.5:
                return (2 * progress * progress * ((c2 + 1) * 2 * progress - c2)) / 2
            else:
                return (2 * math.pow(progress - 0.5, 2) * ((c2 + 1) * 2 * (progress - 0.5) + c2) + 1) / 2
        else:
            return progress  # Default to linear
    
    def show_welcome_screen(self):
        """Show animated welcome screen overlay"""
        # Create a full-screen overlay
        overlay_frame = tk.Frame(self.root, bg=self.colors.bg)
        overlay_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Logo and welcome text with animations
        logo_canvas = tk.Canvas(overlay_frame, bg=self.colors.bg, highlightthickness=0, width=200, height=200)
        logo_canvas.place(relx=0.5, rely=0.4, anchor="center")
        
        # Draw logo
        self.draw_logo(logo_canvas, 100, 100, size=100)
        
        # Welcome text with typing animation
        welcome_label = tk.Label(
            overlay_frame, 
            text="", 
            font=self.title, 
            fg=self.colors.primary, 
            bg=self.colors.bg
        )
        welcome_label.place(relx=0.5, rely=0.55, anchor="center")
        
        subtitle_label = tk.Label(
            overlay_frame, 
            text="", 
            font=self.body_large, 
            fg=self.colors.text_secondary, 
            bg=self.colors.bg
        )
        subtitle_label.place(relx=0.5, rely=0.61, anchor="center")
        
        # Progress bar
        progress_bg = tk.Frame(overlay_frame, bg=self.colors.surface_2, width=300, height=4)
        progress_bg.place(relx=0.5, rely=0.7, anchor="center", width=300)
        
        progress_bar = tk.Frame(overlay_frame, bg=self.colors.primary, width=0, height=4)
        progress_bar.place(relx=0.5, rely=0.7, anchor="center", width=0)
        
        # Typing animation for welcome message
        welcome_text = "OVERSIGHT"
        subtitle_text = "Advanced Activity Monitoring System"
        
        def update_text(i):
            if i <= len(welcome_text):
                welcome_label.config(text=welcome_text[:i])
                self.root.after(80, lambda: update_text(i+1))
            elif i <= len(welcome_text) + len(subtitle_text):
                subtitle_idx = i - len(welcome_text)
                subtitle_label.config(text=subtitle_text[:subtitle_idx])
                self.root.after(40, lambda: update_text(i+1))
        
        # Start text animation
        self.root.after(500, lambda: update_text(0))
        
        # Animate progress bar
        def update_progress_bar(width):
            progress_bar.place(width=width)
        
        self.root.after(1000, lambda: self.animate(
            "progress_bar", 0, 300, 2.0, 
            update_progress_bar, "ease_in_out_quad",
            lambda: self.root.after(500, lambda: self.fade_out_overlay(overlay_frame))
        ))
    
    def fade_out_overlay(self, overlay):
        """Fade out and remove an overlay"""
        alpha = 1.0
        
        def update_alpha(new_alpha):
            nonlocal alpha
            alpha = new_alpha
            # Convert alpha to hex transparency for tkinter
            alpha_hex = int(alpha * 255)
            overlay.configure(bg=f"#{self.colors.bg[1:]}{'%02x' % alpha_hex}")
            
            if alpha <= 0:
                overlay.destroy()
        
        self.animate("overlay_fade", 1.0, 0.0, 0.8, update_alpha, "ease_in_out_quad")
    
    def draw_logo(self, canvas, x, y, size=100):
        """Draw the application logo"""
        radius = size // 2
        
        # Outer circle with gradient
        for i in range(radius, 0, -1):
            # Create gradient from primary to secondary color
            progress = i / radius
            r = int(int(self.colors.primary[1:3], 16) * progress + int(self.colors.secondary[1:3], 16) * (1-progress))
            g = int(int(self.colors.primary[3:5], 16) * progress + int(self.colors.secondary[3:5], 16) * (1-progress))
            b = int(int(self.colors.primary[5:7], 16) * progress + int(self.colors.secondary[5:7], 16) * (1-progress))
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            canvas.create_oval(
                x - i, y - i,
                x + i, y + i,
                outline=color, width=2 if i % 5 == 0 else 1
            )
        
        # Inner eye symbol
        eye_size = radius * 0.6
        canvas.create_oval(
            x - eye_size, y - eye_size,
            x + eye_size, y + eye_size,
            outline=self.colors.primary, width=3
        )
        
        # Pupil
        pupil_size = eye_size * 0.4
        canvas.create_oval(
            x - pupil_size, y - pupil_size,
            x + pupil_size, y + pupil_size,
            fill=self.colors.primary, outline=""
        )
        
        # Eyelid
        canvas.create_arc(
            x - eye_size, y - eye_size,
            x + eye_size, y + eye_size,
            start=0, extent=-180,
            style=tk.ARC, outline=self.colors.primary, width=3
        )
        
        # Add gleam
        gleam_size = pupil_size * 0.4
        canvas.create_oval(
            x - pupil_size * 0.3 - gleam_size, 
            y - pupil_size * 0.3 - gleam_size,
            x - pupil_size * 0.3 + gleam_size, 
            y - pupil_size * 0.3 + gleam_size,
            fill="white", outline=""
        )
    
    def create_header(self):
        """Create sleek header bar with modern minimal styling"""
        # Header frame
        self.header_height = 70
        self.header_frame = tk.Frame(self.main_frame, bg=self.secondary_bg)
        self.header_frame.pack(fill=tk.X)
        self.header_frame.pack_propagate(False)
        
        # Header canvas for design
        self.header_canvas = tk.Canvas(self.header_frame, 
                                     highlightthickness=0, 
                                     bg=self.secondary_bg,
                                     height=self.header_height)
        self.header_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create modern header
        self.draw_sleek_header()
        
        # App title in header
        self.header_canvas.create_text(40, 35, 
                                     text="GUARDIAN", 
                                     font=self.title, 
                                     fill=self.accent_primary, 
                                     anchor="w")
        
        self.header_canvas.create_text(160, 35, 
                                      text="Code & Activity Monitor", 
                                      font=self.body, 
                                      fill=self.secondary_text, 
                                      anchor="w")
        
        # Status indicator in header - redesigned for modern look
        # Create a sleeker status pill
        status_pill_width = 120
        status_pill_height = 30
        
        # Create rounded pill background
        self.status_pill = self.header_canvas.create_rounded_rectangle(
            1050, 35 - status_pill_height//2,
            1050 + status_pill_width, 35 + status_pill_height//2,
            radius=15,
            fill=self.secondary_bg,
            outline=self.border_color,
            width=1)
        
        # Add status indicator dot
        self.connection_indicator = self.header_canvas.create_oval(
            1060, 35-5, 1070, 35+5, 
                                                                fill=self.accent_secondary, 
                                                                outline="")
        
        # Add subtle glow effect to indicator
        self.header_canvas.create_oval(
            1059, 34, 1071, 36+4, 
                                     fill="", 
                                     outline=self.accent_secondary, 
            width=1)
        
        # Status text
        self.status_var = tk.StringVar()
        self.status_var.set("Disconnected")
        self.status_text = self.header_canvas.create_text(
            1085, 35, 
                                                       text=self.status_var.get(), 
                                                       font=self.body, 
            fill=self.text_color, 
                                                       anchor="w")
    
    def draw_sleek_header(self):
        """Draw sleek header with minimal styling similar to Cursor"""
        # width = self.root.winfo_width() if self.root.winfo_width() > 100 else 1280
        # The header_canvas should take the width of its frame, which is packed to X
        width = self.header_canvas.winfo_width()
        if width <= 1: width = 1280 # Fallback if canvas not rendered

        height = self.header_height
        
        # Create header image with dark theme - using self.secondary_bg as base
        header_base_color_rgb = self._ensure_rgb_color(self.secondary_bg)
        header_img = Image.new('RGBA', (width, height), header_base_color_rgb + (255,)) # Solid base
        draw = ImageDraw.Draw(header_img)
        
        # No complex gradient needed if we want a flat, sleek header like modern apps.
        # A subtle top highlight or bottom border is usually enough.

        # Add subtle border line at bottom for separation
        border_color_rgb = self._ensure_rgb_color(self.border_color)
        draw.line(
            [(0, height - 1), (width, height - 1)], 
            fill=border_color_rgb + (150,), # Slightly transparent 
            width=1
        )
        
        # Convert to PhotoImage
        self.header_photo = ImageTk.PhotoImage(header_img)
        
        # Display header
        # Ensure this item is tagged or stored if it needs to be updated/deleted
        if hasattr(self, 'header_bg_item') and self.header_bg_item:
            self.header_canvas.itemconfig(self.header_bg_item, image=self.header_photo)
        else:
            self.header_bg_item = self.header_canvas.create_image(0, 0, image=self.header_photo, anchor="nw")
    
    def create_content_area(self):
        """Create main content area with screen view and apps list"""
        # Content frame
        self.content_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel for screen view - adjusted to give more space to right panel
        self.create_screen_panel()
        
        # Right panel for applications and tabs
        self.create_apps_panel()
    
    def create_screen_panel(self):
        """Create left panel for screen view"""
        # Screen panel - left side (70% width)
        self.screen_panel = tk.Frame(self.content_frame, bg=self.bg_color)
        self.screen_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))  # Increased right padding
        
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
                                     font=self.subtitle, 
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
                                                      font=self.body, 
                                                      fill="white", 
                                                      anchor="w")
        
        # Activity meter
        self.draw_activity_meter()
    
    def draw_activity_meter(self):
        """Draw activity meter with sleek, modern styling"""
        # Calculate meter dimensions
        meter_width = 160
        meter_height = 18
        x_pos = self.screen_width - meter_width - 40
        y_pos = self.screen_height - 35
        
        # Background for the meter - sleek dark
        self.screen_canvas.create_rounded_rectangle(
            x_pos, y_pos, 
            x_pos + meter_width, y_pos + meter_height,
            radius=9, 
            fill="#1C212B",  # Slightly lighter than background
            outline=self.border_color,
            width=1)
        
        # Active part of the meter (will be updated)
        self.activity_meter = self.screen_canvas.create_rounded_rectangle(
            x_pos, y_pos,
            x_pos + meter_width//2, y_pos + meter_height,
            radius=9,
            fill=self.accent_primary,  # Purple accent
            outline="")
            
        # Create glow effect like cursor
        glow_width = 3
        self.screen_canvas.create_rounded_rectangle(
            x_pos - glow_width, y_pos - glow_width,
            x_pos + meter_width//2 + glow_width, y_pos + meter_height + glow_width,
            radius=12,
            fill="",
            outline=self.accent_primary,
            width=1,
            stipple="gray12")  # Very subtle glow
        
        # Status label - clean and modern
        self.screen_canvas.create_text(
            x_pos - 10, y_pos + meter_height//2,
            text="ACTIVITY", 
            font=self.caption, # Replace small_font_tk
            fill=self.text_color,
            anchor="e")
        
        # Status indicators - minimal dots with labels
        status_colors = [
            {"color": self.accent_secondary, "label": "HIGH"},   # Red for high activity
            {"color": self.accent_primary, "label": "MED"},      # Purple for medium
            {"color": self.accent_tertiary, "label": "LOW"}      # Cyan for low
        ]
        
        for i, status in enumerate(status_colors):
            # Position indicators on the right side of the meter
            dot_x = x_pos + meter_width + 15
            dot_y = y_pos + (i * 6) + 3
            
            # Create indicator dot - smaller for modern look
            self.screen_canvas.create_oval(
                dot_x, dot_y, dot_x + 3, dot_y + 3,
                fill=status["color"], outline="")
            
            # Add label - smaller and more subtle
            self.screen_canvas.create_text(
                dot_x + 12, dot_y + 2,
                text=status["label"],
                font=self.caption, # Replace small_font_tk
                fill=self.secondary_text,
                anchor="w")
    
    def draw_screen_panel(self):
        """Draw screen panel with sleek, modern styling"""
        # Get panel dimensions
        self.screen_width = self.screen_panel.winfo_width() 
        if self.screen_width < 100:
            self.screen_width = 800  # Default width if not yet rendered
            
        self.screen_height = self.screen_panel.winfo_height()
        if self.screen_height < 100:
            self.screen_height = 600 # Default height if not yet rendered
        
        # Create dark panel
        panel_img = Image.new('RGBA', (self.screen_width, self.screen_height), (0,0,0,0)) # Transparent base
        draw = ImageDraw.Draw(panel_img)
        
        # Main panel background - use self.secondary_bg for slight contrast with main bg_color
        panel_bg_rgb = self._ensure_rgb_color(self.secondary_bg) 
        border_color_rgb = self._ensure_rgb_color(self.border_color)
        screen_area_bg_rgb = self._ensure_rgb_color(self.bg_color) # Darker for the actual screen content area
        
        # Add subtle shadow for depth - draw it first so it appears behind the panel
        shadow_color = (0, 0, 0, 40)  # Very transparent black
        shadow_offset = 10
        shadow_blur = 15
        
        # Draw shadow as multiple semi-transparent rectangles with decreasing opacity
        for i in range(shadow_blur):
            opacity = int(20 - i * 1.5)  # Decreasing opacity for fade effect
            if opacity <= 0:
                continue
                
            shadow_rect = (
                shadow_offset - i, 
                shadow_offset - i, 
                self.screen_width - shadow_offset + i, 
                self.screen_height - shadow_offset + i
            )
            draw.rounded_rectangle(
                shadow_rect,
                radius=10 + i,  # Increasing radius for blur effect
                fill=(0, 0, 0, opacity)
            )
            
        # Draw the main panel shape with rounded corners
        draw.rounded_rectangle(
            (0, 0, self.screen_width, self.screen_height), 
            radius=10,  # Consistent rounded corners, slightly larger for main panels
            fill=panel_bg_rgb + (250,)) # Main panel bg
        
        # Title bar - integrated into the panel, slightly darker than panel_bg_rgb
        title_bar_height = 40 # Increased height for better visual balance
        title_bar_color = (max(0,panel_bg_rgb[0]-10), max(0,panel_bg_rgb[1]-10), max(0,panel_bg_rgb[2]-10)) # Darker shade
        
        # Draw title bar area (only top part needs to be explicitly drawn if it differs)
        # We can achieve the effect by drawing the main panel and then the content area
        # For a distinct title bar, we can overlay it.
        # Let's draw it as a rounded rectangle at the top, matching top corners
        draw.rounded_rectangle(
            (0, 0, self.screen_width, title_bar_height),
            radius=10, # Match main panel radius
            fill=title_bar_color + (250,)
        )
        # Correct bottom corners of title bar to be square if it's visually distinct like a separate bar
        draw.rectangle(
            (0, title_bar_height - 10, self.screen_width, title_bar_height),
            fill=title_bar_color + (250,)
        )

        # Bottom status bar - similar to title bar
        status_bar_height = 40 # Increased height
        # For symmetry, let's ensure the status bar is also a rounded rect at the bottom
        draw.rounded_rectangle(
            (0, self.screen_height - status_bar_height, self.screen_width, self.screen_height),
            radius=10, # Match main panel radius
            fill=title_bar_color + (250,) # Same darker shade as title bar
        )
        draw.rectangle(
            (0, self.screen_height - status_bar_height, self.screen_width, self.screen_height - status_bar_height + 10),
            fill=title_bar_color + (250,)
        )        

        # Main screen area - inset dark look like code editor
        # Reduced margins for better positioning - fix for the padding issue
        screen_margin = 5  # Reduced from 15 to 5
        self.screen_area = (
            screen_margin, 
            title_bar_height + screen_margin, # Adjusted for new title bar height and look
            self.screen_width - screen_margin, 
            self.screen_height - status_bar_height - screen_margin # Adjusted for new status bar height
        )
        
        # Inner shadow for screen area - adds depth
        inner_shadow_color = (0, 0, 0, 25)
        inner_shadow_width = 6
        for i in range(inner_shadow_width):
            opacity = int(25 - i * 4)  # Decreasing opacity
            if opacity <= 0:
                continue
                
            inset = i
            draw.rounded_rectangle(
                (self.screen_area[0] + inset, self.screen_area[1] + inset,
                 self.screen_area[2] - inset, self.screen_area[3] - inset),
                radius=6 - inset if 6 - inset > 0 else 1,
                fill=None,
                outline=(0, 0, 0, opacity),
                width=1
            )
            
        # Screen viewing area with a very subtle inner border/shadow to give depth
        draw.rounded_rectangle(
            self.screen_area,
            radius=6, # Smaller radius for content area
            fill=screen_area_bg_rgb + (255,),  # Use the darkest bg_color for content
            outline=border_color_rgb + (80,), # Subtle border for the content area
            width=1
        )
        
        # Add subtle border outline for the main panel itself
        draw.rounded_rectangle(
            (0, 0, self.screen_width, self.screen_height),
            radius=10,
            fill=None, # Transparent fill
            outline=border_color_rgb + (100,), # Slightly more visible border for the panel
            width=1)
            
        # Add subtle highlight at the top edge for a glossy effect
        for i in range(3):
            highlight_opacity = 15 - i * 5
            if highlight_opacity <= 0:
                continue
                
            draw.rounded_rectangle(
                (i, i, self.screen_width - i, title_bar_height // 2),
                radius=10,
                fill=None,
                outline=(255, 255, 255, highlight_opacity),
                width=1
            )
        
        # Convert to PhotoImage
        self.screen_frame_img = ImageTk.PhotoImage(panel_img)
        
        # Display on canvas
        if hasattr(self, 'screen_frame') and self.screen_frame:
            self.screen_canvas.itemconfig(self.screen_frame, image=self.screen_frame_img)
        else:
            self.screen_frame = self.screen_canvas.create_image(
                0, 0, image=self.screen_frame_img, anchor="nw")
        
        # Screen title - modern minimal
        # Ensure text is on top of the drawn panel
        # If existing, delete and redraw or use itemconfig. For simplicity, ensure it's called after panel drawing.
        if hasattr(self, 'screen_title_text') and self.screen_title_text:
            self.screen_canvas.delete(self.screen_title_text)
        self.screen_title_text = self.screen_canvas.create_text(
            25, title_bar_height // 2, # Adjusted padding
            text="LIVE MONITORING", 
            font=self.subtitle, # Replace subtitle_font_tk
            fill=self.accent_tertiary, 
            anchor="w")
        
        # Add minimalist control dots - cleaner style
        control_colors = [
            (self.accent_secondary, "close"),
            (self.accent_quaternary, "min"),
            (self.accent_tertiary, "max")
        ]
        dot_radius = 5
        for i, (color, tag) in enumerate(control_colors):
            # Position controls at top right with cleaner spacing
            dot_x = self.screen_width - 80 + (i * (dot_radius * 2 + 8)) # x_start - total_width + current_pos
            dot_y = title_bar_height // 2
            # Delete old dots if they exist
            old_dot = self.screen_canvas.find_withtag(f"screen_dot_{tag}")
            if old_dot: self.screen_canvas.delete(old_dot)
            self.screen_canvas.create_oval(
                dot_x - dot_radius, dot_y - dot_radius,
                dot_x + dot_radius, dot_y + dot_radius,
                fill=color, outline="", tags=f"screen_dot_{tag}")
        
        # Status bar info - cleaner styling
        if hasattr(self, 'view_label') and self.view_label:
            self.screen_canvas.delete(self.view_label)
        self.view_label = self.screen_canvas.create_text(
            25, self.screen_height - status_bar_height // 2, # Adjusted padding 
            text=self.view_label_text, 
            font=self.body, # Replace normal_font_tk
            fill=self.text_color, 
            anchor="w")
            
        # Redraw activity meter if it exists, as its position depends on screen_height
        if hasattr(self, 'activity_meter'):
            self.draw_activity_meter() # Call to redraw/reposition
    
    def create_apps_panel(self):
        """Create right panel for applications and tabs"""
        # Apps panel - right side (30% width)
        self.apps_panel_width = 280  # Further reduced width to 280
        self.apps_panel = tk.Frame(self.content_frame, bg=self.bg_color, width=self.apps_panel_width)
        self.apps_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 40))  # Increased right padding to 40px
        
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
        
        # Create analytics panel - commented out for now until we fix it
        # self.create_analytics_panel()
    
    def create_analytics_panel(self, sidebar_canvas=None, x=20, y=580, width=300):
        """Create a modern analytics panel with data visualization"""
        # If sidebar_canvas not provided, use self.apps_canvas
        if sidebar_canvas is None:
            sidebar_canvas = self.apps_canvas
            
        panel_height = 140
        
        # Create shadow for analytics panel
        shadow = self.create_shadow_image(width, panel_height, radius=12, alpha=60)
        self.analytics_shadow = ImageTk.PhotoImage(shadow)
        sidebar_canvas.create_image(
            x, y,
            image=self.analytics_shadow,
            anchor="nw",
            tags="analytics_shadow"
        )
        
        # Create analytics panel with frosted effect
        panel = self.create_frosted_panel(width, panel_height, radius=12)
        self.analytics_panel = ImageTk.PhotoImage(panel)
        sidebar_canvas.create_image(
            x, y,
            image=self.analytics_panel,
            anchor="nw",
            tags="analytics_panel"
        )
        
        # Header bar
        header_height = 36
        
        sidebar_canvas.create_rectangle(
            x, y,
            x + width, y + header_height,
            fill=self.colors.surface,
            outline="",
            tags="analytics_header"
        )
        
        # Rounded corners for header
        sidebar_canvas.create_arc(
            x, y,
            x + 24, y + 24,
            start=90, extent=90,
            fill=self.colors.surface,
            outline="",
            tags="analytics_header_corner"
        )
        sidebar_canvas.create_arc(
            x + width - 24, y,
            x + width, y + 24,
            start=0, extent=90,
            fill=self.colors.surface,
            outline="",
            tags="analytics_header_corner"
        )
        
        # Header title with icon
        sidebar_canvas.create_text(
            x + 15, y + header_height // 2,
            text="📊",  # Analytics icon
            font=("Segoe UI Emoji", 14),
            fill=self.colors.primary,
            anchor="w",
            tags="analytics_icon"
        )
        
        sidebar_canvas.create_text(
            x + 40, y + header_height // 2,
            text="ACTIVITY INSIGHTS",
            font=self.subtitle_small,
            fill=self.colors.text,
            anchor="w",
            tags="analytics_title"
        )
        
        # Analytics content area
        content_y = y + header_height + 10
        content_height = panel_height - header_height - 20
    
    def draw_apps_panel(self):
        """Draw apps panel with sleek, modern design like Cursor"""
        # Get panel dimensions
        apps_width = self.apps_panel_width
        # Make apps_panel height dynamic based on the content_frame height
        # This requires apps_panel to be packed correctly and to get its height after window rendering.
        # For now, using a fixed or previously calculated height if available.
        apps_height = self.apps_panel.winfo_height()
        if apps_height < 100: apps_height = 690 # Fallback default height, should match control panel top
        
        # Create sleek dark panel
        panel_img = Image.new('RGBA', (apps_width, apps_height), (0,0,0,0)) # Transparent base
        draw = ImageDraw.Draw(panel_img)
        
        panel_bg_rgb = self._ensure_rgb_color(self.secondary_bg)
        border_color_rgb = self._ensure_rgb_color(self.border_color)
        tab_bar_bg_rgb = self._ensure_rgb_color(self.panel_bg) # Slightly different for tab bar
        active_tab_bg_rgb = self._ensure_rgb_color(self.secondary_bg) # Same as panel for seamless look
        accent_primary_rgb = self._ensure_rgb_color(self.accent_primary)

        # Main panel background - sleek dark
        draw.rounded_rectangle(
            (0, 0, apps_width, apps_height), 
            radius=10,  # Consistent rounded corners
            fill=panel_bg_rgb + (250,)) 
        
        # Tab bar with sleek styling
        tab_bar_height = 45 # Slightly taller tab bar for better touch/clickability and visual weight
        draw.rounded_rectangle(
            (0, 0, apps_width, tab_bar_height),
            radius=10, # Match panel radius for top corners
            fill=tab_bar_bg_rgb + (250,)
        )
        # Correct bottom corners of tab bar to be square
        draw.rectangle(
            (0, tab_bar_height - 10, apps_width, tab_bar_height),
            fill=tab_bar_bg_rgb + (250,)
        )
            
        # Active tab indication (assuming first tab is active by default in this drawing)
        # This visual detail should ideally be handled by switch_tab method based on current tab
        active_tab_width = apps_width // 2 # Assuming 2 tabs

        # Draw a background for the active tab text area to make it seem part of the main panel
        draw.rectangle(
            (0, 0, active_tab_width, tab_bar_height),
            fill=active_tab_bg_rgb + (250,) # Make active tab area blend with panel below
        )
        # Redraw top-left rounded corner for the active tab area if it was covered
        draw.rounded_rectangle((0,0,active_tab_width, tab_bar_height), radius=10, fill=active_tab_bg_rgb + (250,))
        draw.rectangle((active_tab_width-10, 0, active_tab_width, tab_bar_height), fill=active_tab_bg_rgb + (250,)) # Ensure right side is square
        draw.rectangle((0, tab_bar_height-10, active_tab_width, tab_bar_height), fill=active_tab_bg_rgb + (250,)) # Ensure bottom is square with main panel

        # Removed the static purple underline since we'll create a dynamic one in switch_tab
        
        # Subtle border for the main apps panel
        draw.rounded_rectangle(
            (0, 0, apps_width, apps_height),
            radius=10,
            fill=None,
            outline=border_color_rgb + (100,), 
            width=1)
        
        # Convert to PhotoImage
        self.apps_frame_img = ImageTk.PhotoImage(panel_img)
        
        # Display on canvas
        if hasattr(self, 'apps_frame') and self.apps_frame:
            self.apps_canvas.itemconfig(self.apps_frame, image=self.apps_frame_img)
        else:
            self.apps_frame = self.apps_canvas.create_image(
                0, 0, image=self.apps_frame_img, anchor="nw")

        # Tab text needs to be redrawn by create_tab_interface or switch_tab
        # Call it here to ensure text appears after panel is drawn/updated
        self.update_tab_text_elements() # Placeholder for a method that redraws tab text
    
    def create_tab_interface(self):
        """Create modern tab interface on apps panel"""
        
        self.app_tab_text = self.apps_canvas.create_text(
            self.apps_panel_width // 4, 22,  # Centered in tab, adjusted y
            text="APPS", 
            font=self.subtitle, # Replace subtitle_font_tk
            fill=self.accent_primary, # Active by default
            tags="apps_tab_text")
        
        self.history_tab_text = self.apps_canvas.create_text(
            self.apps_panel_width // 4 * 3, 22,  # Centered in tab, adjusted y
            text="HISTORY", 
            font=self.button, # Replace normal_font_tk_bold 
            fill=self.secondary_text,
            tags="history_tab_text")
        
        # Make tabs clickable with hover effects
        # These rectangles are for click detection and hover, should be transparent
        self.apps_tab_clickable = self.apps_canvas.create_rectangle(
            0, 0, self.apps_panel_width // 2, 45, # Covers first tab area
            fill="", outline="", tags="apps_tab_clickable")
        
        self.apps_canvas.tag_bind(
            self.apps_tab_clickable, "<Button-1>", lambda e: self.switch_tab("apps"))
        
        self.apps_canvas.tag_bind(
            self.apps_tab_clickable, "<Enter>", 
            lambda e: self.on_tab_hover(self.apps_tab_clickable, True))
        self.apps_canvas.tag_bind(
            self.apps_tab_clickable, "<Leave>", 
            lambda e: self.on_tab_hover(self.apps_tab_clickable, False))
        
        self.history_tab_clickable = self.apps_canvas.create_rectangle(
            self.apps_panel_width // 2, 0, self.apps_panel_width, 45, # Covers second tab area
            fill="", outline="", tags="history_tab_clickable")
        
        self.apps_canvas.tag_bind(
            self.history_tab_clickable, "<Button-1>", lambda e: self.switch_tab("history"))
        
        self.apps_canvas.tag_bind(
            self.history_tab_clickable, "<Enter>", 
            lambda e: self.on_tab_hover(self.history_tab_clickable, True))
        self.apps_canvas.tag_bind(
            self.history_tab_clickable, "<Leave>", 
            lambda e: self.on_tab_hover(self.history_tab_clickable, False))
        
        self.current_hover_rect = None # To store canvas item for hover effect
        
        # Add the initial active tab indicator (under APPS by default)
        self.active_tab_indicator = self.apps_canvas.create_rectangle(
            15, 45 - 3,  # x1, y1 (just below the tabs)
            (self.apps_panel_width // 2) - 15, 45,  # x2, y2
            fill=self.accent_primary,  # Purple underline
            outline=""
        )

    def on_tab_hover(self, tab_widget_tag, is_hovering):
        """Handle tab hover visual feedback."""
        # Find which tab text corresponds to the clickable area tag
        target_text_tag = ""
        if tab_widget_tag == self.apps_tab_clickable:
            target_text_tag = "apps_tab_text"
        elif tab_widget_tag == self.history_tab_clickable:
            target_text_tag = "history_tab_text"
        
        active_tab_color = self.accent_primary
        inactive_tab_color = self.secondary_text
        hover_color = self.accent_tertiary # Bright cyan for hover

        # Determine current active tab to avoid changing its color from active to hover
        is_target_active = False
        if target_text_tag == "apps_tab_text" and self.apps_canvas.itemcget(self.apps_container_window, 'state') == 'normal':
            is_target_active = True
        elif target_text_tag == "history_tab_text" and self.apps_canvas.itemcget(self.history_container_window, 'state') == 'normal':
            is_target_active = True

        if is_hovering:
            if not is_target_active:
                self.apps_canvas.itemconfig(target_text_tag, fill=hover_color)
        else:
            if not is_target_active:
                self.apps_canvas.itemconfig(target_text_tag, fill=inactive_tab_color)
            # If it IS active, ensure it's the active_tab_color
            elif target_text_tag: # ensure target_text_tag is not empty
                 self.apps_canvas.itemconfig(target_text_tag, fill=active_tab_color)

    def update_tab_text_elements(self):
        """Redraws or updates tab text elements. Called after panel redraws."""
        # This is a simplified way to ensure text is on top. A more robust way is to manage layers or use itemconfig.
        if hasattr(self, 'app_tab_text') and self.app_tab_text:
            self.apps_canvas.itemconfig(self.app_tab_text, font=self.subtitle if self.apps_canvas.itemcget(self.apps_container_window, 'state') == 'normal' else self.button)
            self.apps_canvas.itemconfig(self.app_tab_text, fill=self.accent_primary if self.apps_canvas.itemcget(self.apps_container_window, 'state') == 'normal' else self.secondary_text)
            self.apps_canvas.tag_raise(self.app_tab_text)

        if hasattr(self, 'history_tab_text') and self.history_tab_text:
            self.apps_canvas.itemconfig(self.history_tab_text, font=self.subtitle if self.apps_canvas.itemcget(self.history_container_window, 'state') == 'normal' else self.button)
            self.apps_canvas.itemconfig(self.history_tab_text, fill=self.accent_primary if self.apps_canvas.itemcget(self.history_container_window, 'state') == 'normal' else self.secondary_text)
            self.apps_canvas.tag_raise(self.history_tab_text)

        # Also raise clickable areas if they exist
        if hasattr(self, 'apps_tab_clickable'): self.apps_canvas.tag_raise(self.apps_tab_clickable)
        if hasattr(self, 'history_tab_clickable'): self.apps_canvas.tag_raise(self.history_tab_clickable)
    
    def create_apps_list(self):
        """Create modern applications list area"""
        # Search bar - sleek modern style
        search_bg = self.apps_canvas.create_rounded_rectangle(
            20, 60, self.apps_panel_width - 20, 90,  # Thinner search bar
            radius=4,  # Smaller radius for modern look
            fill="#242935")  # Slightly lighter than background
        
        # Search icon - minimal design
        self.apps_canvas.create_oval(
            35, 75, 41, 81, outline=self.secondary_text, width=1)
        self.apps_canvas.create_line(
            40, 80, 45, 85, fill=self.secondary_text, width=1)
        
        # Search text - modern styling
        self.search_text = self.apps_canvas.create_text(
            55, 75, text="Search applications...",
            font=self.caption, # Replace small_font_tk
            fill=self.secondary_text, anchor="w")
        
        # Container for app cards with dark styling
        self.apps_container = tk.Frame(
            self.apps_canvas, bg=self.secondary_bg, highlightthickness=0)
        
        self.apps_container_window = self.apps_canvas.create_window(
            20, 105, window=self.apps_container,
            anchor="nw", width=self.apps_panel_width - 40, height=425)
    
    def create_history_tab(self):
        """Create browser history tab with sleek modern styling"""
        # History container with dark styling
        self.history_container = tk.Frame(
            self.apps_canvas, bg=self.secondary_bg, highlightthickness=0)
        
        # Position it offscreen initially (will be shown on tab switch)
        self.history_container_window = self.apps_canvas.create_window(
            self.apps_panel_width + 20, 105, window=self.history_container,
            anchor="nw", width=self.apps_panel_width - 40, height=425,
            state="hidden")  # Initially hidden
        
        # Modern filter options
        filter_frame = tk.Frame(self.history_container, bg=self.secondary_bg)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Modern filter label
        tk.Label(
            filter_frame, text="FILTER BY:", 
            font=self.caption, # Replace small_font_tk
            fg=self.secondary_text, bg=self.secondary_bg, 
            anchor="w"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Filter buttons with modern styling
        filter_options = ["All", "Search", "Social", "Video"]
        
        for option in filter_options:
            # Create sleek pill buttons
            btn = tk.Label(
                filter_frame, text=option,
                font=self.caption, # Replace small_font_tk
                fg=self.secondary_text if option != "All" else self.accent_primary,
                bg=self.panel_bg if option != "All" else self.highlight_color,
                padx=10, pady=3,
                borderwidth=0
            )
            btn.pack(side=tk.LEFT, padx=(0, 6))
            
            # Add hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(
                bg=self.highlight_color, 
                fg=self.accent_primary))
            
            btn.bind("<Leave>", lambda e, b=btn, o=option: b.config(
                bg=self.panel_bg if o != "All" else self.highlight_color, 
                fg=self.secondary_text if o != "All" else self.accent_primary))
        
        # Scrollable history list with modern styling
        self.history_listbox = tk.Frame(self.history_container, bg=self.secondary_bg)
        self.history_listbox.pack(fill=tk.BOTH, expand=True)
    
    def update_history_list(self):
        """Update history list with sleek styling"""
        # Clear existing history items
        for widget in self.history_listbox.winfo_children():
            widget.destroy()
        
        # Add history items with modern styling
        for item in self.browser_history:
            # Create modern history card
            history_card = tk.Frame(
                self.history_listbox, 
                bg=self.panel_bg,
                highlightthickness=1,
                highlightbackground=self.border_color)
            
            history_card.pack(fill=tk.X, pady=(0, 8))
            
            # Add hover effect
            def on_enter(e, card=history_card):
                card.config(highlightbackground=self.accent_primary)
            
            def on_leave(e, card=history_card):
                card.config(highlightbackground=self.border_color)
                
            history_card.bind("<Enter>", on_enter)
            history_card.bind("<Leave>", on_leave)
            
            # Left side with site icon
            icon_frame = tk.Frame(
                history_card, 
                bg=self.highlight_color, 
                width=32, height=32)
            
            icon_frame.pack(side=tk.LEFT, padx=10, pady=8)
            icon_frame.pack_propagate(False)
            
            # Use domain initial for icon
            domain = item["url"].split("/")[0].replace("www.", "")[0].upper()
            tk.Label(
                icon_frame, text=domain,
                font=self.caption, # Replace small_font_tk
                fg=self.accent_tertiary, bg=icon_frame["bg"]
            ).pack(expand=True)
            
            # History details
            details_frame = tk.Frame(history_card, bg=self.panel_bg)
            details_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8, pady=8)
            
            # Website title
            tk.Label(
                details_frame, text=item["title"],
                font=self.body, # Replace normal_font_tk
                fg=self.text_color, bg=self.panel_bg,
                anchor="w", justify="left"
            ).pack(fill=tk.X, anchor="w")
            
            # URL with subdued styling
            tk.Label(
                details_frame, text=item["url"],
                font=self.caption, # Replace small_font_tk
                fg=self.secondary_text, bg=self.panel_bg,
                anchor="w", justify="left"
            ).pack(fill=tk.X, anchor="w")
            
            # Time visited
            time_label = tk.Label(
                history_card, text=item["time"],
                font=self.caption, # Replace small_font_tk
                fg=self.secondary_text, bg=self.panel_bg
            )
            time_label.pack(side=tk.RIGHT, padx=10, pady=10)
    
    def update_status(self, status_text, color=None):
        """Update connection status indicator with elegant animation"""
        try:
            # Update status text
            if hasattr(self, 'status_var'):
                self.status_var.set(status_text)
            
            if hasattr(self, 'status_text') and hasattr(self, 'header_canvas'):
                try:
                    self.header_canvas.itemconfig(self.status_text, text=status_text)
                except Exception:
                    pass
            
            # Comment out the problematic server_status_text update
            # Attempting to update the server status text is causing the error
            '''
            if hasattr(self, 'server_status_text'):
                try:
                    self.control_canvas.itemconfig(self.server_status_text, text=status_text)
                except TypeError:
                    pass
            '''
            
            # Update status indicator color
            if color:
                if color == "green":
                    fill_color = self.colors.success
                elif color == "red":
                    fill_color = self.colors.secondary
                elif color == "orange":
                    fill_color = self.colors.warning
                else:
                    fill_color = color
                    
                # Update status dot
                if hasattr(self, 'connection_indicator') and hasattr(self, 'header_canvas'):
                    try:
                        self.header_canvas.itemconfig(self.connection_indicator, fill=fill_color)
                    except Exception:
                        pass
                    
                # Update pulse color
                if hasattr(self, 'status_pulse') and hasattr(self, 'header_canvas'):
                    try:
                        self.header_canvas.itemconfig(self.status_pulse, outline=fill_color + "80")  # 50% transparency
                    except Exception:
                        pass
        except Exception:
            # Silently ignore any errors in the status update
            pass
    
    def start_server(self):
        """Start monitoring server with elegant transitions"""
        if self.server_running:
            return
            
        try:
            # Update status with animation
            self.update_status("Starting server...", "orange")
            
            # For demonstration, simulate server start
            self.server_running = True
            
            # Update button states
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            
            # Elegant status transition with animation
            def update_status_delayed():
                self.update_status("Connected", "green")
                # Start activity simulations
                self.root.after(1000, self.simulate_activity_updates)
            
            # Delayed status update for visual effect
            self.root.after(1000, update_status_delayed)
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}", "red")
    
    def show_loading_bar(self):
        """Show a loading bar animation overlay for visual effect only"""
        # Create a semi-transparent overlay
        overlay_frame = tk.Frame(self.root, bg=self.colors.bg + "99")  # 60% opacity
        overlay_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Container for loading elements
        loading_container = tk.Frame(overlay_frame, bg=self.colors.surface_2)
        loading_container.configure(width=400, height=150)
        loading_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Add rounded corners and shadow to container
        container_canvas = tk.Canvas(loading_container, bg=self.colors.surface_2, 
                                    highlightthickness=0, width=400, height=150)
        container_canvas.place(x=0, y=0)
        
        # Create rounded rectangle for the container
        container_canvas.create_rounded_rectangle(2, 2, 398, 148, radius=15, 
                                                fill=self.colors.surface_2, 
                                                outline=self.colors.border, width=1)
        
        # Loading text
        loading_label = tk.Label(
            container_canvas, 
            text="LOADING DATA", 
            font=self.subtitle, 
            fg=self.colors.primary, 
            bg=self.colors.surface_2
        )
        loading_label.place(relx=0.5, rely=0.3, anchor="center")
        
        # Progress bar background
        progress_bg = tk.Frame(container_canvas, bg=self.colors.surface_3, width=320, height=8)
        progress_bg.place(relx=0.5, rely=0.55, anchor="center", width=320)
        
        # Progress bar
        progress_bar = tk.Frame(container_canvas, bg=self.colors.primary, width=0, height=8)
        progress_bar.place(relx=0.5, rely=0.55, anchor="center", width=0)
        
        # Status text
        status_var = tk.StringVar()
        status_var.set("Initializing connection...")
        status_label = tk.Label(
            container_canvas, 
            textvariable=status_var, 
            font=self.body_small, 
            fg=self.colors.text_secondary, 
            bg=self.colors.surface_2
        )
        status_label.place(relx=0.5, rely=0.75, anchor="center")
        
        # Status messages to cycle through
        status_messages = [
            "Initializing connection...",
            "Establishing secure channel...",
            "Loading monitoring modules...",
            "Preparing data streams...",
            "Activating oversight protocols...",
            "Connection established!"
        ]
        
        # Animate progress bar
        def update_progress_bar(width):
            progress_bar.place(width=width)
            
            # Update status message based on progress
            progress_percent = width / 320
            message_idx = min(int(progress_percent * len(status_messages)), len(status_messages) - 1)
            status_var.set(status_messages[message_idx])
        
        # Start progress animation
        self.animate(
            "loading_progress", 0, 320, 3.0, 
            update_progress_bar, "ease_in_out_quad",
            lambda: self.root.after(500, lambda: self.fade_out_overlay(overlay_frame))
        )
    
    def stop_server(self):
        """Stop monitoring server with elegant transitions"""
        if not self.server_running:
            return
            
        # Update status with animation
        self.update_status("Stopping server...", "orange")
        
        # For demonstration, simulate server stop
        self.server_running = False
        
        # Update button states
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        
        # Elegant status transition
        def update_status_delayed():
            self.update_status("Disconnected", "red")
        
        # Delayed status update for visual effect
        self.root.after(1000, update_status_delayed)
    
    def pause_screen(self):
        """Pause/resume screen updates with elegant animation"""
        self.screen_paused = not self.screen_paused
        
        if self.screen_paused:
            # Update button text and status
            self.pause_button.config(text="RESUME SCREEN")
            self.update_status("Screen updates paused", "orange")
            
            # Add overlay to indicate paused state
            if hasattr(self, 'screen_area'):
                x1, y1, x2, y2 = self.screen_area
                
                # Semi-transparent overlay
                overlay = self.screen_canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=self.colors.overlay_medium,
                    outline="",
                    tags="pause_overlay"
                )
                
                # Pause icon
                icon_width = 40
                icon_height = 60
                icon_x = (x1 + x2) // 2
                icon_y = (y1 + y2) // 2
                
                # Two pause bars
                bar_width = 15
                bar_spacing = 10
                
                self.screen_canvas.create_rectangle(
                    icon_x - bar_width - bar_spacing//2, icon_y - icon_height//2,
                    icon_x - bar_spacing//2, icon_y + icon_height//2,
                    fill=self.colors.text,
                    outline="",
                    tags="pause_icon"
                )
                
                self.screen_canvas.create_rectangle(
                    icon_x + bar_spacing//2, icon_y - icon_height//2,
                    icon_x + bar_width + bar_spacing//2, icon_y + icon_height//2,
                    fill=self.colors.text,
                    outline="",
                    tags="pause_icon"
                )
                
                # Animate overlay appearance
                self.screen_canvas.itemconfig(overlay, fill=self.colors.bg + "00")  # Start transparent
                
                def update_overlay_alpha(alpha):
                    self.screen_canvas.itemconfig(
                        overlay,
                        fill=self.colors.overlay_medium[:-2] + f"{int(alpha*255):02x}"
                    )
                
                self.animate("pause_overlay", 0.0, 0.5, 0.5, update_overlay_alpha, "ease_out_quad")
        else:
            # Update button text and status
            self.pause_button.config(text="PAUSE SCREEN")
            self.update_status("Screen updates resumed", "green")
            
            # Remove pause overlay with fade animation
            if self.screen_canvas.find_withtag("pause_overlay"):
                overlay = self.screen_canvas.find_withtag("pause_overlay")[0]
                
                def update_overlay_alpha(alpha):
                    self.screen_canvas.itemconfig(
                        overlay,
                        fill=self.colors.overlay_medium[:-2] + f"{int(alpha*255):02x}"
                    )
                
                # Fade out animation
                self.animate(
                    "pause_overlay", 0.5, 0.0, 0.5,
                    update_overlay_alpha, "ease_in_quad",
                    lambda: self.screen_canvas.delete("pause_overlay", "pause_icon")
                )
    
    def switch_tab(self, tab_name):
        """Switch between apps and history tabs with elegant animation"""
        if not hasattr(self, 'apps_container_window') or not hasattr(self, 'history_container_window'):
            print("Tab containers not initialized yet")
            return
            
        if tab_name == self.current_tab:
            return
            
        # Store previous tab for animation
        prev_tab = self.current_tab
        self.current_tab = tab_name
        
        # Use apps_panel instead of sidebar
        panel_width = self.apps_panel.winfo_width() if self.apps_panel.winfo_width() > 50 else self.apps_panel_width
        tab_width = (panel_width - 20) // 2
        
        # Determine which canvas to use
        canvas = self.apps_canvas
        
        # Get current tab indicator position
        if hasattr(self, 'active_tab_indicator'):
            current_coords = canvas.coords(self.active_tab_indicator)
            
            # Calculate target coordinates based on the selected tab
            if tab_name == "apps":
                # APPS tab - left side
                target_x1 = 15
                target_x2 = (panel_width // 2) - 15
            else:
                # HISTORY tab - right side
                target_x1 = (panel_width // 2) + 15
                target_x2 = panel_width - 15
                
            # The y coordinates remain the same
            target_y1 = current_coords[1]
            target_y2 = current_coords[3]
            
            # Animate the tab indicator's movement
            def update_indicator_position(progress):
                # Calculate current position based on progress
                current_x1 = current_coords[0] + (target_x1 - current_coords[0]) * progress
                current_x2 = current_coords[2] + (target_x2 - current_coords[2]) * progress
                
                # Update the indicator's position
                canvas.coords(
                    self.active_tab_indicator,
                    current_x1, target_y1, current_x2, target_y2
                )
            
            # Start the animation over 0.7 seconds with a smoother easing for better transition
            self.animate(
                "tab_indicator", 0.0, 1.0, 0.7,
                update_indicator_position, "ease_in_out_cubic"
            )
        else:
            # Create new tab indicator if it doesn't exist yet
            if tab_name == "apps":
                # Create indicator under the APPS tab
                self.active_tab_indicator = canvas.create_rectangle(
                    15, 45 - 3,  # x1, y1 (just below the tabs)
                    (panel_width // 2) - 15, 45,  # x2, y2
                    fill=self.accent_primary,  # Purple underline
                    outline=""
                )
            else:  # history tab
                # Create indicator under the HISTORY tab
                self.active_tab_indicator = canvas.create_rectangle(
                    (panel_width // 2) + 15, 45 - 3,  # x1, y1 (just below the tabs)
                    panel_width - 15, 45,  # x2, y2
                    fill=self.accent_primary,  # Purple underline
                    outline=""
                )
        
        try:
            if tab_name == "apps":
            # Update tab colors
                canvas.itemconfig("apps_tab_text", font=self.subtitle, fill=self.accent_primary)
                canvas.itemconfig("history_tab_text", font=self.button, fill=self.secondary_text)
            
                # Show apps container, hide history container
                canvas.itemconfig(self.apps_container_window, state="normal")
                canvas.itemconfig(self.history_container_window, state="hidden")
                
                # Update search text
                if hasattr(self, 'search_text'):
                    canvas.itemconfig(self.search_text, text="Search applications...")
                
            elif tab_name == "history":
                # Update tab colors
                canvas.itemconfig("apps_tab_text", font=self.button, fill=self.secondary_text)
                canvas.itemconfig("history_tab_text", font=self.subtitle, fill=self.accent_primary)
            
                # Show history container, hide apps container
                canvas.itemconfig(self.apps_container_window, state="hidden")
                canvas.itemconfig(self.history_container_window, state="normal")
                
                # Update search text
                if hasattr(self, 'search_text'):
                    canvas.itemconfig(self.search_text, text="Search history...")
            
        except Exception as e:
            print(f"Error switching tabs: {e}")
            # Revert to previous tab if there was an error
            self.current_tab = prev_tab
    
    def load_sample_data(self):
        """Load sample data with elegant animations"""
        # Populate apps list
        self.windows_list = list(self.sample_windows.values())
        self.update_apps_list()
        
        # Update browser history
        self.browser_history = self.sample_history
        self.update_history_list()
        
        # Create sample screen with animation
        self.create_sample_screen()
        
        # Remove the status update that's causing errors
        # self.update_status("Ready to connect", "orange")
    
    def animate_activity_meter(self):
        """Animate activity meter with smooth transitions"""
        if not hasattr(self, 'activity_level'):
            self.activity_level = 0.5  # Start at mid-level
            
        # Slightly change activity level to simulate real usage
        change = random.uniform(-0.08, 0.08)
        self.activity_level = max(0.1, min(0.9, self.activity_level + change))
        
        # Update meter width
        meter_width = 180
        meter_height = 6
        
        x = self.screen_canvas.coords(self.activity_meter)[0]  # Left edge stays fixed
        y = self.screen_canvas.coords(self.activity_meter)[1]  # Top edge
        
        # New width based on activity level
        new_width = meter_width * self.activity_level
        
        # Update meter position with animation
        self.screen_canvas.coords(
            self.activity_meter,
            x, y,
            x + new_width, y + meter_height
        )
        
        # Update color based on activity level
        if self.activity_level < 0.3:
            color = self.colors.success  # Low activity
        elif self.activity_level < 0.7:
            color = self.colors.primary  # Medium activity
        else:
            color = self.colors.secondary  # High activity
            
        self.screen_canvas.itemconfig(self.activity_meter, fill=color)
        
        # Schedule next update
        self.root.after(50, self.animate_activity_meter)
    
    def simulate_activity_updates(self):
        """Simulate random activity updates for demo purposes"""
        if not self.server_running:
            return
            
        # Randomly change active window
        if random.random() > 0.7:
            if self.windows_list:
                new_active = random.choice(self.windows_list)
                self.active_window_id = new_active["id"]
                
                # Update UI
                self.update_apps_list()
                
                # Update view label
                self.view_label_text = f"Current View: {new_active['title']}"
                if hasattr(self, 'view_label'):
                    self.screen_canvas.itemconfig(self.view_label, text=self.view_label_text)
                
                # Flash status briefly
                self.update_status(f"Switched to {new_active['title']}", "green")
                self.root.after(2000, lambda: self.update_status("Connected", "green"))
        
        # Schedule next update with variable timing
        self.root.after(random.randint(3000, 7000), self.simulate_activity_updates)
    
    def update_apps_list(self):
        """Update applications list with elegant modern UI"""
        # Clear existing content
        for widget in self.apps_container.winfo_children():
            widget.destroy()
        
        # Create scrollable frame
        apps_canvas = tk.Canvas(
            self.apps_container,
            bg=self.colors.surface,
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            self.apps_container,
            orient="vertical",
            command=apps_canvas.yview,
            style="Vertical.TScrollbar"
        )
        scrollable_frame = tk.Frame(apps_canvas, bg=self.colors.surface)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: apps_canvas.configure(scrollregion=apps_canvas.bbox("all"))
        )
        
        apps_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        apps_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        scrollbar.pack(side="right", fill="y")
        apps_canvas.pack(side="left", fill="both", expand=True)
        
        # Add apps to the list
        category_colors = {
            "games": self.colors.category_games,
            "web": self.colors.category_web,
            "social": self.colors.category_social,
            "productivity": self.colors.category_productivity,
            "system": self.colors.category_system,
            "education": self.colors.category_education,
            "video": self.colors.category_video,
            "other": self.colors.category_other
        }
        
        for i, window in enumerate(self.windows_list):
            # App item container
            app_frame = tk.Frame(
                scrollable_frame,
                bg=self.colors.surface,
                padx=5,
                pady=3
            )
            app_frame.pack(fill="x", expand=True)
            
            # App card with shadow effect
            app_card = tk.Canvas(
                app_frame,
                bg=self.colors.surface,
                highlightthickness=0,
                height=80
            )
            app_card.pack(fill="x", padx=2, pady=2)
            
            # Card background with rounded corners
            app_card.create_rounded_rectangle(
                5, 5,
                app_card.winfo_reqwidth() - 5, 75,
                radius=10,
                fill=self.colors.surface_2,
                outline="",
                tags=f"app_bg_{i}"
            )
            
            # Highlight active app
            is_active = window["id"] == self.active_window_id
            if is_active:
                # Active indicator with glow
                app_card.create_rounded_rectangle(
                    5, 5,
                    app_card.winfo_reqwidth() - 5, 75,
                    radius=10,
                    fill=self.colors.surface_3,
                    outline=self.colors.primary,
                    width=2,
                    tags=f"app_active_bg_{i}"
                )
            
            # Category indicator
            category = window.get("category", "other")
            category_color = category_colors.get(category, self.colors.category_other)
            
            app_card.create_rounded_rectangle(
                15, 15,
                35, 65,
                radius=5,
                fill=category_color,
                outline="",
                tags=f"app_category_{i}"
            )
            
            # Category icon
            app_card.create_text(
                25, 40,
                text=window.get("icon", "📱"),
                font=("Segoe UI Emoji", 16),
                fill="white",
                tags=f"app_icon_{i}"
            )
            
            # App title with elegant typography
            app_card.create_text(
                50, 30,
                text=window["title"],
                font=self.subtitle_small if is_active else self.body,
                fill=self.colors.text if is_active else self.colors.text_secondary,
                anchor="w",
                tags=f"app_title_{i}"
            )
            
            # Process name - monospace for technical feel
            app_card.create_text(
                50, 55,
                text=window["process"],
                font=self.mono_small,
                fill=self.colors.text_tertiary,
                anchor="w",
                tags=f"app_process_{i}"
            )
            
            # Add 'View' button for each app
            view_button = ttk.Button(
                app_card,
                text="VIEW",
                style="OutlinePrimary.TButton",
                command=lambda app_id=window["id"]: self.select_app(app_id)
            )
            
            view_button_window = app_card.create_window(
                app_card.winfo_reqwidth() - 80, 40,
                window=view_button,
                width=70,
                height=30,
                anchor="e",
                tags=f"app_view_btn_{i}"
            )
            
            # Add hover effect for card
            def on_enter(e, idx=i):
                if self.windows_list[idx]["id"] != self.active_window_id:
                    app_card.itemconfig(f"app_bg_{idx}", fill=self.colors.surface_3)
                    app_card.itemconfig(f"app_title_{idx}", fill=self.colors.text)
            
            def on_leave(e, idx=i):
                if self.windows_list[idx]["id"] != self.active_window_id:
                    app_card.itemconfig(f"app_bg_{idx}", fill=self.colors.surface_2)
                    app_card.itemconfig(f"app_title_{idx}", fill=self.colors.text_secondary)
            
            app_card.bind("<Enter>", on_enter)
            app_card.bind("<Leave>", on_leave)
            
            # Update card width dynamically
            app_card.update_idletasks()
            w = app_frame.winfo_width() - 10 if app_frame.winfo_width() > 10 else 290
            app_card.itemconfig(f"app_bg_{i}", width=w-10)
            if is_active:
                app_card.itemconfig(f"app_active_bg_{i}", width=w-10)
            
            # Fix view button position
            app_card.coords(view_button_window, w-80, 40)
    
    def update_history_list(self):
        """Update browser history list with elegant modern UI"""
        # Clear existing content
        for widget in self.history_container.winfo_children():
            widget.destroy()
        
        # Create scrollable frame
        history_canvas = tk.Canvas(
            self.history_container,
            bg=self.colors.surface,
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            self.history_container,
            orient="vertical",
            command=history_canvas.yview,
            style="Vertical.TScrollbar"
        )
        scrollable_frame = tk.Frame(history_canvas, bg=self.colors.surface)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: history_canvas.configure(scrollregion=history_canvas.bbox("all"))
        )
        
        history_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        history_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        scrollbar.pack(side="right", fill="y")
        history_canvas.pack(side="left", fill="both", expand=True)
        
        # Add history items
        category_colors = {
            "games": self.colors.category_games,
            "web": self.colors.category_web,
            "social": self.colors.category_social,
            "productivity": self.colors.category_productivity,
            "system": self.colors.category_system,
            "education": self.colors.category_education,
            "video": self.colors.category_video,
            "other": self.colors.category_other
        }
        
        for i, item in enumerate(self.browser_history):
            # History item container
            item_frame = tk.Frame(
                scrollable_frame,
                bg=self.colors.surface,
                padx=5,
                pady=3
            )
            item_frame.pack(fill="x", expand=True)
            
            # History card
            history_card = tk.Canvas(
                item_frame,
                bg=self.colors.surface,
                highlightthickness=0,
                height=70
            )
            history_card.pack(fill="x", padx=2, pady=2)
            
            # Card background with rounded corners
            history_card.create_rounded_rectangle(
                5, 5,
                history_card.winfo_reqwidth() - 5, 65,
                radius=10,
                fill=self.colors.surface_2,
                outline="",
                tags=f"history_bg_{i}"
            )
            
            # Category indicator (colored dot)
            category = item.get("category", "web")
            category_color = category_colors.get(category, self.colors.category_web)
            
            history_card.create_oval(
                15, 35 - 6,
                15 + 12, 35 + 6,
                fill=category_color,
                outline="",
                tags=f"history_category_{i}"
            )
            
            # Time label
            history_card.create_text(
                40, 20,
                text=item["time"],
                font=self.mono_small,
                fill=self.colors.text_tertiary,
                anchor="w",
                tags=f"history_time_{i}"
            )
            
            # Title with elegant typography
            history_card.create_text(
                40, 40,
                text=item["title"],
                font=self.body,
                fill=self.colors.text,
                anchor="w",
                tags=f"history_title_{i}"
            )
            
            # URL - monospace for technical feel
            history_card.create_text(
                40, 55,
                text=item["url"],
                font=self.mono_small,
                fill=self.colors.info,
                anchor="w",
                tags=f"history_url_{i}"
            )
            
            # Add hover effect for card
            def on_enter(e, idx=i):
                history_card.itemconfig(f"history_bg_{idx}", fill=self.colors.surface_3)
            
            def on_leave(e, idx=i):
                history_card.itemconfig(f"history_bg_{idx}", fill=self.colors.surface_2)
            
            history_card.bind("<Enter>", on_enter)
            history_card.bind("<Leave>", on_leave)
            
            # Update card width dynamically
            history_card.update_idletasks()
            w = item_frame.winfo_width() - 10 if item_frame.winfo_width() > 10 else 290
            history_card.itemconfig(f"history_bg_{i}", width=w-10)
    
    def create_sample_screen(self):
        """Create sample screen capture with elegant animation"""
        # Screen dimensions from the screen area
        if hasattr(self, 'screen_area'):
            x1, y1, x2, y2 = self.screen_area
            screen_width = x2 - x1
            screen_height = y2 - y1
            
            # Create a blank screen with subtle texture
            screen = Image.new('RGB', (screen_width, screen_height), self._hex_to_rgb(self.colors.bg))
            draw = ImageDraw.Draw(screen)
            
            # Draw a sample Minecraft-like interface
            # Sky
            for y in range(0, screen_height // 3):
                # Gradient from light blue to darker blue
                progress = y / (screen_height // 3)
                r = int(135 * (1 - progress) + 80 * progress)
                g = int(206 * (1 - progress) + 140 * progress)
                b = int(235 * (1 - progress) + 180 * progress)
                draw.line([(0, y), (screen_width, y)], fill=(r, g, b))
            
            # Hills/mountains
            for x in range(0, screen_width, 5):
                # Random height mountains
                height = int(screen_height // 3 + math.sin(x/50) * 30 + random.randint(-10, 10))
                draw.line([(x, height), (x, screen_height // 3)], fill=(60, 90, 60))
            
            # Ground/terrain
            draw.rectangle(
                [0, screen_height // 3, screen_width, screen_height],
                fill=(82, 54, 32)
            )
            
            # Add grid pattern for Minecraft blocks
            grid_size = 20
            for x in range(0, screen_width, grid_size):
                draw.line([(x, screen_height // 3), (x, screen_height)], fill=(60, 40, 20), width=1)
            
            for y in range(screen_height // 3, screen_height, grid_size):
                draw.line([(0, y), (screen_width, y)], fill=(60, 40, 20), width=1)
            
            # Add some random colored blocks
            block_colors = [
                (110, 80, 50),  # Brown
                (100, 100, 100),  # Stone
                (30, 150, 30),  # Green
                (150, 30, 30),  # Red
                (30, 30, 150),  # Blue
            ]
            
            for _ in range(40):
                grid_x = random.randint(0, screen_width // grid_size - 1)
                grid_y = random.randint(screen_height // 3 // grid_size, screen_height // grid_size - 1)
                color = random.choice(block_colors)
                
                draw.rectangle(
                    [grid_x * grid_size, grid_y * grid_size,
                     (grid_x + 1) * grid_size, (grid_y + 1) * grid_size],
                    fill=color
                )
            
            # HUD elements - hotbar
            hotbar_width = screen_width // 2
            hotbar_height = 30
            hotbar_x = (screen_width - hotbar_width) // 2
            hotbar_y = screen_height - hotbar_height - 10
            
            # Hotbar background
            draw.rounded_rectangle(
                [hotbar_x, hotbar_y, hotbar_x + hotbar_width, hotbar_y + hotbar_height],
                radius=5,
                fill=(0, 0, 0, 128)  # Semi-transparent black
            )
            
            # Hotbar slots
            slot_size = hotbar_height - 4
            for i in range(9):
                slot_x = hotbar_x + 2 + i * (slot_size + 2)
                
                # Draw slot
                draw.rectangle(
                    [slot_x, hotbar_y + 2, slot_x + slot_size, hotbar_y + 2 + slot_size],
                    fill=(60, 60, 60, 200),
                    outline=(100, 100, 100, 150)
                )
                
                # Highlight selected slot
                if i == 4:
                    draw.rectangle(
                        [slot_x - 2, hotbar_y, slot_x + slot_size + 2, hotbar_y + hotbar_height],
                        outline=(255, 255, 255, 200),
                        width=2
                    )
            
            # Create crosshair in center
            crosshair_size = 10
            center_x = screen_width // 2
            center_y = screen_height // 2
            
            draw.line(
                [center_x - crosshair_size, center_y,
                 center_x + crosshair_size, center_y],
                fill=(255, 255, 255, 200),
                width=2
            )
            
            draw.line(
                [center_x, center_y - crosshair_size,
                 center_x, center_y + crosshair_size],
                fill=(255, 255, 255, 200),
                width=2
            )
            
            # Display the screen
            self.screen_photo = ImageTk.PhotoImage(screen)
            
            if not hasattr(self, 'screen_image'):
                # Position the image exactly at the screen_area coordinates
                self.screen_image = self.screen_canvas.create_image(
                    x1, y1,
                    image=self.screen_photo,
                    anchor="nw",
                    tags="screen_image"
                )
            else:
                self.screen_canvas.itemconfig(self.screen_image, image=self.screen_photo)
                # Ensure correct positioning
                self.screen_canvas.coords(self.screen_image, x1, y1)
                
            # Update view label
            active_app = next((app for app in self.windows_list if app["id"] == self.active_window_id), None)
            if active_app:
                self.view_label_text = f"Current View: {active_app['title']}"
                self.screen_canvas.itemconfig(self.view_label, text=self.view_label_text)
    
    def select_app(self, app_id):
        """Select an app to view with elegant transition"""
        # Update active window
        self.active_window_id = app_id
        
        # Update apps list
        self.update_apps_list()
        
        # Update view with animation
        # Add a brief flash effect
        if hasattr(self, 'screen_area'):
            x1, y1, x2, y2 = self.screen_area
            
            # Create flash overlay
            flash = self.screen_canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=self.colors.primary + "40",  # Semi-transparent overlay
                outline="",
                tags="screen_flash"
            )
            
            # Animate flash out
            def update_flash_alpha(alpha):
                self.screen_canvas.itemconfig(
                    flash,
                    fill=self.colors.primary + f"{int(alpha*64):02x}"
                )
            
            # After flash animation, create new sample screen and ensure correct positioning
            def after_flash():
                self.screen_canvas.delete("screen_flash")
                self.create_sample_screen()
                # Ensure screen is positioned correctly
                if hasattr(self, 'screen_image') and hasattr(self, 'screen_area'):
                    self.screen_canvas.coords(self.screen_image, self.screen_area[0], self.screen_area[1])
            
            self.animate(
                "screen_flash", 1.0, 0.0, 0.5,
                update_flash_alpha, "ease_out_quad",
                after_flash
            )
        
        # Update view label
        active_app = next((app for app in self.windows_list if app["id"] == app_id), None)
        if active_app:
            self.view_label_text = f"Current View: {active_app['title']}"
            if hasattr(self, 'view_label'):
                self.screen_canvas.itemconfig(self.view_label, text=self.view_label_text)

    def _ensure_color_compatible(self, color):
        """Convert hex color with alpha to TkInter compatible color"""
        if isinstance(color, str) and color.startswith('#') and len(color) == 9:
            # Extract RGB part only, discard alpha
            return color[:7]
        return color
        
    def create_control_panel(self):
        """Create control panel with sleek modern styling"""
        # Control panel at the bottom
        self.control_frame = tk.Frame(self.main_frame, bg=self.bg_color, height=180)
        self.control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Canvas for control panel
        self.control_canvas = tk.Canvas(self.control_frame, 
                                      highlightthickness=0, 
                                      bg=self.bg_color)
        self.control_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Draw control panel
        self.draw_control_panel()
        
        # Server address input - refined styling
        ip_label_x = 60
        ip_label_y = 40
        entry_width = 200
        entry_height = 36
        entry_x = ip_label_x + 100
        
        # Label with clean styling
        self.control_canvas.create_text(
            ip_label_x, ip_label_y,
            text="SERVER IP:", 
            font=self.subtitle_small,
            fill=self.text_color,
            anchor="w",
            tags="ip_label")
        
        # Create input shadow for depth
        self.control_canvas.create_rounded_rectangle(
            entry_x + 2, ip_label_y - entry_height//2 + 2,
            entry_x + entry_width + 2, ip_label_y + entry_height//2 + 2,
            radius=6,
            fill=self._ensure_color_compatible(self.colors.shadow_light),
            outline="",
            tags="ip_entry_shadow"
        )
        
        # Create stylish input field
        self.control_canvas.create_rounded_rectangle(
            entry_x, ip_label_y - entry_height//2,
            entry_x + entry_width, ip_label_y + entry_height//2,
            radius=6, 
            fill=self.panel_bg,
            outline=self.border_color,
            width=1,
            tags="ip_entry_bg"
        )
        
        # Add highlight effect for active field
        highlight = self.control_canvas.create_rounded_rectangle(
            entry_x, ip_label_y - entry_height//2,
            entry_x + entry_width, ip_label_y + entry_height//2,
            radius=6, 
            fill="",
            outline=self.accent_primary,
            width=2,
            tags="ip_entry_highlight"
        )
        self.control_canvas.itemconfig(highlight, state="hidden")
        
        # Entry widget for IP
        self.ip_var = tk.StringVar()
        self.ip_var.set(self.server_ip)
        
        self.ip_entry = tk.Entry(
            self.control_canvas,
            textvariable=self.ip_var,
            font=self.body,
            bg=self.panel_bg,
            fg=self.text_color,
            bd=0,
            highlightthickness=0
        )
        
        self.ip_entry_window = self.control_canvas.create_window(
            entry_x + 10, ip_label_y,
            window=self.ip_entry,
            anchor="w",
            width=entry_width - 20,
            height=entry_height - 10,
            tags="ip_entry"
        )
        
        # Add focus events for highlight effect
        def on_entry_focus(e):
            self.control_canvas.itemconfig(highlight, state="normal")
            
        def on_entry_blur(e):
            self.control_canvas.itemconfig(highlight, state="hidden")
            
        self.ip_entry.bind("<FocusIn>", on_entry_focus)
        self.ip_entry.bind("<FocusOut>", on_entry_blur)
        
        # Port input with matching style
        port_label_x = entry_x + entry_width + 40
        port_width = 80
        
        self.control_canvas.create_text(
            port_label_x, ip_label_y,
            text="PORT:", 
            font=self.subtitle_small,
            fill=self.text_color,
            anchor="w",
            tags="port_label")
            
        port_entry_x = port_label_x + 60
        
        # Port input shadow
        self.control_canvas.create_rounded_rectangle(
            port_entry_x + 2, ip_label_y - entry_height//2 + 2,
            port_entry_x + port_width + 2, ip_label_y + entry_height//2 + 2,
            radius=6,
            fill=self._ensure_color_compatible(self.colors.shadow_light),
            outline="",
            tags="port_entry_shadow"
        )
        
        # Port input background
        self.control_canvas.create_rounded_rectangle(
            port_entry_x, ip_label_y - entry_height//2,
            port_entry_x + port_width, ip_label_y + entry_height//2,
            radius=6, 
            fill=self.panel_bg,
            outline=self.border_color,
            width=1,
            tags="port_entry_bg"
        )
        
        # Port highlight
        port_highlight = self.control_canvas.create_rounded_rectangle(
            port_entry_x, ip_label_y - entry_height//2,
            port_entry_x + port_width, ip_label_y + entry_height//2,
            radius=6, 
            fill="",
            outline=self.accent_primary,
            width=2,
            tags="port_entry_highlight"
        )
        self.control_canvas.itemconfig(port_highlight, state="hidden")
        
        # Entry widget for port
        self.port_var = tk.StringVar()
        self.port_var.set(str(self.server_port))
        
        self.port_entry = tk.Entry(
            self.control_canvas,
            textvariable=self.port_var,
            font=self.body,
            bg=self.panel_bg,
            fg=self.text_color,
            bd=0,
            highlightthickness=0
        )
        
        self.port_entry_window = self.control_canvas.create_window(
            port_entry_x + 10, ip_label_y,
            window=self.port_entry,
            anchor="w",
            width=port_width - 20,
            height=entry_height - 10,
            tags="port_entry"
        )
        
        # Add focus events for port highlight
        def on_port_focus(e):
            self.control_canvas.itemconfig(port_highlight, state="normal")
            
        def on_port_blur(e):
            self.control_canvas.itemconfig(port_highlight, state="hidden")
            
        self.port_entry.bind("<FocusIn>", on_port_focus)
        self.port_entry.bind("<FocusOut>", on_port_blur)
        
        # Status display with clean styling
        status_x = port_entry_x + port_width + 40
        
        self.control_canvas.create_text(
            status_x, ip_label_y,
            text="STATUS:", 
            font=self.subtitle_small,
            fill=self.text_color,
            anchor="w",
            tags="status_label")
            
        status_display_x = status_x + 80
        
        # Create status pill with shadow
        self.control_canvas.create_rounded_rectangle(
            status_display_x + 2, ip_label_y - entry_height//2 + 2,
            status_display_x + 150 + 2, ip_label_y + entry_height//2 + 2,
            radius=entry_height//2,
            fill=self._ensure_color_compatible(self.colors.shadow_light),
            outline="",
            tags="status_display_shadow"
        )
        
        # Status pill background
        self.status_pill_bg = self.control_canvas.create_rounded_rectangle(
            status_display_x, ip_label_y - entry_height//2,
            status_display_x + 150, ip_label_y + entry_height//2,
            radius=entry_height//2, 
            fill=self.panel_bg,
            outline=self.border_color,
            width=1,
            tags="status_display_bg"
        )
        
        # Status indicator (dot)
        self.server_status_indicator = self.control_canvas.create_oval(
            status_display_x + 15 - 6, ip_label_y - 6,
            status_display_x + 15 + 6, ip_label_y + 6,
            fill="red",  # Start with disconnected
            outline="",
            tags="status_indicator"
        )
        
        # Status pulse animation (initially hidden)
        self.status_pulse = self.control_canvas.create_oval(
            status_display_x + 15 - 8, ip_label_y - 8,
            status_display_x + 15 + 8, ip_label_y + 8,
            outline="red",
            width=2,
            state="hidden",
            tags="status_pulse"
        )
        
        # Status text
        self.server_status_text = self.control_canvas.create_text(
            status_display_x + 40, ip_label_y,
            text="Disconnected",
            font=self.body,
            fill=self.text_color,
            anchor="w",
            tags="status_text"
        )
        
        # Action buttons with refined styling
        button_y = 100
        button_width = 150
        button_height = 40
        button_spacing = 40
        
        # Start button
        start_button_x = 60
        
        # Button shadow for depth
        self.control_canvas.create_rounded_rectangle(
            start_button_x + 3, button_y - button_height//2 + 3,
            start_button_x + button_width + 3, button_y + button_height//2 + 3,
            radius=button_height//2,
            fill=self._ensure_color_compatible(self.colors.shadow_medium),
            outline="",
            tags="start_button_shadow"
        )
        
        # Button background
        self.start_button_bg = self.control_canvas.create_rounded_rectangle(
            start_button_x, button_y - button_height//2,
            start_button_x + button_width, button_y + button_height//2,
            radius=button_height//2, 
            fill=self.colors.success,
            outline="",
            tags="start_button_bg"
        )
        
        # Button text
        self.start_button_text = self.control_canvas.create_text(
            start_button_x + button_width//2, button_y,
            text="START SERVER",
            font=self.button,
            fill="white",
            tags="start_button_text"
        )
        
        # Create button interactivity
        start_button_area = self.control_canvas.create_rectangle(
            start_button_x, button_y - button_height//2,
            start_button_x + button_width, button_y + button_height//2,
            fill="",
            outline="",
            tags="start_button_area"
        )
        
        # Add hover and click effects
        def on_start_enter(e):
            self.control_canvas.itemconfig(self.start_button_bg, fill=self.colors.success_hover)
            
        def on_start_leave(e):
            self.control_canvas.itemconfig(self.start_button_bg, fill=self.colors.success)
            
        self.control_canvas.tag_bind("start_button_area", "<Enter>", on_start_enter)
        self.control_canvas.tag_bind("start_button_area", "<Leave>", on_start_leave)
        self.control_canvas.tag_bind("start_button_area", "<Button-1>", lambda e: self.start_server())
        
        # Store button reference for enabling/disabling
        self.start_button = SimpleObject()
        self.start_button.config = lambda **kwargs: self.control_canvas.itemconfig(
            self.start_button_bg, state=kwargs.get('state', 'normal'))
        
        # Stop button
        stop_button_x = start_button_x + button_width + button_spacing
        
        # Button shadow
        self.control_canvas.create_rounded_rectangle(
            stop_button_x + 3, button_y - button_height//2 + 3,
            stop_button_x + button_width + 3, button_y + button_height//2 + 3,
            radius=button_height//2,
            fill=self._ensure_color_compatible(self.colors.shadow_medium),
            outline="",
            tags="stop_button_shadow"
        )
        
        # Button background
        self.stop_button_bg = self.control_canvas.create_rounded_rectangle(
            stop_button_x, button_y - button_height//2,
            stop_button_x + button_width, button_y + button_height//2,
            radius=button_height//2, 
            fill=self.colors.secondary,
            outline="",
            tags="stop_button_bg"
        )
        
        # Button text
        self.stop_button_text = self.control_canvas.create_text(
            stop_button_x + button_width//2, button_y,
            text="STOP SERVER",
            font=self.button,
            fill="white",
            tags="stop_button_text"
        )
        
        # Create button interactivity
        stop_button_area = self.control_canvas.create_rectangle(
            stop_button_x, button_y - button_height//2,
            stop_button_x + button_width, button_y + button_height//2,
            fill="",
            outline="",
            tags="stop_button_area"
        )
        
        # Add hover and click effects
        def on_stop_enter(e):
            self.control_canvas.itemconfig(self.stop_button_bg, fill=self.colors.secondary_hover)
            
        def on_stop_leave(e):
            self.control_canvas.itemconfig(self.stop_button_bg, fill=self.colors.secondary)
            
        self.control_canvas.tag_bind("stop_button_area", "<Enter>", on_stop_enter)
        self.control_canvas.tag_bind("stop_button_area", "<Leave>", on_stop_leave)
        self.control_canvas.tag_bind("stop_button_area", "<Button-1>", lambda e: self.stop_server())
        
        # Store button reference
        self.stop_button = SimpleObject()
        self.stop_button.config = lambda **kwargs: self.control_canvas.itemconfig(
            self.stop_button_bg, state=kwargs.get('state', 'normal'))
        
        # Pause button
        pause_button_x = stop_button_x + button_width + button_spacing
        
        # Button shadow
        self.control_canvas.create_rounded_rectangle(
            pause_button_x + 3, button_y - button_height//2 + 3,
            pause_button_x + button_width + 3, button_y + button_height//2 + 3,
            radius=button_height//2,
            fill=self._ensure_color_compatible(self.colors.shadow_medium),
            outline="",
            tags="pause_button_shadow"
        )
        
        # Button background
        self.pause_button_bg = self.control_canvas.create_rounded_rectangle(
            pause_button_x, button_y - button_height//2,
            pause_button_x + button_width, button_y + button_height//2,
            radius=button_height//2, 
            fill=self.colors.info,
            outline="",
            tags="pause_button_bg"
        )
        
        # Button text
        self.pause_button_text = self.control_canvas.create_text(
            pause_button_x + button_width//2, button_y,
            text="PAUSE SCREEN",
            font=self.button,
            fill="white",
            tags="pause_button_text"
        )
        
        # Create button interactivity
        pause_button_area = self.control_canvas.create_rectangle(
            pause_button_x, button_y - button_height//2,
            pause_button_x + button_width, button_y + button_height//2,
            fill="",
            outline="",
            tags="pause_button_area"
        )
        
        # Add hover and click effects
        def on_pause_enter(e):
            self.control_canvas.itemconfig(self.pause_button_bg, fill=self.colors.info_hover)
            
        def on_pause_leave(e):
            self.control_canvas.itemconfig(self.pause_button_bg, fill=self.colors.info)
            
        self.control_canvas.tag_bind("pause_button_area", "<Enter>", on_pause_enter)
        self.control_canvas.tag_bind("pause_button_area", "<Leave>", on_pause_leave)
        self.control_canvas.tag_bind("pause_button_area", "<Button-1>", lambda e: self.pause_screen())
        
        # Store button reference
        self.pause_button = SimpleObject()
        self.pause_button.config = lambda **kwargs: self.control_canvas.itemconfig(
            self.pause_button_text, text=kwargs.get('text', "PAUSE SCREEN"))
        
        # Export button
        export_button_x = pause_button_x + button_width + button_spacing
        
        # Button shadow
        self.control_canvas.create_rounded_rectangle(
            export_button_x + 3, button_y - button_height//2 + 3,
            export_button_x + button_width + 3, button_y + button_height//2 + 3,
            radius=button_height//2,
            fill=self._ensure_color_compatible(self.colors.shadow_medium),
            outline="",
            tags="export_button_shadow"
        )
        
        # Button background
        self.export_button_bg = self.control_canvas.create_rounded_rectangle(
            export_button_x, button_y - button_height//2,
            export_button_x + button_width, button_y + button_height//2,
            radius=button_height//2, 
            fill=self.colors.warning,
            outline="",
            tags="export_button_bg"
        )
        
        # Button text
        self.export_button_text = self.control_canvas.create_text(
            export_button_x + button_width//2, button_y,
            text="EXPORT DATA",
            font=self.button,
            fill="white",
            tags="export_button_text"
        )
        
        # Create button interactivity
        export_button_area = self.control_canvas.create_rectangle(
            export_button_x, button_y - button_height//2,
            export_button_x + button_width, button_y + button_height//2,
            fill="",
            outline="",
            tags="export_button_area"
        )
        
        # Add hover and click effects
        def on_export_enter(e):
            self.control_canvas.itemconfig(self.export_button_bg, fill=self.colors.warning_hover)
            
        def on_export_leave(e):
            self.control_canvas.itemconfig(self.export_button_bg, fill=self.colors.warning)
            
        self.control_canvas.tag_bind("export_button_area", "<Enter>", on_export_enter)
        self.control_canvas.tag_bind("export_button_area", "<Leave>", on_export_leave)
        self.control_canvas.tag_bind("export_button_area", "<Button-1>", lambda e: self.export_data())
        
        # Store button reference
        self.export_button = self.control_canvas
        
        # Initialize button states
        self.start_button.itemconfig = lambda **kwargs: self.control_canvas.itemconfig(
            self.start_button_bg, state=kwargs.get('state', 'normal'))
            
        self.stop_button.itemconfig = lambda **kwargs: self.control_canvas.itemconfig(
            self.stop_button_bg, state=kwargs.get('state', 'normal'))
        
        # Disable stop button initially
        self.stop_button.config(state="disabled")
        
        # Version number - professional touch
        self.control_canvas.create_text(
            1230, 150,
            text="v1.5.2",
            font=self.caption,
            fill=self.secondary_text,
            anchor="e",
            tags="version"
        )
        
        # Copyright - professional touch
        self.control_canvas.create_text(
            60, 150,
            text="© 2023 Guardian Technologies",
            font=self.caption,
            fill=self.secondary_text,
            anchor="w",
            tags="copyright"
        )
    
    def export_data(self):
        """Export monitoring data to file"""
        # This would typically save data to a file, for demo we'll just show a message
        messagebox.showinfo("Export Data", "Activity data would be exported to a file.\nThis is a placeholder for the actual export functionality.")
        
    def start_status_pulse_animation(self):
        """Animate the status indicator pulse effect"""
        indicator_size = 12
        pulse_size = indicator_size + 4
        max_pulse_size = indicator_size + 12
        x = int(self.control_canvas.coords(self.server_status_indicator)[0] + indicator_size/2)
        y = int(self.control_canvas.coords(self.server_status_indicator)[1] + indicator_size/2)
        
        def update_pulse(size):
            self.control_canvas.coords(
                self.server_status_pulse,
                x - size/2, y - size/2,
                x + size/2, y + size/2
            )
            
            # Also update opacity based on size
            alpha = int(128 - (size - pulse_size) * 10)
            if alpha < 0: alpha = 0
            
            # Get current color
            current_color = self.control_canvas.itemcget(self.server_status_indicator, "fill")
            
            # Set pulse color to match indicator with transparency
            if current_color:
                if current_color.startswith("#"):
                    self.control_canvas.itemconfig(
                        self.server_status_pulse, 
                        outline=current_color + f"{alpha:02x}"
                    )
        
        # Start animation cycle
        self.animate(
            "status_pulse", pulse_size, max_pulse_size, 1.5,
            update_pulse, "ease_in_out_quad",
            lambda: self.animate(
                "status_pulse", max_pulse_size, pulse_size, 1.5,
                update_pulse, "ease_in_out_quad",
                lambda: self.start_status_pulse_animation()
            )
        )
    
    def draw_control_panel(self):
        """Draw the control panel background"""
        # Get the width and height
        width = self.control_frame.winfo_width()
        if width < 100:
            width = 1260  # Default width if not rendered yet
            
        height = self.control_frame.winfo_height()
        if height < 50:
            height = 180  # Default height
            
        # Create a panel background
        self.control_canvas.create_rectangle(
            0, 0, width, height, 
            fill=self.secondary_bg, 
            outline="",
            tags="control_bg"
        )
        
        # Add subtle separator line at top
        self.control_canvas.create_line(
            10, 5, width-10, 5,
            fill=self.border_color,
            tags="control_separator"
        )

# Add this at the bottom of the file
if __name__ == "__main__":
    root = tk.Tk()
    app = FuturisticParentMonitorApp(root)
    # Prevent the application from closing instantly by adding mainloop call
    root.mainloop()
