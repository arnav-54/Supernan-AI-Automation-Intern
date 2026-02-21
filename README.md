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

## 📈 The "Scale" Question (500 Hours Overnight)

**Question:** How would you modify this script to process 500 hours of video overnight with a budget?
**Answer:** Processing 500h (~30,000 mins) overnight requires heavy horizontal scaling:
1. **Infrastructure**: Transition from sequential execution to a distributed microservice architecture on AWS (EKS) or RunPod Serverless.
2. **Message Queue**: Use RabbitMQ or AWS SQS to distribute video chunks. We'd chunk videos into 2-5 minute segments.
3. **Pipeline Decoupling**:
   - `Worker Group A (CPU)`: Downloads and chunks video (FFmpeg).
   - `Worker Group B (GPU - L4)`: Transcribes using Faster-Whisper.
   - `Worker Group C (GPU/CPU)`: Translates in bulk.
   - `Worker Group D (GPU - A100)`: Generates cloned audio with XTTSv2.
   - `Worker Group E (GPU - A100)`: VideoReTalking is the bottleneck. This requires the largest fleet.
4. **Assembly**: A final CPU worker merges chunks back using temporal crossfading.

### Estimated Cost at Scale
- **In-house cluster (RunPod/Lambda)**: ~$0.05 to $0.15 per minute depending on GPU density. ~500 hrs (30k mins) = $1,500 - $4,500.
