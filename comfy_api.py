import json
import uuid
import urllib.request
import urllib.parse
import websocket
import time
import requests
import os

class ComfyClient:
    def __init__(self, server_address="127.0.0.1:8188"):
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())
        self.ws = None

    def connect(self):
        ws_url = "ws://{}/ws?clientId={}".format(self.server_address, self.client_id)
        try:
            self.ws = websocket.WebSocket()
            self.ws.connect(ws_url)
            return True
        except Exception as e:
            print(f"WebSocket connection failed: {e}")
            return False

    def disconnect(self):
        if self.ws:
            self.ws.close()

    def queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        url = "http://{}/prompt".format(self.server_address)
        req = urllib.request.Request(url, data=data)
        try:
            return json.loads(urllib.request.urlopen(req).read())
        except Exception as e:
            print(f"Queue prompt failed: {e}")
            return None

    def get_image(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        url = "http://{}/view?{}".format(self.server_address, url_values)
        try:
            with urllib.request.urlopen(url) as response:
                return response.read()
        except Exception as e:
            print(f"Get image failed: {e}")
            return None

    def get_history(self, prompt_id):
        url = "http://{}/history/{}".format(self.server_address, prompt_id)
        try:
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read())
        except Exception as e:
            print(f"Get history failed: {e}")
            return None
            
    def wait_for_completion(self, prompt_id):
        while True:
            try:
                out = self.ws.recv()
                if isinstance(out, str):
                    message = json.loads(out)
                    if message['type'] == 'executing':
                        data = message['data']
                        if data['node'] is None and data['prompt_id'] == prompt_id:
                            return True # Execution finished
            except Exception as e:
                print(f"WebSocket execution error: {e}")
                return False
                
    def generate(self, workflow, output_dir):
        if not self.ws:
            if not self.connect():
                raise ConnectionError("Could not connect to ComfyUI server")

        prompt_id_resp = self.queue_prompt(workflow)
        if not prompt_id_resp:
             raise RuntimeError("Failed to queue prompt")
             
        prompt_id = prompt_id_resp['prompt_id']
        print(f"Prompt queued: {prompt_id}")
        
        if self.wait_for_completion(prompt_id):
            history = self.get_history(prompt_id)
            if not history:
                 raise RuntimeError("Failed to get history")
            
            history_data = history[prompt_id]
            outputs = history_data.get('outputs', {})
            
            saved_files = []
            for node_id, output_data in outputs.items():
                if 'images' in output_data:
                    for image in output_data['images']:
                        image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                        if image_data:
                            # Save to output dir
                            if not os.path.exists(output_dir):
                                os.makedirs(output_dir)
                                
                            # Create a unique filename to avoid overwrites or just use what api gave
                            # For safety let's prepend timestamp or something if needed, 
                            # but for now let's just use the filename from server
                            save_path = os.path.join(output_dir, image['filename'])
                            with open(save_path, 'wb') as f:
                                f.write(image_data)
                            saved_files.append(save_path)
            
            return saved_files
        else:
            raise RuntimeError("Generation failed or timed out")

