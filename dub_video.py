import argparse
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

    print("\n🚀 Starting Supernan Dubbing Pipeline (Indic-Conformer Optimized)...")

    print("\n=== Step 1: Clip Extraction (15s minimum) ===")
    extract_video_segment(args.input_video, chunk_video, args.start_time, args.end_time)
    target_duration = get_duration(chunk_video)
    print(f"Target Video Duration: {target_duration:.2f}s")
    
    print("\n=== Step 2: Speaker Reference Extraction ===")
    extract_audio(chunk_video, ref_audio)
    extract_long_reference(args.input_video, long_ref_audio, start_time=args.start_time, duration=30)

    print("\n=== Step 3: High-Fidelity ASR (Indic-Conformer) ===")
    # This model is state-of-the-art for Kannada and handles the full 15s segment.
    segments = transcribe_audio(ref_audio)
    # Ensure the segment covers the whole duration for perfect sync
    segments[0]['end'] = target_duration 
    
    print("\n=== Step 4: Machine Translation (Context-Aware) ===")
    hindi_segments = translate_to_hindi(segments)

    print("\n=== Step 5: Voice Cloning (XTTS v2) ===")
    out_path = generate_hindi_dub(hindi_segments, long_ref_audio, raw_hindi_audio)
    
    if out_path and os.path.exists(raw_hindi_audio):
        print("\n=== Step 6: Chained Duration Matching (Perfect 15s Sync) ===")
        # This matches the generated audio to the EXACT target duration (15s+)
        match_audio_duration(raw_hindi_audio, target_duration, synced_hindi_audio)
        
        print("\n=== Step 7: Lip-Sync & Face Enhancement (VideoReTalking + GFPGAN) ===")
        run_video_retalking(chunk_video, synced_hindi_audio, args.output_video)
        print(f"\n✨ SUCCESS! Your 15-second dubbed video is ready at: {args.output_video}")
    else:
        print("\n⚠️ Dubbing failed or no speech detected.")

if __name__ == "__main__":
    main()
