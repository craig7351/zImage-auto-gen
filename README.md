# Z-Image-Turbo (ComfyUI Client)

[English](#english) | [繁體中文](#traditional-chinese)

---

<a name="english"></a>
## English

A powerful and user-friendly client for ComfyUI, designed for efficient image generation with advanced wildcard management.

### Key Features

*   **ComfyUI Integration**: Connects seamlessly to your local ComfyUI server.
*   **Wildcard System**: Robust prompt generation using configurable wildcards.
    *   **Group Selection**: Organize wildcards into groups (1-10). Items in the same group with the "Random (?)" option checked are mutually exclusive (only one is selected per generation).
    *   **Dynamic Editing**: Edit the generated prompt code (e.g., `__RANDOM__outfit__`) directly in the preview window before generation.
    *   **Real-time Updates**: Changes to the prompt preview are applied immediately to the next image in the batch.
*   **Multilingual Support**: Fully supports **English** and **Traditional Chinese** interfaces, with **Traditional Chinese as the default**.
*   **Built-in Image Viewer**:
    *   Dedicated window for browsing generated images.
    *   Thumbnail list and scalable preview.
    *   **Prompt Copy**: One-click copy of the generation prompt and settings.
*   **Batch Generation**: Support for batch processing (1-512 images) with optional stop functionality.
*   **WebP Conversion**: Automatic conversion to WebP format to save disk space.
*   **Prompt Logging**: Automatically saves the full prompt used for each image to a text file.
*   **Portable**: Can be built into a standalone executable (EXE) via GitHub Actions.

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/craig7351/zImage-auto-gen.git
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    python main.py
    ```

---

<a name="traditional-chinese"></a>
## Traditional Chinese (繁體中文)

這是一個功能強大且易於使用的 ComfyUI 客戶端，專為高效的圖像生成與進階 Wildcard 管理而設計。

### 主要特點

*   **ComfyUI 整合**: 無縫連接到您的本地 ComfyUI 伺服器。
*   **Wildcard 系統**: 使用可配置的 Wildcard 進行強大的提示詞生成。
    *   **群組選擇 (Group Selection)**: 將 Wildcard 分組 (1-10)。在同一群組中勾選「隨機 (?)」的項目是互斥的 (每次生成只會選中其中一個)。
    *   **動態編輯**: 生成前可直接在預覽視窗中編輯提示詞代碼 (例如 `__RANDOM__outfit__`)。
    *   **即時更新**: 對預覽視窗的修改會立即套用到批次生成的下一張圖片。
*   **多語言支援**: 完整支援 **英文** 與 **繁體中文** 介面，並以 **繁體中文為預設**。
*   **內建圖片瀏覽器**:
    *   獨立視窗瀏覽生成的圖片。
    *   縮圖列表與可縮放預覽。
    *   **複製 Prompt**: 一鍵複製生成使用的提示詞與設定。
*   **批次生成**: 支援批次處理 (1-512 張圖片)，並具備停止功能。
*   **WebP 轉檔**: 支援自動轉檔為 WebP 格式以節省硬碟空間。
*   **Prompt 紀錄**: 自動將每張圖片使用的完整提示詞儲存為文字檔。
*   **可攜式**: 支援透過 GitHub Actions 自動打包為獨立執行檔 (EXE)。

### 安裝與執行

1.  複製儲存庫:
    ```bash
    git clone https://github.com/craig7351/zImage-auto-gen.git
    ```
2.  安裝依賴:
    ```bash
    pip install -r requirements.txt
    ```
3.  執行程式:
    ```bash
    python main.py
    ```
