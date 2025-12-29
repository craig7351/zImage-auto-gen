import customtkinter as ctk
import threading
import json
import os
import sys
import glob
from tkinter import filedialog, messagebox
from comfy_api import ComfyClient

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ComfyUI Client - Z Image Turbo (Wildcard Edition)")
        self.geometry("1100x800") # Increased size for new UI

        # Data storage for wildcards: { category: { filename: [options] } }
        # Flattened for nested directories as: { "outfit/theme": { "casual": [...] } } 
        # But for UI, we want Tabs for top-level folders.
        self.wildcards = {} 
        
        # UI State
        self.selections = {} # { "subject/count": "1girl", ... }

        self.load_workflow_template()
        self.load_wildcards()
        self.create_widgets()
        
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

    def load_wildcards(self):
        """Recursively scan 'wildcards' directory."""
        base_dir = "wildcards"
        if not os.path.exists(base_dir):
            if getattr(sys, 'frozen', False):
                 # Try to look in _MEIPASS if bundled? 
                 # Usually external files are not in MEIPASS unless added. 
                 # Assuming user keeps 'wildcards' folder next to EXE.
                 pass
            else:
                os.makedirs(base_dir)
                
        # Structure: self.wildcards[main_category][sub_key] = [options]
        # main_category = top level folder name (e.g., 'subject')
        # sub_key = filename (no ext) OR relative path for nested (e.g., 'theme/casual')
        
        for root, dirs, files in os.walk(base_dir):
            rel_path = os.path.relpath(root, base_dir)
            if rel_path == ".": continue
            
            # Top level folder is the category/tab name
            parts = rel_path.split(os.sep)
            top_category = parts[0]
            
            if top_category not in self.wildcards:
                self.wildcards[top_category] = {}
            
            # Sub-path within the category (e.g., 'theme' inside 'outfit')
            sub_path = "/".join(parts[1:]) 
            
            for file in files:
                if file.endswith(".txt"):
                    key = os.path.splitext(file)[0]
                    if sub_path:
                        key = f"{sub_path}/{key}"
                    
                    full_path = os.path.join(root, file)
                    with open(full_path, "r", encoding="utf-8") as f:
                        lines = [line.strip() for line in f.readlines() if line.strip()]
                        # Add empty option for deselection
                        lines.insert(0, "") 
                        self.wildcards[top_category][key] = lines
                        
    def create_widgets(self):
        # 1. Config Area (Top)
        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkLabel(self.config_frame, text="Server:").pack(side="left", padx=5)
        self.ip_entry = ctk.CTkEntry(self.config_frame, width=100)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.pack(side="left", padx=2)
        
        ctk.CTkLabel(self.config_frame, text=":").pack(side="left")
        self.port_entry = ctk.CTkEntry(self.config_frame, width=60)
        self.port_entry.insert(0, "8188")
        self.port_entry.pack(side="left", padx=2)
        
        ctk.CTkButton(self.config_frame, text="Browse Output", width=80, command=self.browse_output).pack(side="right", padx=5)
        self.output_entry = ctk.CTkEntry(self.config_frame, width=200)
        self.output_entry.insert(0, "./output")
        self.output_entry.pack(side="right", padx=5)
        ctk.CTkLabel(self.config_frame, text="Output:").pack(side="right", padx=5)

        # 2. Main Content Area (Split: Left=Wildcards, Right=Preview/Log)
        self.main_split = ctk.CTkFrame(self, fg_color="transparent")
        self.main_split.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Left: Wildcard Tabs
        self.left_panel = ctk.CTkFrame(self.main_split, width=700)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        if self.wildcards:
            self.tab_view = ctk.CTkTabview(self.left_panel)
            self.tab_view.pack(fill="both", expand=True)
            
            # Sort keys to keep order consistent if desired, or relying on dict order
            sorted_cats = sorted(self.wildcards.keys())
            
            # Specific order preference (optional)
            order_pref = ["subject", "face", "hair", "body", "outfit", "pose", "scene", "camera", "lighting", "style", "control", "negative"]
            # Reorder
            sorted_cats = sorted(sorted_cats, key=lambda x: order_pref.index(x) if x in order_pref else 99)
            
            for category in sorted_cats:
                self.tab_view.add(category)
                self.create_tab_content(category)
        else:
            ctk.CTkLabel(self.left_panel, text="No wildcards found in 'wildcards/' folder.").pack(pady=20)

        # Right: Prompt Preview & Logs
        self.right_panel = ctk.CTkFrame(self.main_split, width=350)
        self.right_panel.pack(side="right", fill="both", padx=(5, 0))
        
        # Prompt Preview
        ctk.CTkLabel(self.right_panel, text="Prompt Preview:").pack(pady=5, anchor="w")
        self.prompt_text = ctk.CTkTextbox(self.right_panel, height=200)
        self.prompt_text.pack(pady=5, fill="x")
        
        # Buttons
        self.btn_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.btn_frame.pack(pady=5, fill="x")
        
        self.refresh_btn = ctk.CTkButton(self.btn_frame, text="Sync from Selection", command=self.update_prompt_text)
        self.refresh_btn.pack(side="left", fill="x", expand=True, padx=2)
        
        self.generate_btn = ctk.CTkButton(self.btn_frame, text="GENERATE", fg_color="green", height=40, command=self.start_generation)
        self.generate_btn.pack(side="left", fill="x", expand=True, padx=2)

        # Logs
        ctk.CTkLabel(self.right_panel, text="Logs:").pack(pady=(10,0), anchor="w")
        self.log_text = ctk.CTkTextbox(self.right_panel)
        self.log_text.pack(pady=5, fill="both", expand=True)

    def create_tab_content(self, category):
        tab = self.tab_view.tab(category)
        
        # Use a scrollable frame inside tab
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", expand=True)
        
        # Get items
        items = self.wildcards[category]
        # Sort items: simple files first, then subfolders (if any)
        # items keys are like "color", "theme/casual"
        
        # Grouping logic would be nice for visuals
        # Just simple dynamic Grid for now
        
        row = 0
        for key, options in items.items():
            # key example: "theme/casual" or "count"
            label_text = key.replace("_", " ").title()
            
            # Frame for each row
            row_frame = ctk.CTkFrame(scroll, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row_frame, text=label_text, width=150, anchor="e").pack(side="left", padx=10)
            
            # Combobox
            # We need to bind this to a variable or callback
            # Use a callback with lambda to capture the key
            
            # Unique selection key: category/key
            full_key = f"{category}/{key}"
            
            combo = ctk.CTkComboBox(row_frame, values=options, width=300, 
                                    command=lambda val, k=full_key: self.on_selection_change(k, val))
            combo.set("") # Default empty
            combo.pack(side="left", fill="x", expand=True)
            
            # Initial state empty
            self.selections[full_key] = ""
            
            row += 1

    def on_selection_change(self, key, value):
        self.selections[key] = value
        self.update_prompt_text()

    def update_prompt_text(self):
        # Gather all non-empty selections
        # We can respect the order_pref to construct the prompt logically
        
        parts = []
        
        # Desired order of categories
        cat_order = ["subject", "face", "hair", "body", "outfit", "pose", "scene", "camera", "lighting", "style", "control", "negative"]
        
        # We need to iterate through categories in order, then files in that category
        # But self.selections is flat "cat/file".
        
        # Let's bucketize selections first
        bucket = {c: [] for c in cat_order}
        others = []
        
        for full_key, val in self.selections.items():
            if not val: continue
            
            cat = full_key.split("/")[0]
            if cat in bucket:
                bucket[cat].append(val)
            else:
                others.append(val)
                
        # Construct final string
        final_parts = []
        for cat in cat_order:
            if bucket[cat]:
                # Add a comment/separator logic if needed, but simple join is best for prompt
                final_parts.extend(bucket[cat])
                
        final_parts.extend(others)
        
        prompt_str = ", ".join(final_parts)
        
        # Update Textbox
        self.prompt_text.delete("0.0", "end")
        self.prompt_text.insert("0.0", prompt_str)

    def browse_output(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, directory)

    def log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def start_generation(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        output_dir = self.output_entry.get()
        prompt = self.prompt_text.get("0.0", "end").strip()

        if not ip or not port:
            self.log("Error: IP and Port are required.")
            return

        self.generate_btn.configure(state="disabled", text="Generating...")
        thread = threading.Thread(target=self.run_generation, args=(ip, port, output_dir, prompt))
        thread.start()

    def run_generation(self, ip, port, output_dir, prompt):
        try:
            client = ComfyClient(server_address=f"{ip}:{port}")
            self.log(f"Connecting to {ip}:{port}...")

            import copy
            import random
            
            # 1. Build Payload
            # Based on previous analysis of Z Image Turbo Workflow
            prompt_workflow = {
                "39": {"inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default"}, "class_type": "CLIPLoader"},
                "40": {"inputs": {"vae_name": "ae.safetensors"}, "class_type": "VAELoader"},
                "46": {"inputs": {"unet_name": "z_image_turbo_bf16.safetensors", "weight_dtype": "default"}, "class_type": "UNETLoader"},
                "41": {"inputs": {"width": 1024, "height": 1024, "batch_size": 1}, "class_type": "EmptySD3LatentImage"},
                "45": {"inputs": {"text": prompt, "clip": ["39", 0]}, "class_type": "CLIPTextEncode"},
                "42": {"inputs": {"conditioning": ["45", 0]}, "class_type": "ConditioningZeroOut"},
                "47": {"inputs": {"model": ["46", 0], "shift": 3.0}, "class_type": "ModelSamplingAuraFlow"},
                "44": {"inputs": {"model": ["47", 0], "positive": ["45", 0], "negative": ["42", 0], "latent_image": ["41", 0], "seed": random.randint(1, 10**15), "steps": 9, "cfg": 1.0, "sampler_name": "res_multistep", "scheduler": "simple", "denoise": 1.0}, "class_type": "KSampler"},
                "43": {"inputs": {"samples": ["44", 0], "vae": ["40", 0]}, "class_type": "VAEDecode"},
                "9": {"inputs": {"filename_prefix": "z-image", "images": ["43", 0]}, "class_type": "SaveImage"}
            }
            
            self.log("Queuing prompt...")
            result_files = client.generate(prompt_workflow, output_dir)
            
            self.log("Generation Complete!")
            for f in result_files:
                self.log(f"Saved: {f}")
                
        except Exception as e:
            self.log(f"Error: {str(e)}")
        finally:
            self.generate_btn.configure(state="normal", text="GENERATE")

if __name__ == "__main__":
    app = App()
    app.mainloop()
