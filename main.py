import customtkinter as ctk
import threading
import json
import os
import sys
import glob
import time
import re
import random
from tkinter import filedialog, messagebox
from PIL import Image
from PIL import Image
from comfy_api import ComfyClient
from image_viewer import ImageViewer

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# UI Translations
TRANSLATIONS = {
    "en": {
        "title": "ComfyUI Client - Z Image Turbo",
        "server": "Server:",
        "output": "Output:",
        "browse": "Browse",
        "fixed_prompt": "Fixed Prompt:",
        "preview": "Prompt Preview:",
        "sync": "Sync",
        "generate": "GENERATE",
        "stop": "STOP",
        "logs": "Logs:",
        "generating": "Generating...",
        "error_conn": "Error: IP and Port are required.",
        "ready": "GENERATE",
        "no_wildcards": "No wildcards found.",
        "batch": "Count:",
        "conn_start": "Connecting...",
        "stopped": "Generation stopped by user.",
        "download_log": "Download Log",
        "webp_convert": "Convert WebP",
        "compression": "Compression:",
        "converted": "Converted to WebP (Q={})",
        "viewer": "Image Viewer",
        "export_wc": "Export Wildcards",
        "import_wc": "Import Wildcards",
        "export_success": "Wildcards exported successfully!",
        "import_success": "Wildcards imported successfully! Refreshed.",
        "import_confirm": "This will overwrite current wildcard files. Continue?"
    },
    "zh": {
        "title": "ComfyUI 客戶端 - Z Image Turbo",
        "server": "伺服器:",
        "output": "輸出目錄:",
        "browse": "瀏覽",
        "fixed_prompt": "固定提示詞:",
        "preview": "提示詞預覽:",
        "sync": "同步",
        "generate": "開始生成",
        "stop": "停止",
        "logs": "執行紀錄:",
        "generating": "生成中...",
        "error_conn": "錯誤: 需要輸入 IP 和 Port",
        "ready": "開始生成",
        "no_wildcards": "找不到 Wildcards 資料。",
        "batch": "張數:",
        "conn_start": "連線中...",
        "stopped": "已由使用者停止生成。",
        "download_log": "下載紀錄",
        "webp_convert": "轉 WebP",
        "compression": "壓縮率:",
        "converted": "已轉為 WebP (品質={})",
        "viewer": "看圖軟體",
        "export_wc": "匯出設定",
        "import_wc": "匯入設定",
        "export_success": "Wildcards 匯出成功！",
        "import_success": "Wildcards 匯入成功！已重新整理。",
        "import_confirm": "這將會覆寫目前的 Wildcard 設定檔。確定要繼續嗎？"
    }
}

# Label Translations
LABEL_MAP_ZH = {
    "subject": "1. 主題 (Subject)",
    "face": "2. 臉部 (Face)",
    "hair": "3. 髮型 (Hair)",
    "body": "4. 身材 (Body)",
    "outfit": "5. 服裝 (Outfit)",
    "pose": "6. 姿勢 (Pose)",
    "scene": "7. 場景 (Scene)",
    "camera": "8. 鏡頭 (Camera)",
    "lighting": "9. 光影 (Lighting)",
    "style": "10. 風格 (Style)",
    "control": "11. 控制 (Control)",
    "negative": "12. 負面 (Negative)",
    
    "count": "人數", "type": "種族", "role": "職業/角色", "age": "年齡", "ethnicity": "膚色/種族", "vibe": "氣質",
    "expression": "表情", "eyes_color": "瞳孔顏色", "eyes_shape": "眼型", "makeup": "妝容", "skin": "膚質", "special_marks": "特徵", "gaze": "視線",
    "color": "髮色", "length": "長度", "style": "髮型", "details": "細節",
    "height": "身高", "build": "體型", "posture": "儀態", "hands": "手部",
    "sets/casual": "休閒套裝", "sets/school": "制服套裝", "sets/business": "職場套裝", "sets/dress": "禮服/洋裝", "sets/sporty": "運動套裝", "sets/traditional": "傳統服飾", "sets/onepiece": "連身裝",
    "garments/top": "上衣", "garments/bottom": "下身", "garments/shoes": "鞋子", "garments/accessories": "飾品",
    "attributes/color_palette": "色系", "attributes/material": "材質",
    "base": "基礎/動作", "hand_pose": "手勢", "interaction": "互動", "dynamic": "動態",
    "location/indoor": "室內", "location/outdoor": "室外",
    "time": "時間", "weather": "天氣", "season": "季節", "background_detail": "背景細節", "props": "物件",
    "shot_type": "景別", "angle": "角度", "lens": "鏡頭", "composition": "構圖", "depth_of_field": "景深",
    "source": "光源", "mood": "氛圍", "color_temp": "色溫", "contrast": "對比",
    "medium": "媒材", "genre": "流派", "render": "渲染", "art_direction": "美術", "quality_tags": "品質標籤",
    "fixed_identity": "固定角色", "forbidden_mix": "禁止標籤", "prompt_syntax": "語法"
}

