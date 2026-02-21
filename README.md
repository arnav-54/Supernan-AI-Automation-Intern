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
