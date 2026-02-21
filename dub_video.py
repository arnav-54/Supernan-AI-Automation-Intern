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
