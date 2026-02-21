import os
import torch
from TTS.api import TTS
import gc

def generate_hindi_dub(segments, speaker_audio_path, output_audio_path):
    print("Initializing XTTS v2 for voice cloning...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    combined_hindi_text = " ".join([seg['hi_text'] for seg in segments])
    print(f"Generating full TTS for text snippet...")
    
    tts.tts_to_file(
        text=combined_hindi_text,
        file_path=output_audio_path,
        speaker_wav=speaker_audio_path,
        language="hi"
    )

    # VRAM Cleanup
    del tts
    if device == "cuda":
        torch.cuda.empty_cache()
    gc.collect()
    return output_audio_path
