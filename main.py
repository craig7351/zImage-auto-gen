import customtkinter as ctk
import threading
import json
import os
import sys
from tkinter import filedialog
from comfy_api import ComfyClient

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ComfyUI Client - Z Image Turbo")
        self.geometry("600x650")

        # Load Workflow Template
        self.workflow_data = None
        self.load_workflow_template()

        self.create_widgets()
        
    def load_workflow_template(self):
        try:
            # Handle PyInstaller path
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
                
            json_path = os.path.join(application_path, "workflow_template.json")
            
            with open(json_path, "r", encoding="utf-8") as f:
                self.workflow_data = json.load(f)
        except Exception as e:
            self.log(f"Error loading workflow template: {e}")

    def create_widgets(self):
        # Configuration Frame
        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.pack(pady=10,padx=10, fill="x")

        # IP Address
        self.ip_label = ctk.CTkLabel(self.config_frame, text="Server IP:")
        self.ip_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ip_entry = ctk.CTkEntry(self.config_frame, width=120)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)

        # Port
        self.port_label = ctk.CTkLabel(self.config_frame, text="Port:")
        self.port_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.port_entry = ctk.CTkEntry(self.config_frame, width=80)
        self.port_entry.insert(0, "8188")
        self.port_entry.grid(row=0, column=3, padx=5, pady=5)

        # Output Directory
        self.output_label = ctk.CTkLabel(self.config_frame, text="Output:")
        self.output_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.output_entry = ctk.CTkEntry(self.config_frame, width=200)
        self.output_entry.insert(0, "./output")
        self.output_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.browse_btn = ctk.CTkButton(self.config_frame, text="Browse", width=60, command=self.browse_output)
        self.browse_btn.grid(row=1, column=3, padx=5, pady=5)
        
        # Prompt Area
        self.prompt_label = ctk.CTkLabel(self, text="Prompt:")
        self.prompt_label.pack(pady=(10,0), padx=10, anchor="w")
        self.prompt_text = ctk.CTkTextbox(self, height=150)
        self.prompt_text.pack(pady=5, padx=10, fill="x")
        
        # Set default prompt from template
        if self.workflow_data:
            # Node 45 is CLIPTextEncode
            default_prompt = ""
            for node in self.workflow_data.get("nodes", []):
                if node["id"] == 45: 
                    default_prompt = node["widgets_values"][0] if node.get("widgets_values") else ""
                    break
            self.prompt_text.insert("0.0", default_prompt)

        # Generate Button
        self.generate_btn = ctk.CTkButton(self, text="Generate Image", command=self.start_generation, height=40)
        self.generate_btn.pack(pady=15, padx=10, fill="x")

        # Log Area
        self.log_label = ctk.CTkLabel(self, text="Logs:")
        self.log_label.pack(pady=(10,0), padx=10, anchor="w")
        self.log_text = ctk.CTkTextbox(self, height=150, state="disabled")
        self.log_text.pack(pady=5, padx=10, fill="both", expand=True)

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

        self.generate_btn.configure(state="disabled")
        thread = threading.Thread(target=self.run_generation, args=(ip, port, output_dir, prompt))
        thread.start()

    def run_generation(self, ip, port, output_dir, prompt):
        try:
            client = ComfyClient(server_address=f"{ip}:{port}")
            self.log(f"Connecting to {ip}:{port}...")

            # Prepare Workflow
            # Use deep copy logic or just json load again if needed, but dictionary copy is fine for simple structure
            import copy
            workflow = copy.deepcopy(self.workflow_data)
            
            # Update Prompt (Node 45) -> In 'nodes' list for API formatted JSON?
            # Wait, the stored JSON in 'workflow_template.json' is the "User Format" (graph), 
            # OR is it the "API Format" (prompt)?
            # The file I read earlier `image_z_image_turbo_origin.json` has "nodes" and "links", so it is the Graph/UI format.
            # ComfyUI API expects the API format (key-value dict of node_id -> inputs).
            # I need to convert, OR usually, simply sending the "prompt" dictionary (node_id keys) works.
            # BUT, the file I have IS the UI format. I cannot send this directly to `/prompt`.
            # I must assume the user has a way to get the API format OR I need to parse the UI format to API format.
            # Parsing UI format to API format is complex (needs to resolve links).
            
            # Let's re-examine `image_z_image_turbo_origin.json` content from the earlier tool output.
            # It has "nodes", "links", "groups"... this is DEFINITELY the UI format.
            # ComfyUI API `/prompt` requires the API format (Node ID -> class_type, inputs).
            
            # CRITICAL: I cannot easily convert UI format to API format without a complex parser.
            # HOWEVER, often "Save (API Format)" in ComfyUI gives the right JSON.
            # If the user only provided the .json from "Save", it's the UI format.
            # I might need to ask the user for the API format version, OR try to construct it.
            
            # Wait, looking at the JSON again.
            # Node 45 (CLIPTextEncode) inputs: {"clip": [44, 0], "text": "..."} <-- this is how API format looks like?
            # NO, the JSON has "inputs": [{"name":..., "link": 44...}]. This is UI format.
            
            # FIX: I will implement a basic converter/parser since the graph is simple.
            # OR better, since I know the specific structure of THIS workflow, I can hardcode the API payload structure 
            # and just map the values. This is safer and robust for THIS specific tool.
            
            # Let's verify the node IDs and connections from the JSON analysis:
            # 39: CLIPLoader
            # 40: VAELoader
            # 46: UNETLoader
            # 41: EmptySD3LatentImage
            # 45: CLIPTextEncode (Positive Prompt) -> inputs: clip from 44? No wait. 
            # Let's look at links.
            # Link 44: Node 39 (CLIP) -> Node 45 (CLIPTextEncode)
            # Link 45: Node 43 (VAEDecode) -> Node 9 (SaveImage)
            
            # I will manually construct the prompt dictionary based on the analysis.
            prompt_workflow = {
                "39": {
                    "inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default"},
                    "class_type": "CLIPLoader"
                },
                "40": {
                    "inputs": {"vae_name": "ae.safetensors"},
                    "class_type": "VAELoader"
                },
                "46": {
                    "inputs": {"unet_name": "z_image_turbo_bf16.safetensors", "weight_dtype": "default"},
                    "class_type": "UNETLoader"
                },
                "41": {
                    "inputs": {"width": 1024, "height": 1024, "batch_size": 1},
                    "class_type": "EmptySD3LatentImage"
                },
                "45": {
                    "inputs": {
                        "text": prompt,
                        "clip": ["39", 0] 
                    },
                    "class_type": "CLIPTextEncode"
                },
                "42": { # ConditioningZeroOut
                     "inputs": {
                         "conditioning": ["45", 0] # Wait, link 36 goes from 45 to 42.
                     },
                     "class_type": "ConditioningZeroOut"
                },
                "47": { # ModelSamplingAuraFlow
                    "inputs": {
                        "model": ["46", 0],
                        "shift": 3.0
                    },
                    "class_type": "ModelSamplingAuraFlow"
                },
                "44": { # KSampler
                    "inputs": {
                        "model": ["47", 0],
                        "positive": ["45", 0],  # Link 41
                        "negative": ["42", 0],  # Link 42
                        "latent_image": ["41", 0], # Link 43
                        "seed": 0, # Randomize in code
                        "steps": 9,
                        "cfg": 1.0,
                        "sampler_name": "res_multistep",
                        "scheduler": "simple",
                        "denoise": 1.0
                    },
                    "class_type": "KSampler"
                },
                "43": { # VAEDecode
                    "inputs": {
                        "samples": ["44", 0],
                        "vae": ["40", 0]
                    },
                    "class_type": "VAEDecode"
                },
                "9": { # SaveImage
                    "inputs": {
                        "filename_prefix": "z-image",
                        "images": ["43", 0]
                    },
                    "class_type": "SaveImage"
                }
            }
            
            # Randomize Seed
            import random
            prompt_workflow["44"]["inputs"]["seed"] = random.randint(1, 10**15)
            
            self.log("Queuing prompt...")
            result_files = client.generate(prompt_workflow, output_dir)
            
            self.log("Generation Complete!")
            for f in result_files:
                self.log(f"Saved: {f}")
                
        except Exception as e:
            self.log(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.generate_btn.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()
