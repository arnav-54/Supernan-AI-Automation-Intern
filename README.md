# Supernan AI Automation Intern Assessment

This repository contains a modular Python pipeline (`dub_video.py`) that generates a high-fidelity Hindi-dubbed version of a video.

## 🌟 Architecture & Resourcefulness

To achieve max fidelity with a budget of **₹0**, the pipeline strictly leverages state-of-the-art open-source models optimized for free GPU tiers (like Google Colab T4):
1. **Extraction**: `ffmpeg-python` (Zero cost, fast).
2. **Transcription**: `faster-whisper` (Orders of magnitude faster than standard Whisper).
3. **Translation**: Context-aware translating with `IndicTrans2` or `deep-translator`.
4. **Voice Cloning**: `Coqui XTTS v2` (Zero-shot voice cloning with speaker reference).
5. **Lip Sync**: `VideoReTalking` with GFPGAN (Prevents mouth blurring and retains face resolution—crucial for 40% Visual Fidelity requirement).

### Clever Handling of Constraints
To run heavy models (VideoReTalking + XTTS v2) on Colab without crashing out of memory:
- **Modular execution:** The pipeline flushes VRAM between steps (`torch.cuda.empty_cache()` and deleting model instances).
- **Chunking/Batching**: The translation and voice generation steps batch audio into smaller sentence chunks.

## 🚀 Setup Instructions

We highly recommend running this pipeline in **Google Colab** to easily deploy the GPU-heavy dependencies.

1. **Clone Repo**:
   ```bash
   git clone https://github.com/arnav-54/Supernan-AI-Automation-Intern.git
   cd Supernan-AI-Automation-Intern
   ```
2. **Install System Dependencies**:
   ```bash
   sudo apt-get update && sudo apt-get install -y ffmpeg
   ```
3. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Clone VideoReTalking**:
   ```bash
   git clone https://github.com/OpenTalker/video-retalking.git
   cd video-retalking && pip install -r requirements.txt && cd ..
   ```

## 🎥 Running the Pipeline

Extract a 15-second snippet and dub it:
```bash
python dub_video.py \
    --input_video "supernan_training.mp4" \
    --start_time 00:00:15 \
    --end_time 00:00:30 \
    --output_video "final_hindi_dub.mp4"
```
