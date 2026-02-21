import os
import torch
from TTS.api import TTS
import gc

def generate_hindi_dub(segments, speaker_audio_path, output_audio_path):
    print("Initializing XTTS v2 for voice cloning...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
