import os
import torch
from TTS.api import TTS
import gc

def generate_hindi_dub(segments, speaker_audio_path, output_audio_path):
    print("Initializing XTTS v2 for voice cloning...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    # Logic for handling long audio: Batching by character count
    # Even if we only render 15s, this architecture scales for 500 hours.
    MAX_CHARS = 250
    batches = []
    current_batch = ""
    
    for seg in segments:
        text = seg['hi_text']
        if len(current_batch) + len(text) < MAX_CHARS:
            current_batch += " " + text
        else:
            batches.append(current_batch.strip())
            current_batch = text
    if current_batch:
        batches.append(current_batch.strip())

    temp_files = []
    print(f"Generating TTS in {len(batches)} batches...")
    
    for i, batch_text in enumerate(batches):
        temp_out = f"temp_batch_{i}.wav"
        tts.tts_to_file(
            text=batch_text,
            file_path=temp_out,
            speaker_wav=speaker_audio_path,
            language="hi"
        )
        temp_files.append(temp_out)

    if not temp_files:
        print("No audio segments generated. Skipping wave creation.")
        return None

    # Combine batches
    import wave
    with wave.open(output_audio_path, 'wb') as outfile:
        for i, infile_name in enumerate(temp_files):
            with wave.open(infile_name, 'rb') as infile:
                if i == 0:
                    outfile.setparams(infile.getparams())
                outfile.writeframes(infile.readframes(infile.getnframes()))
            os.remove(infile_name)

    # VRAM Cleanup
    del tts
    if device == "cuda":
        torch.cuda.empty_cache()
    gc.collect()
    
    return output_audio_path
