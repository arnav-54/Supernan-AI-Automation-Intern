import ffmpeg
import os

def extract_video_segment(input_path: str, output_path: str, start_time: str, end_time: str):
    print(f"Extracting video chunk from {start_time} to {end_time}...")
    try:
        (
            ffmpeg
            .input(input_path, ss=start_time, to=end_time)
            .output(output_path, c='copy')
            .overwrite_output()
            .run(quiet=True)
        )
        return output_path
    except ffmpeg.Error as e:
        print("FFmpeg encoding error:", e.stderr)
        raise

def extract_audio(video_path: str, audio_path: str):
    print("Extracting reference audio...")
    try:
        (
             ffmpeg
             .input(video_path)
             .output(audio_path, acodec='pcm_s16le', ac=1, ar='22050')
             .overwrite_output()
             .run(quiet=True)
        )
        return audio_path
    except ffmpeg.Error as e:
        print("FFmpeg audio extraction error:", e.stderr)
        raise
