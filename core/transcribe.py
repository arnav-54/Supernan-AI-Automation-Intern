from faster_whisper import WhisperModel
import os
import gc
import torch

def transcribe_audio(audio_path: str):
    print("Transcribing audio using faster-whisper...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    
    model = WhisperModel("base", device=device, compute_type=compute_type)
    segments, info = model.transcribe(audio_path, beam_size=5) # Auto-detect language

    results = []
    for segment in segments:
        results.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        })
    
    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    gc.collect()
    
    return results
