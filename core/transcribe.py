from faster_whisper import WhisperModel
import os
import gc
import torch

def transcribe_audio(audio_path: str):
    print("Transcribing audio using faster-whisper (small)...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # Using float16 for speed if on GPU, otherwise int8
    compute_type = "float16" if device == "cuda" else "int8"
    
    # Stage 3: Whisper-medium for best-in-class open-source accuracy
    model = WhisperModel("medium", device=device, compute_type=compute_type)
    
    # Force Kannada (kn) to prevent detection errors
    segments, info = model.transcribe(audio_path, beam_size=5, language="kn")
    
    full_text = ""
    for segment in segments:
        full_text += " " + segment.text
    
    print(f"✅ Final Transcription: {full_text.strip()}")

    # We return a single merged segment to ensure the XTTS step 
    # produces a continuous 15s+ voice track for perfect sync.
    results = [{
        "start": 0.0,
        "end": 15.0, # Placeholder, matched in main
        "text": full_text.strip()
    }]
    
    # Clean up
    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    gc.collect()
    
    return results
