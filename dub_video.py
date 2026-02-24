import argparse
# Global patch for PyTorch 2.6+ to allow loading Coqui TTS models
import torch
import torch.serialization
from functools import partial

# We trust Coqui TTS models, so we disable the strict 'weights_only' check
# that prevents loading of complex config classes.
torch.load = partial(torch.load, weights_only=False)

import os
from core.media_utils import extract_video_segment, extract_audio, extract_long_reference, get_duration, match_audio_duration
from core.transcribe import transcribe_audio
from core.translate import translate_to_hindi
from core.voice_clone import generate_hindi_dub
from core.lipsync import run_video_retalking

def main():
    parser = argparse.ArgumentParser(description="Supernan - AI Voice Dubbing & Lipsync Pipeline")
    parser.add_argument("--input_video", type=str, required=True, help="Path to input video")
    parser.add_argument("--start_time", type=str, default="00:00:15", help="Start time (HH:MM:SS)")
    parser.add_argument("--end_time", type=str, default="00:00:30", help="End time (HH:MM:SS)")
    parser.add_argument("--output_video", type=str, default="final_dubbed.mp4", help="Final output path")
    args = parser.parse_args()

    work_dir = "temp_processing"
    os.makedirs(work_dir, exist_ok=True)
    chunk_video = f"{work_dir}/chunk.mp4"
    ref_audio = f"{work_dir}/ref_audio.wav"
    long_ref_audio = f"{work_dir}/long_ref_audio.wav"
    raw_hindi_audio = f"{work_dir}/raw_dubbed_audio.wav"
    synced_hindi_audio = f"{work_dir}/synced_audio.wav"

    print("\n🚀 Starting Supernan Dubbing Pipeline (Modular High-Fidelity)...")

    print("\n=== Stage 1: Precision Clipping (FFmpeg) ===")
    extract_video_segment(args.input_video, chunk_video, args.start_time, args.end_time)
    target_duration = get_duration(chunk_video)
    print(f"Target Video Duration: {target_duration:.2f}s")
    
    print("\n=== Stage 2: Denoised Audio Extraction (FFmpeg) ===")
    extract_audio(chunk_video, ref_audio)
    extract_long_reference(args.input_video, long_ref_audio, start_time=args.start_time, duration=30)

    print("\n=== Stage 3: High-Accuracy Transcription (Whisper-Medium) ===")
    segments = transcribe_audio(ref_audio)
    segments[0]['end'] = target_duration 
    
    print("\n=== Stage 4: Natural Hindi Translation (IndicTrans2) ===")
    hindi_segments = translate_to_hindi(segments)

    print("\n=== Stage 5: Smart Voice Cloning (XTTS v2) ===")
    out_path = generate_hindi_dub(hindi_segments, long_ref_audio, raw_hindi_audio)
    
    if out_path and os.path.exists(raw_hindi_audio):
        print("\n=== Stage 6: Natural Sync & Speed Locking (1.15x) ===")
        match_audio_duration(raw_hindi_audio, target_duration, synced_hindi_audio)
        
        print("\n=== Stage 7: Robust Lip-Sync (VideoReTalking) ===")
        run_video_retalking(chunk_video, synced_hindi_audio, args.output_video)
        print(f"\n✨ SUCCESS! Your 15-second dubbed video is ready at: {args.output_video}")
    else:
        print("\n⚠️ Dubbing failed or no speech detected.")

if __name__ == "__main__":
    main()
