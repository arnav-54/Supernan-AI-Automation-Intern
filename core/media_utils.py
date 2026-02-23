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
             .output(audio_path, acodec='pcm_s16le', ac=1, ar='16000')
             .overwrite_output()
             .run(quiet=True)
        )
        return audio_path
    except ffmpeg.Error as e:
        print("FFmpeg audio extraction error:", e.stderr)
        raise

def extract_long_reference(input_path: str, ref_path: str, start_time: str = "00:00:00", duration: int = 30):
    """Extract a longer audio clip (default 30s) from the full video for better voice cloning."""
    print(f"Extracting {duration}s reference audio from full video for voice cloning...")
    try:
        (
            ffmpeg
            .input(input_path, ss=start_time, t=duration)
            .output(ref_path, acodec='pcm_s16le', ac=1, ar='16000')
            .overwrite_output()
            .run(quiet=True)
        )
        return ref_path
    except ffmpeg.Error as e:
        print("FFmpeg long reference extraction error:", e.stderr)
        raise

def get_duration(file_path: str):
    """Get duration of a media file using ffprobe."""
    probe = ffmpeg.probe(file_path)
    return float(probe['format']['duration'])

def match_audio_duration(audio_path: str, target_duration: float, output_path: str):
    """Stretch or compress audio to match a target duration exactly."""
    current_duration = get_duration(audio_path)
    ratio = current_duration / target_duration
    
    print(f"Modifying audio speed: {current_duration:.2f}s -> {target_duration:.2f}s (Ratio: {ratio:.2f})")
    
    try:
        (
            ffmpeg
            .input(audio_path)
            .filter('atempo', ratio)
            .output(output_path)
            .overwrite_output()
            .run(quiet=True)
        )
        return output_path
    except ffmpeg.Error as e:
        print("FFmpeg duration match error:", e.stderr)
        # Fallback to copy if it fails
        import shutil
        shutil.copy(audio_path, output_path)
        return output_path
