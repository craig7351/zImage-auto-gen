import customtkinter as ctk
import os
import glob
import threading
import concurrent.futures
from PIL import Image, ImageTk

class ImageViewer(ctk.CTkToplevel):
    def __init__(self, parent, initial_dir="."):
        super().__init__(parent)
        self.title("Image Viewer")
        self.geometry("1400x800")
        
        self.current_dir = initial_dir
        self.image_files = []
        self.thumbnails = {} # path -> CTkImage
        self.current_index = -1
        self.thumbnail_size = 100
        
        # Optimization
        self._resize_timer = None
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        self.thumb_buttons = []
        
        self.create_layout()
        self.load_images_in_thread()
        
        # Key bindings
        self.bind("<Left>", self.prev_image)
        self.bind("<Right>", self.next_image)
        self.bind("<Up>", self.prev_image)
        self.bind("<Down>", self.next_image)

    def destroy(self):
        self.pool.shutdown(wait=False)
        super().destroy()
        
    def create_layout(self):
        # 1. Toolbar (Top)
        self.toolbar = ctk.CTkFrame(self, height=40)
        self.toolbar.pack(side="top", fill="x", padx=5, pady=5)
        
        self.btn_open = ctk.CTkButton(self.toolbar, text="Open Folder", command=self.open_folder, width=100)
        self.btn_open.pack(side="left", padx=5)
        
        self.slider_label = ctk.CTkLabel(self.toolbar, text="Thumbnail Size:")
        self.slider_label.pack(side="left", padx=(20, 5))
        
        self.slider = ctk.CTkSlider(self.toolbar, from_=50, to=200, number_of_steps=150, command=self.on_slider_change)
        self.slider.set(self.thumbnail_size)
        self.slider.pack(side="left", padx=5)
        
        self.btn_refresh = ctk.CTkButton(self.toolbar, text="Refresh", command=self.refresh_folder, width=80)
        self.btn_refresh.pack(side="left", padx=20)
        
        # Zoom Dropdown
        ctk.CTkLabel(self.toolbar, text="Zoom:").pack(side="left", padx=(20, 5))
        self.zoom_combo = ctk.CTkComboBox(self.toolbar, values=["Fit", "50%", "75%", "100%", "150%", "200%"], width=80, command=lambda v: self.show_image(self.current_index))
        self.zoom_combo.set("75%")
        self.zoom_combo.pack(side="left", padx=5)
        
        self.status_label = ctk.CTkLabel(self.toolbar, text="Ready")
        self.status_label.pack(side="right", padx=10)

        # Main Content Split
        self.panes = ctk.CTkFrame(self, fg_color="transparent")
        self.panes.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        
        # 2. Left Panel (Thumbnails)
        self.left_panel = ctk.CTkFrame(self.panes, width=300)
        self.left_panel.pack(side="left", fill="y", padx=(0, 5))
        
        self.thumb_scroll = ctk.CTkScrollableFrame(self.left_panel, width=280)
        self.thumb_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 3. Center Panel (Preview)
        # Using ScrollableFrame to allow scrolling when zoomed in
        self.preview_panel = ctk.CTkScrollableFrame(self.panes, fg_color="black") 
        self.preview_panel.pack(side="left", fill="both", expand=True, padx=5)
        
        self.preview_image_label = ctk.CTkLabel(self.preview_panel, text="")
        self.preview_image_label.pack(expand=True, fill="both", anchor="center") 
        
        # 4. Right Panel (Info)
        self.right_panel = ctk.CTkFrame(self.panes, width=300)
        self.right_panel.pack(side="right", fill="y", padx=(5, 0))
        

        
        self.info_header = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.info_header.pack(fill="x", pady=5)
        
        ctk.CTkLabel(self.info_header, text="Prompt Info").pack(side="left", padx=5)
        ctk.CTkButton(self.info_header, text="Copy", width=60, height=24, command=self.copy_prompt).pack(side="right", padx=5)
        
        self.info_text = ctk.CTkTextbox(self.right_panel, wrap="word")
        self.info_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.file_info_label = ctk.CTkLabel(self.right_panel, text="", anchor="w", justify="left")
        self.file_info_label.pack(fill="x", padx=5, pady=5)

    def open_folder(self):
        d = ctk.filedialog.askdirectory(initialdir=self.current_dir)
        if d:
            self.current_dir = d
            self.load_images_in_thread()

    def refresh_folder(self):
        self.load_images_in_thread()
        
    def load_images_in_thread(self):
        # Clear existing
        for widget in self.thumb_scroll.winfo_children():
            widget.destroy()
        self.thumb_buttons = []
        self.status_label.configure(text="Loading...")
        
        thread = threading.Thread(target=self._scan_and_load)
        thread.start()
        
    def _scan_and_load(self):
        if not os.path.exists(self.current_dir): return
        
        # Scan for images 
        exts = ["*.png", "*.jpg", "*.jpeg", "*.webp"]
        files = []
        for ext in exts:
            # On Windows, both *.png and *.PNG might return same files depending on python/OS
            # To be safe, we collect all and deduplicate by absolute path
            chunk = glob.glob(os.path.join(self.current_dir, ext))
            files.extend(chunk)
            chunk_upper = glob.glob(os.path.join(self.current_dir, ext.upper()))
            files.extend(chunk_upper)
            
        # Deduplicate
        unique_files = list(set([os.path.abspath(f) for f in files]))
        
        # Sort by mtime (newest first)
        unique_files.sort(key=os.path.getmtime, reverse=True)
        self.image_files = unique_files
        
        # Update UI first
        self.after(50, lambda: self.status_label.configure(text=f"Found {len(self.image_files)} images"))
        self.after(100, self._start_thumbnail_generation)

    def _start_thumbnail_generation(self):
        # Create buttons first (fast)
        for idx, fpath in enumerate(self.image_files):
            btn = ctk.CTkButton(self.thumb_scroll, 
                                text=os.path.basename(fpath), 
                                compound="top",
                                width=self.thumbnail_size + 20,
                                fg_color="transparent", border_width=1,
                                command=lambda i=idx: self.show_image(i))
            btn.pack(pady=2, fill="x")
            self.thumb_buttons.append(btn)
        
        # Submit tasks to thread pool
        for idx, (fpath, btn) in enumerate(zip(self.image_files, self.thumb_buttons)):
            self.pool.submit(self._generate_thumb, idx, fpath, btn, self.thumbnail_size)
            
        if self.image_files:
            self.after(100, lambda: self.show_image(0))

    def _generate_thumb(self, idx, fpath, btn, target_size):
        try:
            # Prepare PIL Image in background thread
            with Image.open(fpath) as img:
                img.load() # Ensure data is loaded
                img.thumbnail((target_size, target_size))
                thumb_ready = img.copy() # Detach from file
                
            def update_btn_main_thread():
                if btn.winfo_exists():
                    # Create CTkImage in Main Thread
                    ctk_img = ctk.CTkImage(light_image=thumb_ready, dark_image=thumb_ready, size=thumb_ready.size)
                    btn.configure(image=ctk_img)
                    btn.image = ctk_img # Keep reference to prevent GC
                        
            self.after(0, update_btn_main_thread)
        except Exception as e:
            print(f"Thumb error: {e}")

    def on_slider_change(self, val):
        self.thumbnail_size = int(val)
        if self._resize_timer:
            self.after_cancel(self._resize_timer)
        self._resize_timer = self.after(500, self.refresh_thumbnails_only)

    def refresh_thumbnails_only(self):
        self._resize_timer = None
        # Submit new resize tasks for existing buttons
        # We don't need to recreate buttons, just update images
        for idx, (fpath, btn) in enumerate(zip(self.image_files, self.thumb_buttons)):
             if btn.winfo_exists():
                 btn.configure(width=self.thumbnail_size + 20)
                 self.pool.submit(self._generate_thumb, idx, fpath, btn, self.thumbnail_size)

    def show_image(self, index):
        if not (0 <= index < len(self.image_files)): return
        
        self.current_index = index
        fpath = self.image_files[index]
        
        # Updates buttons highlight
        for i, btn in enumerate(self.thumb_buttons):
            if i == index: btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
            else: btn.configure(fg_color="transparent")
            
        # Load main image
        try:
            img = Image.open(fpath)
            
            # Zoom Logic
            zoom_mode = self.zoom_combo.get()
            
            if zoom_mode == "Fit":
                # For fit, we use the visible size of the scrollable frame
                # Note: winfo_width might be small if not pack yet, so fallback default
                display_w = self.preview_panel.winfo_width()
                display_h = self.preview_panel.winfo_height()
                
                if display_w < 50: display_w = 800
                if display_h < 50: display_h = 600
                
                # Account for scrollbar space approx
                display_w -= 20 
                display_h -= 20
                
                img_ratio = img.width / img.height
                panel_ratio = display_w / display_h
                
                if img_ratio > panel_ratio:
                    w = display_w
                    h = int(w / img_ratio)
                else:
                    h = display_h
                    w = int(h * img_ratio)
            else:
                # Percentage
                scale = int(zoom_mode.replace("%", "")) / 100.0
                w = int(img.width * scale)
                h = int(img.height * scale)
                
            ctk_full = ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
            self.preview_image_label.configure(image=ctk_full, text="")
            self.preview_image_label.image = ctk_full # keep ref
            
            # Reset scroll position logic could be added here if needed
            # self.preview_panel._parent_canvas.yview_moveto(0) (Private API, maybe skip)

            # Update info
            file_size_kb = os.path.getsize(fpath) / 1024
            info_str = f"File: {os.path.basename(fpath)}\nRes: {img.width}x{img.height}\nSize: {file_size_kb:.1f} KB"
            self.file_info_label.configure(text=info_str)
            
            # Load prompt txt
            base_path = os.path.splitext(fpath)[0]
            txt_path = base_path + ".txt"
            
            prompt_content = "No prompt file found."
            if os.path.exists(txt_path):
                with open(txt_path, "r", encoding="utf-8") as f:
                    prompt_content = f.read()
            
            self.info_text.configure(state="normal")
            self.info_text.delete("0.0", "end")
            self.info_text.insert("0.0", prompt_content)
            self.info_text.configure(state="disabled")
            
        except Exception as e:
            print(e)

    def copy_prompt(self):
        content = self.info_text.get("0.0", "end").strip()
        if content:
            self.clipboard_clear()
            self.clipboard_append(content)
            self.status_label.configure(text="Prompt Copied!")
            self.after(2000, lambda: self.status_label.configure(text="Ready"))

    def prev_image(self, event=None):
        if self.current_index > 0:
            self.show_image(self.current_index - 1)
            
    def next_image(self, event=None):
        if self.current_index < len(self.image_files) - 1:
            self.show_image(self.current_index + 1)
