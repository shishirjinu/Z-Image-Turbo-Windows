import os, subprocess, shlex, uuid, time
import re
from pathlib import Path
import gradio as gr

ROOT = Path(__file__).parent
SD_EXE = str(ROOT / "sd_bin" / "sd.exe")
MODEL_PATH = str(ROOT / "models" / "zimage" / "z_image_turbo_Q4_0.gguf")
OUTDIR = str(ROOT / "outputs")
os.makedirs(OUTDIR, exist_ok=True)

DEFAULT_VAE_PATH = str(ROOT / "models" / "vae" / "ae.safetensors")
DEFAULT_LLM_PATH = str(ROOT / "models" / "llm" / "Qwen3-4B-Instruct-2507-Q4_K_M.gguf")

def gen_image(prompt, width, height, steps, seed, cfg_scale, vae_path, llm_path):
    uid = uuid.uuid4().hex[:8]
    out_file = os.path.join(OUTDIR, f"out_{uid}.png")
    if not os.path.isfile(SD_EXE):
        return None, f"sd.exe not found: {SD_EXE}"
    if not os.path.isfile(MODEL_PATH):
        return None, f"Model not found: {MODEL_PATH}"
    vae_path = (vae_path or "").strip() or DEFAULT_VAE_PATH
    llm_path = (llm_path or "").strip() or DEFAULT_LLM_PATH
    if not os.path.isfile(vae_path):
        return None, f"VAE not found: {vae_path}"
    if not os.path.isfile(llm_path):
        return None, f"LLM (text encoder) not found: {llm_path}"

    cmd = (
        f'"{SD_EXE}" '
        f'--diffusion-model "{MODEL_PATH}" '
        f'--vae "{vae_path}" '
        f'--llm "{llm_path}" '
        f'-p "{prompt}" '
        f'--cfg-scale {cfg_scale} '
        f'--steps {steps} '
        f'-H {height} -W {width} '
        f'-o "{out_file}" '
        f'--seed {seed}'
    )
    print("Running:", cmd)
    t0 = time.perf_counter()
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    t1 = time.perf_counter()
    elapsed = t1 - t0
    print(proc.stdout)
    reported = []
    if proc.stdout:
        m = re.search(r"generate_image completed in\s+([0-9.]+)s", proc.stdout)
        if m:
            reported.append(f"sd.exe generate_image: {m.group(1)}s")
        m = re.search(r"sampling completed, taking\s+([0-9.]+)s", proc.stdout)
        if m:
            reported.append(f"sd.exe sampling: {m.group(1)}s")
        m = re.search(r"loading tensors completed, taking\s+([0-9.]+)s", proc.stdout)
        if m:
            reported.append(f"sd.exe model load: {m.group(1)}s")

    timing_line = f"Wall-clock time: {elapsed:.2f}s"
    if reported:
        timing_line += "\n" + "\n".join(reported)

    combined_log = (timing_line + "\n\n" + (proc.stdout.strip() if proc.stdout else "")).strip()
    if proc.returncode != 0:
        return None, f"sd.exe exited with code {proc.returncode}\n\n{combined_log}".strip()
    imgs = sorted(Path(OUTDIR).glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
    if imgs:
        return str(imgs[0]), combined_log if combined_log else "Done"
    else:
        return None, (combined_log if combined_log else "No image was produced. Check sd.exe output above.")

with gr.Blocks() as demo:
    gr.Markdown("# Z-Image Turbo - Minimal UI")
    with gr.Row():
        prompt = gr.Textbox(label="Prompt", value="A large orange octopus on an ocean floor, cinematic, 8k")
    with gr.Row():
        width = gr.Dropdown([256, 384, 512, 640], value=512, label="Width")
        height = gr.Dropdown([256, 384, 512, 640], value=512, label="Height")
        steps = gr.Slider(1, 50, value=20, step=1, label="Steps")
        cfg_scale = gr.Slider(0.0, 10.0, value=1.0, step=0.1, label="CFG Scale")
        seed = gr.Number(value=0, label="Seed (0 = random)")
    with gr.Row():
        vae_path = gr.Textbox(label="VAE path", value=DEFAULT_VAE_PATH)
        llm_path = gr.Textbox(label="LLM (Qwen) path", value=DEFAULT_LLM_PATH)
    with gr.Row():
        btn = gr.Button("Generate")
    img = gr.Image(label="Result")
    status = gr.Textbox(label="Status", interactive=False, lines=12)
    def run_and_return(p, w, h, st, sd, cfg, vae, llm):
        yield None, "Generating... (keep this window open; first run can take time)"
        out, log = gen_image(p, int(w), int(h), int(st), int(sd), float(cfg), vae, llm)
        if out:
            yield out, log if log else "Done"
            return
        yield None, log if log else "Failed"
    btn.click(run_and_return, inputs=[prompt, width, height, steps, seed, cfg_scale, vae_path, llm_path], outputs=[img, status])

demo.launch(server_name="127.0.0.1", server_port=9000, share=False)
