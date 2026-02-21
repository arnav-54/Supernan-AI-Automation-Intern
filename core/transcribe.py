from faster_whisper import WhisperModel
import os
import gc
import torch

def transcribe_audio(audio_path: str):
    print("Transcribing audio using faster-whisper...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    
    model = WhisperModel("base", device=device, compute_type=compute_type)
    segments, info = model.transcribe(audio_path, beam_size=5, language="en")
