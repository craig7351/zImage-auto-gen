# ComfyUI 工作流分析: Z Image Turbo

## 檔案資訊
- **檔案名稱**: `image_z_image_turbo_origin.json`
- **用途**: 文字生成圖片 (Text-to-Image)
- **核心特點**: 使用 Z Image Turbo 模型與 Qwen 3.4B 文本編碼器，具備極高的生成速度（9步）。

## 1. 核心模型架構
此工作流採用了獨特的模型組合，推測基於 SD3 或類似的大型 Transformer 架構（因使用了 `EmptySD3LatentImage`）。

- **UNET 模型 (Diffusion Model)**
  - 檔案: `z_image_turbo_bf16.safetensors`
  - 類型: Turbo 模型，針對少步數生成進行了優化。
- **CLIP (Text Encoder)**
  - 檔案: `qwen_3_4b.safetensors`
  - 類型: Qwen (通義千問) 3.4B LLM，提供強大的語義理解能力。
- **VAE (Variational Autoencoder)**
  - 檔案: `ae.safetensors`
  - 用途: 將 Latent 圖像解碼為像素圖像。

## 2. 工作流邏輯 (Step-by-Step)
工作流節點被清晰地分為幾個群組：

### Step 1: 載入模型 (Load models)
使用以下節點載入核心組件：
- `CLIPLoader`: 載入 Qwen 3.4B。
- `VAELoader`: 載入 VAE。
- `UNETLoader`: 載入 Turbo UNET 模型。

### Step 2: 設定圖像尺寸 (Image size)
- 節點: `EmptySD3LatentImage`
- 解析度: **1024x1024**
- Batch Size: 1

### Step 3: 提示詞設定 (Prompt)
- **正面提示詞 (Positive)**: 使用 `CLIPTextEncode`。
  - 預設內容: *"Latina female with thick wavy hair, harbor boats and pastel houses behind. Breezy seaside light, warm tones, cinematic close-up."*
- **負面提示詞 (Negative)**: 使用 `ConditioningZeroOut`，表示不使用特定的負面提示詞，直接將條件歸零。

### Step 4: 採樣與生成
- **模型採樣調整**: `ModelSamplingAuraFlow` (Shift=3)，顯示此模型可能使用了 AuraFlow 架構。
- **採樣器 (KSampler)**:
  - **Steps**: 9 (極少步數)
  - **CFG**: 1.0
  - **Sampler**: `res_multistep`
  - **Scheduler**: `simple`

## 3. 依賴資源與模型路徑
若要執行此工作流，需確保以下模型位於 ComfyUI 的 `models` 目錄下的相應資料夾中：

```text
ComfyUI/
├── models/
│   ├── text_encoders/
│   │      └── qwen_3_4b.safetensors
│   ├── diffusion_models/
│   │      └── z_image_turbo_bf16.safetensors
│   └── vae/
│          └── ae.safetensors
```
