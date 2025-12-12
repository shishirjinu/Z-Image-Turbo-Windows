# Z-Image Turbo — One-Click Windows Installer (4GB / 6–8GB / 10GB+ VRAM)

This package gives you a **clean, minimal, safe Windows setup** to run **Z-Image Turbo (GGUF)** locally using a lightweight **Gradio Web UI**, without requiring complicated tools like ComfyUI or Wan2GP.

It is built for **low-VRAM GPUs** (even 4GB cards) and uses **quantized GGUF models** for maximum compatibility.

---

# ⭐ Features

- ✔ One-Click installer (`start_zimage.bat`)
- ✔ Automatic Python venv creation  
- ✔ Automatic GGUF model download  
- ✔ Choose VRAM tier visually (4GB / 6–8GB / 10GB+)  
- ✔ Minimal web UI (Prompt → Image)  
- ✔ Safe: **no unknown EXE automatically downloaded**
- ✔ Uses the secure and trusted **stable-diffusion.cpp** backend  
- ✔ Runs locally at **http://127.0.0.1:9000**

---

# ⚠ Why do you need to provide `sd.exe` manually?

This installer **will never download executable (.exe) files from the internet automatically** for safety reasons.

`sd.exe` is the Windows binary for **stable-diffusion.cpp** — a trusted open-source GPU/CPU inference engine.  
You must manually download a version you trust and place it in:

`ZImage-Windows\sd_bin\sd.exe`

---

# ✅ Where to get `sd.exe` (Windows)

Go to the **stable-diffusion.cpp Releases** page and download a Windows ZIP that contains the `sd.exe` binary.

From the release assets list, pick one of these (names may include the commit/hash):

- **NVIDIA (recommended)**: `sd-...-bin-win-cuda12-x64.zip`
- **CPU only**: `sd-...-bin-win-x64.zip`

After downloading:

1. Extract the ZIP.
2. Find `sd.exe` inside the extracted folder.
3. Copy `sd.exe` into:

`ZImage-Windows\sd_bin\sd.exe`

Important:

- If the ZIP also contains `.dll` files, copy them into the **same** `sd_bin` folder next to `sd.exe`.
- Some stable-diffusion.cpp releases provide DLLs as a separate download. If your ZIP only has `sd.exe` but you still get a crash, download the matching DLL package for the same release and copy all DLLs next to `sd.exe`.
- If Windows shows errors like `VCRUNTIME140.dll missing`, install **Microsoft Visual C++ Redistributable 2015-2022 (x64)** and try again.

---

# Requirements (for beginners)

- **Windows 10/11 (64-bit)**
- **Python 3.10+** (the installer creates an isolated venv automatically)
- **Microsoft Visual C++ Redistributable 2015-2022 (x64)**
- **NVIDIA GPU users (optional)**
  - Install the latest NVIDIA driver
  - Use the `win-cuda...` build of `sd.exe` (recommended)

# Troubleshooting

If generation fails or `sd.exe` crashes:

- **Make sure you copied DLLs**
  - When you extract the stable-diffusion.cpp release ZIP, copy **`sd.exe` and any `.dll` files next to it** into `sd_bin\`
- **Try the CPU build to confirm your setup**
  - Download `sd-...-bin-win-x64.zip` (CPU-only) and test with that first
  - If CPU works but CUDA fails, it is usually a driver/CUDA compatibility issue
- **Common crash code**
  - `3221225781` (`0xC0000135`) usually means **missing DLL / runtime dependency**

---

# What the installer downloads automatically

The one-click setup will automatically download these **model files** (safe, non-executable):

- Z-Image Turbo GGUF (diffusion model)
- Qwen GGUF (LLM/text encoder)

Only `sd.exe` is **manual**.

Note: The VAE file (`ae.safetensors`) may require a Hugging Face login to download, so the installer will ask you to download it manually.

If any automatic download fails (network restrictions, Hugging Face blocked), you can download manually and place files here:

- `models\zimage\` (Z-Image Turbo GGUF)
  - Source: https://huggingface.co/leejet/Z-Image-Turbo-GGUF/tree/main
- `models\vae\ae.safetensors`
  - Source: https://huggingface.co/black-forest-labs/FLUX.1-schnell/tree/main
- `models\llm\Qwen3-4B-Instruct-2507-Q4_K_M.gguf`
  - Source: https://huggingface.co/unsloth/Qwen3-4B-Instruct-2507-GGUF/tree/main

During large downloads (GB-sized GGUF files), the installer shows a progress indicator in the terminal. Please keep the window open until it finishes.

