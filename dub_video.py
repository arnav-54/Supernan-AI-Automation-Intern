import argparse
import os
from core.media_utils import extract_video_segment, extract_audio
from core.transcribe import transcribe_audio
from core.translate import translate_to_hindi
from core.voice_clone import generate_hindi_dub
from core.lipsync import run_video_retalking

def main():
    parser = argparse.ArgumentParser(description="Auto Voice Dubbing and Lipsync Pipeline")
    parser.add_argument("--input_video", type=str, required=True, help="Path to input video")
    parser.add_argument("--start_time", type=str, default="00:00:15", help="Start time (HH:MM:SS)")
    parser.add_argument("--end_time", type=str, default="00:00:30", help="End time (HH:MM:SS)")
    parser.add_argument("--output_video", type=str, default="final_dubbed.mp4", help="Final output path")
    args = parser.parse_args()

    work_dir = "temp_processing"
    os.makedirs(work_dir, exist_ok=True)
    chunk_video = f"{work_dir}/chunk.mp4"
    ref_audio = f"{work_dir}/ref_audio.wav"
    hindi_audio = f"{work_dir}/dubbed_audio.wav"

    print("=== Step 1: Crop Video ===")
    extract_video_segment(args.input_video, chunk_video, args.start_time, args.end_time)
    
    print("=== Step 2: Extract Speaker Audio ===")
    extract_audio(chunk_video, ref_audio)

    print("=== Step 3: Transcribe ===")
    segments = transcribe_audio(ref_audio)
    
    print("=== Step 4: Translate -> Hindi ===")
    hindi_segments = translate_to_hindi(segments)

    print("=== Step 5: Voice Cloning (XTTS v2) ===")
    generate_hindi_dub(hindi_segments, ref_audio, hindi_audio)
    
    print("=== Step 6: High Fidelity Lipsync (VideoReTalking) ===")
    run_video_retalking(chunk_video, hindi_audio, args.output_video)
    
    print(f"\n✅ Pipeline Complete! Output saved to: {args.output_video}")

if __name__ == "__main__":
    main()
