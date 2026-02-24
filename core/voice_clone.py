import os
import torch
from TTS.api import TTS
import gc

def generate_hindi_dub(segments, speaker_audio_path, output_audio_path):
    print("Stage 5: Smart Voice Cloning (XTTS v2) + Clarity Booster...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    
    combined_text = " ".join([seg['hi_text'] for seg in segments])
    
    # Smart Splitting: Text ko logical points par toda gaya (Stage 5)
    import re
    # Split by common Hindi conjunctions and punctuation
    sentences = re.split('([।|?|!|.]|और|कि|लेकिन|ताकि)', combined_text)
    
    batches = []
    chunk = ""
    for s in sentences:
        if len(chunk) + len(s) < 180: # Slightly smaller for better flow
            chunk += s
        else:
            if chunk: batches.append(chunk.strip())
            chunk = s
    if chunk: batches.append(chunk.strip())
    
    temp_files = []
    print(f"Processing {len(batches)} smart batches for Stage 5...")
    
    for i, text in enumerate(batches):
        if not text or len(text) < 2: continue
        t_path = f"temp_processing/batch_{i}.wav"
        tts.tts_to_file(text=text, file_path=t_path, speaker_wav=speaker_audio_path, language="hi")
        temp_files.append(t_path)
    
    # Merge batches
    raw_merged = output_audio_path + ".raw.wav"
    if temp_files:
        import wave
        with wave.open(raw_merged, 'wb') as outfile:
            for i, f in enumerate(temp_files):
                with wave.open(f, 'rb') as infile:
                    if i == 0: outfile.setparams(infile.getparams())
                    outfile.writeframes(infile.readframes(infile.getnframes()))
                os.remove(f)
    
    # Stage 5 Clarity Booster: Equalizer, Compressor, Loudnorm
    print("Applying Clarity Booster (EQ + Compressor + Loudnorm)...")
    try:
        import subprocess
        # eq: soft boost to high end, compand: compression, loudnorm: normalization
        cmd = [
            'ffmpeg', '-i', raw_merged,
            '-af', 'equalizer=f=3000:width_type=o:width=2:g=3,compand=0.3|0.3:1|1:-90/-60|-60/-40|-40/-30|-20/-20:6:0:-90:0.2,loudnorm',
            '-y', output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        os.remove(raw_merged)
    except Exception as e:
        print(f"Clarity Booster failed, using raw audio: {e}")
        import shutil
        shutil.move(raw_merged, output_path)
    
    print(f"✅ Stage 5 Premium Dubbing complete: {output_audio_path}")

    # VRAM Cleanup
    del tts
    if device == "cuda":
        torch.cuda.empty_cache()
    gc.collect()
    
    return output_audio_path