BATCH_OPTIONS = ["1", "4", "8", "16", "32", "64", "128", "256", "512"]

CATEGORIES_ORDER = ["subject", "face", "hair", "body", "outfit", "pose", "scene", "camera", "lighting", "style", "control", "negative"]

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.lang = "zh" 
        self.wildcards = {} 
        self.selections = {} 
        self.stop_requested = False
        
        self.current_category = None
        self.nav_buttons = {} 
        self.category_frames = {} 
        self.checkbox_vars = {} 
        self.category_frames = {} 
        self.category_frames = {} 
        self.checkbox_vars = {} 
        self.comboboxes = {} 
        self.group_vars = {}
        self.viewer_window = None

        self.title("ComfyUI Client")
        self.geometry("1000x850") 

        self.load_workflow_template()
        
        self.create_widgets()
        self.load_wildcards_and_refresh()

    def get_text(self, key):
        return TRANSLATIONS.get(self.lang, TRANSLATIONS["en"]).get(key, key)
        
    def get_label(self, key):
        if self.lang == "zh":
            if key in LABEL_MAP_ZH: return LABEL_MAP_ZH[key]
            return LABEL_MAP_ZH.get(key, key.replace("_", " ").title())
        return key.replace("_", " ").title()

    def get_category_label(self, cat):
        if self.lang == "zh":
            return LABEL_MAP_ZH.get(cat, cat.title())
        return cat.title()

    def load_workflow_template(self):
        try:
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(application_path, "workflow_template.json")
            with open(json_path, "r", encoding="utf-8") as f:
                self.workflow_data = json.load(f)
        except Exception as e:
            print(f"Error loading workflow: {e}")

    def load_wildcards_and_refresh(self):
        self.wildcards = {}
        self.selections = {}
        self.checkbox_vars = {}
        self.comboboxes = {}
        self.group_vars = {}
        
        dir_name = "wildcards_zh" if self.lang == "zh" else "wildcards_en"
        base_dir = dir_name
        if not os.path.exists(base_dir):
            if os.path.exists("wildcards"): base_dir = "wildcards"
            
        if os.path.exists(base_dir):
            for root, dirs, files in os.walk(base_dir):
                rel_path = os.path.relpath(root, base_dir)
                if rel_path == ".": continue
                
                parts = rel_path.split(os.sep)
                top_category = parts[0]
                
                if top_category not in self.wildcards:
                    self.wildcards[top_category] = {}
                
                sub_path = "/".join(parts[1:]) 
                
                for file in files:
                    if file.endswith(".txt"):
                        key = os.path.splitext(file)[0]
                        if sub_path:
                            key = f"{sub_path}/{key}"
                        
                        full_path = os.path.join(root, file)
                        with open(full_path, "r", encoding="utf-8") as f:
                            lines = [line.strip() for line in f.readlines() if line.strip()]
                            lines.insert(0, "") 
                            self.wildcards[top_category][key] = lines
        
        self.rebuild_navigation()

    def create_widgets(self):
        # 1. Config Area
        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.pack(pady=5, padx=10, fill="x")
        
        self.lang_switch = ctk.CTkSegmentedButton(self.config_frame, values=["English", "中文"], command=self.on_lang_change)
        self.lang_switch = ctk.CTkSegmentedButton(self.config_frame, values=["English", "中文"], command=self.on_lang_change)
        self.lang_switch.set("中文")
        self.lang_switch.pack(side="left", padx=5)

        self.viewer_btn = ctk.CTkButton(self.config_frame, text="Viewer", width=80, command=self.open_viewer)
        self.viewer_btn.pack(side="left", padx=5)

        self.import_btn = ctk.CTkButton(self.config_frame, text="Import", width=80, command=self.import_wildcards)
        self.import_btn.pack(side="left", padx=5)
        
        self.export_btn = ctk.CTkButton(self.config_frame, text="Export", width=80, command=self.export_wildcards)
        self.export_btn.pack(side="left", padx=5)

        self.server_label = ctk.CTkLabel(self.config_frame, text="")
        self.server_label.pack(side="left", padx=5)
        
        self.ip_entry = ctk.CTkEntry(self.config_frame, width=100)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.pack(side="left", padx=2)
        
        ctk.CTkLabel(self.config_frame, text=":").pack(side="left")
        self.port_entry = ctk.CTkEntry(self.config_frame, width=60)
        self.port_entry.insert(0, "8188")
        self.port_entry.pack(side="left", padx=2)
        
        self.batch_label = ctk.CTkLabel(self.config_frame, text="Batch:")
        self.batch_label.pack(side="left", padx=(15, 5))
        self.batch_combo = ctk.CTkComboBox(self.config_frame, values=BATCH_OPTIONS, width=70)
        self.batch_combo.set("1")
        self.batch_combo.pack(side="left", padx=2)

        # WebP Settings
        self.webp_var = ctk.BooleanVar(value=True)
        self.webp_chk = ctk.CTkCheckBox(self.config_frame, text="WebP", variable=self.webp_var, width=60)
        self.webp_chk.pack(side="left", padx=(15, 5))
        
        self.comp_label = ctk.CTkLabel(self.config_frame, text="Comp:")
        self.comp_label.pack(side="left", padx=2)
        
        self.comp_combo = ctk.CTkComboBox(self.config_frame, values=["0%", "20%", "40%", "60%", "80%", "100%"], width=70)
        self.comp_combo.set("20%")
        self.comp_combo.pack(side="left", padx=2)
        
        self.browse_btn = ctk.CTkButton(self.config_frame, text="", width=80, command=self.browse_output)
        self.browse_btn.pack(side="right", padx=5)
        
        self.output_entry = ctk.CTkEntry(self.config_frame, width=200)
        self.output_entry.insert(0, "../output")
        self.output_entry.pack(side="right", padx=5)
        self.output_label = ctk.CTkLabel(self.config_frame, text="")
        self.output_label.pack(side="right", padx=5)

        # 2. Main Content
        self.main_split = ctk.CTkFrame(self, fg_color="transparent")
        self.main_split.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Left Panel (Fixed Width)
        self.left_panel = ctk.CTkFrame(self.main_split, width=450)
        self.left_panel.pack(side="left", fill="both", expand=False, padx=(0, 5))
        
        # Right Panel
        self.right_panel = ctk.CTkFrame(self.main_split)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # --- Right Panel Widgets ---
        
        # Fixed Prompt
        self.fixed_prompt_label = ctk.CTkLabel(self.right_panel, text="", anchor="w")
        self.fixed_prompt_label.pack(pady=(5,0), anchor="w", padx=5)
        
        self.fixed_prompt_text = ctk.CTkTextbox(self.right_panel, height=60)
        self.fixed_prompt_text.pack(pady=5, fill="x", padx=5)
        self.fixed_prompt_text.bind("<KeyRelease>", lambda e: self.update_prompt_text())

        # Preview
        self.preview_label = ctk.CTkLabel(self.right_panel, text="", anchor="w")
        self.preview_label.pack(pady=5, anchor="w", padx=5)
        
        self.prompt_text = ctk.CTkTextbox(self.right_panel, height=200)
        self.prompt_text.pack(pady=5, fill="x", padx=5)
        
        self.btn_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.btn_frame.pack(pady=5, fill="x", padx=5)
        
        self.refresh_btn = ctk.CTkButton(self.btn_frame, text="", command=self.update_prompt_text)
        self.refresh_btn.pack(side="left", fill="x", expand=True, padx=2)
        
        self.generate_btn = ctk.CTkButton(self.btn_frame, text="", fg_color="green", height=40, command=self.start_generation)
        self.generate_btn.pack(side="left", fill="x", expand=True, padx=2)
        
        self.stop_btn = ctk.CTkButton(self.btn_frame, text="", fg_color="red", hover_color="darkred", height=40, command=self.stop_generation)
        self.stop_btn.pack(side="left", padx=2)

        self.log_header_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.log_header_frame.pack(pady=(10,0), fill="x", padx=5)

        self.logs_label = ctk.CTkLabel(self.log_header_frame, text="", anchor="w")
        self.logs_label.pack(side="left")
        
        self.download_log_btn = ctk.CTkButton(self.log_header_frame, text="", width=100, height=24, command=self.download_log)
        self.download_log_btn.pack(side="right")
        
        self.log_text = ctk.CTkTextbox(self.right_panel)
        self.log_text.pack(pady=5, fill="both", expand=True, padx=5)
        
        # --- Left Panel Widgets (Nav + Content) ---
        self.nav_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.nav_frame.pack(side="top", fill="x", pady=5)

    def rebuild_navigation(self):
        for widget in self.nav_frame.winfo_children(): widget.destroy()
        for widget in self.left_panel.winfo_children():
            if widget != self.nav_frame: widget.destroy()
        
        self.category_frames.clear()
        self.nav_buttons.clear()
        
        if not self.wildcards:
            ctk.CTkLabel(self.left_panel, text=self.get_text("no_wildcards")).pack(pady=20)
            return

        sorted_cats = sorted(self.wildcards.keys())
        sorted_cats = sorted(sorted_cats, key=lambda x: CATEGORIES_ORDER.index(x) if x in CATEGORIES_ORDER else 99)

        # Nav Buttons
        cols = 3
        for i, category in enumerate(sorted_cats):
            btn_text = self.get_category_label(category)
            row, col = i // cols, i % cols
            btn = ctk.CTkButton(self.nav_frame, text=btn_text, fg_color="gray", command=lambda c=category: self.show_category(c))
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
            self.nav_buttons[category] = btn

            # Content Frame
            frame = ctk.CTkScrollableFrame(self.left_panel)
            self.category_frames[category] = frame
            
            # Content items
            items = self.wildcards[category]
            sorted_keys = sorted(items.keys())
            
            for key in sorted_keys:
                options = items[key]
                label_text = self.get_label(key)
                full_key = f"{category}/{key}" 
                
                row_frame = ctk.CTkFrame(frame, fg_color="transparent")
                row_frame.pack(side="top", fill="x", pady=2)
                
                # Group Dropdown
                group_opts = [""] + [str(i) for i in range(1, 11)]
                group_var = ctk.StringVar(value="")
                self.group_vars[full_key] = group_var
                group_cbox = ctk.CTkComboBox(row_frame, values=group_opts, width=60, variable=group_var)
                group_cbox.pack(side="left", padx=(5,2))
                
                rand_var = ctk.IntVar()
                seq_var = ctk.IntVar()
                self.checkbox_vars[full_key] = {"r": rand_var, "s": seq_var}

                cb_r = ctk.CTkCheckBox(row_frame, text="?", width=24, checkbox_width=18, variable=rand_var,
                                       command=lambda k=full_key: self.on_checkbox_toggle(k, "r"))
                cb_r.pack(side="left", padx=(5,2))
                
                cb_s = ctk.CTkCheckBox(row_frame, text="S", width=24, checkbox_width=18, variable=seq_var,
                                       command=lambda k=full_key: self.on_checkbox_toggle(k, "s"))
                cb_s.pack(side="left", padx=(0,5))
                
                ctk.CTkLabel(row_frame, text=label_text, width=80, anchor="e").pack(side="left", padx=2)
                
                combo = ctk.CTkComboBox(row_frame, values=options, width=200, 
                                        command=lambda val, k=full_key: self.on_combo_change(k, val))
                combo.set("")
                combo.pack(side="left", fill="x", expand=True, padx=5)
                
                self.comboboxes[full_key] = combo
                self.selections[full_key] = ""

        for i in range(cols): self.nav_frame.grid_columnconfigure(i, weight=1)

        self.update_ui_text()
        if sorted_cats: self.show_category(sorted_cats[0])

    def on_checkbox_toggle(self, key, mode):
        vars = self.checkbox_vars[key]
        r_val = vars["r"].get()
        s_val = vars["s"].get()
        combo = self.comboboxes[key]

        if mode == "r" and r_val == 1:
            vars["s"].set(0) # Uncheck S
            self.selections[key] = f"__RANDOM__{key}__"
            combo.configure(state="disabled")
        elif mode == "s" and s_val == 1:
            vars["r"].set(0) # Uncheck R
            self.selections[key] = f"__SEQUENTIAL__{key}__"
            combo.configure(state="disabled")
        else:
            self.selections[key] = combo.get()
            combo.configure(state="normal")
            
        self.update_prompt_text()

    def on_combo_change(self, key, value):
        vars = self.checkbox_vars[key]
        if vars["r"].get() == 0 and vars["s"].get() == 0:
            self.selections[key] = value
            self.update_prompt_text()

    def show_category(self, category):
        for frame in self.category_frames.values(): frame.pack_forget()
        if category in self.category_frames:
            self.category_frames[category].pack(side="top", fill="both", expand=True, padx=2, pady=2)
        
        self.current_category = category
        for cat, btn in self.nav_buttons.items():
            if cat == category: btn.configure(fg_color=["#3B8ED0", "#1F6AA5"]) 
            else: btn.configure(fg_color="transparent", border_width=1, text_color=("gray10", "gray90")) 

    def on_lang_change(self, value):
        self.lang = "zh" if value == "中文" else "en"
        self.update_ui_text()
        self.load_wildcards_and_refresh()
        self.prompt_text.delete("0.0", "end")

    def open_viewer(self):
        if self.viewer_window is None or not self.viewer_window.winfo_exists():
            # Use current output dir as default
            current_out = self.output_entry.get()
            if not os.path.isdir(current_out): current_out = "."
            self.viewer_window = ImageViewer(self, initial_dir=current_out)
        else:
            self.viewer_window.focus()

    def update_ui_text(self):
        self.title(self.get_text("title"))
        self.server_label.configure(text=self.get_text("server"))
        self.output_label.configure(text=self.get_text("output"))
        self.browse_btn.configure(text=self.get_text("browse"))
        self.viewer_btn.configure(text=self.get_text("viewer"))
        self.fixed_prompt_label.configure(text=self.get_text("fixed_prompt"))
        self.preview_label.configure(text=self.get_text("preview"))
        self.refresh_btn.configure(text=self.get_text("sync"))
        self.generate_btn.configure(text=self.get_text("ready"))
        self.stop_btn.configure(text=self.get_text("stop"))
        self.logs_label.configure(text=self.get_text("logs"))
        self.download_log_btn.configure(text=self.get_text("download_log"))
        self.batch_label.configure(text=self.get_text("batch"))
        self.webp_chk.configure(text=self.get_text("webp_convert"))
        self.comp_label.configure(text=self.get_text("compression"))

        self.export_btn.configure(text=self.get_text("export_wc"))
        self.import_btn.configure(text=self.get_text("import_wc"))

    def export_wildcards(self):
        f = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not f: return
        
        base_dir = "wildcards_zh" if self.lang == "zh" else "wildcards_en"
        data = {}
        
        if os.path.exists(base_dir):
            for root, dirs, files in os.walk(base_dir):
                for file in files:
                    if file.endswith(".txt"):
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, base_dir)
                        # Normalize separators to / for JSON
                        key = rel_path.replace(os.sep, "/")
                        try:
                            with open(full_path, "r", encoding="utf-8") as tf:
                                lines = [l.strip() for l in tf.readlines() if l.strip()]
                                data[key] = lines
                        except Exception as e:
                            print(f"Error reading {full_path}: {e}")
                            
        try:
            with open(f, "w", encoding="utf-8") as jf:
                json.dump(data, jf, indent=2, ensure_ascii=False)
            messagebox.showinfo("Success", self.get_text("export_success"))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def import_wildcards(self):
        f = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not f: return
        
        if not messagebox.askyesno("Confirm", self.get_text("import_confirm")):
            return
            
        base_dir = "wildcards_zh" if self.lang == "zh" else "wildcards_en"
        
        try:
            with open(f, "r", encoding="utf-8") as jf:
                data = json.load(jf)
                
            for key, lines in data.items():
                # key is rel path e.g. "scene/location/outdoor.txt" or just "outdoor.txt" if flat?
                # current logic supports nested dirs.
                # ensure key uses correct sep
                norm_key = key.replace("/", os.sep)
                target_path = os.path.join(base_dir, norm_key)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                
                with open(target_path, "w", encoding="utf-8") as tf:
                    # join with newlines
                    content = "\n".join(lines)
                    tf.write(content)
                    
            self.load_wildcards_and_refresh()
            messagebox.showinfo("Success", self.get_text("import_success"))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_prompt_text(self):
        bucket = {c: [] for c in CATEGORIES_ORDER}
        others = []
        
        for full_key, val in self.selections.items():
            if not val: continue
            
            display_val = val
            if val.startswith("__RANDOM__"):
                label_key = full_key.split("/", 1)[1]
                display_val = f"<Random: {self.get_label(label_key)}>"
            elif val.startswith("__SEQUENTIAL__"):
                label_key = full_key.split("/", 1)[1]
                display_val = f"<Seq: {self.get_label(label_key)}>"

            cat = full_key.split("/")[0]
            if cat in bucket: bucket[cat].append(display_val)
            else: others.append(display_val)
        
        final_parts = []
        for cat in CATEGORIES_ORDER:
            if bucket[cat]: final_parts.extend(bucket[cat])
        final_parts.extend(others)
        
        fixed = self.fixed_prompt_text.get("0.0", "end").strip()
        
        prompt_parts = []
        if fixed: prompt_parts.append(fixed)
        if final_parts: prompt_parts.extend(final_parts)
            
        prompt_str = ", ".join(prompt_parts)
        self.prompt_text.delete("0.0", "end")
        self.prompt_text.insert("0.0", prompt_str)

    def browse_output(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, directory)

    def download_log(self):
        content = self.log_text.get("0.0", "end")
        if not content.strip(): return
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        initial_file = f"log_{timestamp}.txt"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=initial_file,
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.log(f"Log saved to: {file_path}")
            except Exception as e:
                self.log(f"Error saving log: {e}")

    def log(self, message):
        try:
            self.log_text.configure(state="normal")
            self.log_text.insert("end", message + "\n")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")
        except: pass

    def stop_generation(self):
        self.stop_requested = True
        self.log(self.get_text("stopped"))

    def start_generation(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        output_dir = self.output_entry.get()
        
        bucket = {c: [] for c in CATEGORIES_ORDER}
        others = []
        for full_key, val in self.selections.items():
            if not val: continue
            cat = full_key.split("/")[0]
            if cat in bucket: bucket[cat].append(val)
            else: others.append(val)
        
        final_parts = []
        for cat in CATEGORIES_ORDER:
            if bucket[cat]: final_parts.extend(bucket[cat])
        final_parts.extend(others)
        
        fixed = self.fixed_prompt_text.get("0.0", "end").strip()
        prompt_parts = []
        if fixed: prompt_parts.append(fixed)
        if final_parts: prompt_parts.extend(final_parts)
        
        raw_prompt_template = ", ".join(prompt_parts)
        
        try: batch_count = int(self.batch_combo.get())
        except: batch_count = 1

        if not ip or not port:
            self.log(self.get_text("error_conn"))
            return

        self.stop_requested = False
        self.generate_btn.configure(state="disabled", text=self.get_text("generating"))
        
        do_webp = self.webp_var.get()
        comp_val_str = self.comp_combo.get().replace("%", "")
        try: comp_val = int(comp_val_str)
        except: comp_val = 20
        
        thread = threading.Thread(target=self.run_generation, args=(ip, port, output_dir, raw_prompt_template, batch_count, do_webp, comp_val))
        thread.start()

    def run_generation(self, ip, port, output_dir, prompt_template, batch_count, do_webp, comp_val):
        try:
            client = ComfyClient(server_address=f"{ip}:{port}")
            self.log(f"{self.get_text('conn_start')} {ip}:{port}...")

            if not client.connect():
                 self.log(f"Failed to connect to {ip}:{port}")
                 return

            for i in range(batch_count):
                if self.stop_requested:
                    self.log("Batch stopped.")
                    break

                self.log(f"--- Batch {i+1}/{batch_count} ---")
                
                # --- Prompt Resolution Logic ---
                final_prompt = prompt_template
                
                # 1. Group Logic: Determine winners and losers
                group_keys = {} # "1" -> ["sets/casual", "sets/school"]
                for full_key, var in self.group_vars.items():
                    g_val = var.get()
                    if g_val and g_val != "":
                        if g_val not in group_keys: group_keys[g_val] = []
                        group_keys[g_val].append(full_key)
                
                losers = set()
                for gid, keys in group_keys.items():
                    if keys:
                        winner = random.choice(keys)
                        for k in keys:
                            if k != winner: losers.add(k)

                # 2. Token Logic: Find and replace
                # We look for __RANDOM__KEY__ or __SEQUENTIAL__KEY__
                tokens = re.findall(r"__(RANDOM|SEQUENTIAL)__([a-zA-Z0-9_/]+)__", final_prompt)
                
                # Pre-calculate path map for valid keys
                path_map = {}
                for cat_name, wildcards in self.wildcards.items():
                    for key_name, options in wildcards.items():
                        # Support both "cat/key" and just "key" if unique? 
                        # Our system uses "cat/key" as the unique identifier in self.selections
                        full_key = f"{cat_name}/{key_name}"
                        path_map[full_key] = [o for o in options if o]

                for mode, key in tokens:
                    full_token = f"__{mode}__{key}__"
                    
                    # If this key is a loser in a group, remove it
                    if key in losers:
                        final_prompt = final_prompt.replace(full_token, "")
                        continue

                    # If not found in wildcards, skip (might be manual text)
                    if key not in path_map:
                        continue
                        
                    cats = path_map[key]
                    repl_val = ""
                    
                    if not cats:
                        repl_val = ""
                    elif mode == "RANDOM":
                        repl_val = random.choice(cats)
                    elif mode == "SEQUENTIAL":
                        idx = i % len(cats)
                        repl_val = cats[idx]
                        
                    final_prompt = final_prompt.replace(full_token, repl_val, 1)

                # 3. Cleanup
                final_prompt = re.sub(r",\s*,", ",", final_prompt) # Remove double commas
                final_prompt = re.sub(r"\s+", " ", final_prompt)   # Remove double spaces
                final_prompt = final_prompt.strip().strip(",")
                
                self.log(f"Prompt: {final_prompt[:50]}...")
                
                # --- Workflow Execution ---
                seed_val = random.randint(1, 10**15)
                
                prompt_workflow = {
                    "39": {"inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default"}, "class_type": "CLIPLoader"},
                    "40": {"inputs": {"vae_name": "ae.safetensors"}, "class_type": "VAELoader"},
                    "46": {"inputs": {"unet_name": "z_image_turbo_bf16.safetensors", "weight_dtype": "default"}, "class_type": "UNETLoader"},
                    "41": {"inputs": {"width": 1024, "height": 1024, "batch_size": 1}, "class_type": "EmptySD3LatentImage"},
                    "45": {"inputs": {"text": final_prompt, "clip": ["39", 0]}, "class_type": "CLIPTextEncode"},
                    "42": {"inputs": {"conditioning": ["45", 0]}, "class_type": "ConditioningZeroOut"},
                    "47": {"inputs": {"model": ["46", 0], "shift": 3.0}, "class_type": "ModelSamplingAuraFlow"},
                    "44": {"inputs": {"model": ["47", 0], "positive": ["45", 0], "negative": ["42", 0], "latent_image": ["41", 0], 
                                      "seed": seed_val, 
                                      "steps": 9, "cfg": 1.0, "sampler_name": "res_multistep", "scheduler": "simple", "denoise": 1.0}, "class_type": "KSampler"},
                    "43": {"inputs": {"samples": ["44", 0], "vae": ["40", 0]}, "class_type": "VAEDecode"},
                    "9": {"inputs": {"filename_prefix": "z-image", "images": ["43", 0]}, "class_type": "SaveImage"}
                }
                
                result_files = client.generate(prompt_workflow, output_dir)
                for f in result_files:
                    self.log(f"Saved: {os.path.basename(f)}")
                    
                    final_image_path = f
                    
                    # WebP Conversion
                    if do_webp and f.lower().endswith(".png"):
                        try:
                            quality = max(1, 100 - comp_val)
                            webp_path = os.path.splitext(f)[0] + ".webp"
                            
                            with Image.open(f) as img:
                                img.save(webp_path, "WEBP", quality=quality)
                            
                            self.log(self.get_text("converted").format(quality))
                            
                            if os.path.exists(webp_path):
                                os.remove(f)
                                final_image_path = webp_path
                        except Exception as e:
                            self.log(f"WebP Error: {e}")

                    # Save Prompt
                    try:
                        txt_path = os.path.splitext(final_image_path)[0] + ".txt"
                        with open(txt_path, "w", encoding="utf-8") as prompt_file:
                            prompt_file.write(final_prompt)
                        self.log(f"Saved Prompt: {os.path.basename(txt_path)}")
                    except Exception as e:
                        self.log(f"Error saving prompt file: {str(e)}")
                
            self.log("All tasks completed or stopped.")

                
        except Exception as e:
            self.log(f"Error: {str(e)}")
        finally:
            self.generate_btn.configure(state="normal", text=self.get_text("ready"))

if __name__ == "__main__":
    app = App()
    app.mainloop()
