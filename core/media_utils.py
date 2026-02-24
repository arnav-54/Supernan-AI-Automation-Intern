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
    print("Stage 2: Denoised Audio Extraction (afftdn + highpass)...")
    try:
        import subprocess
        # afftdn for adaptive noise reduction, highpass to remove low-end rumble
        cmd = [
            'ffmpeg', '-i', video_path,
            '-af', 'afftdn,highpass=f=200',
            '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
            '-y', audio_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return audio_path
    except Exception as e:
        print(f"Audio extraction error: {e}")
        return None

def extract_long_reference(input_path: str, ref_path: str, start_time: str = "00:00:00", duration: int = 30):
    """Extract a longer denoised audio clip from the full video for better voice cloning."""
    print(f"Stage 2: Extracting {duration}s clean reference audio...")
    try:
        import subprocess
        cmd = [
            'ffmpeg', '-i', input_path, '-ss', start_time, '-t', str(duration),
            '-af', 'afftdn,highpass=f=200',
            '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
            '-y', ref_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return ref_path
    except Exception as e:
        print(f"Long reference extraction error: {e}")
        return None

def get_duration(file_path: str):
    """Get duration of a media file using ffprobe."""
    probe = ffmpeg.probe(file_path)
    return float(probe['format']['duration'])

def match_audio_duration(audio_path: str, target_duration: float, output_path: str):
    """Stage 6: Natural Sync & Speed Locking (Max 1.15x) + Smart Padding."""
    current_duration = get_duration(audio_path)
    ratio = current_duration / target_duration
    
    # Speed Locking: Keep ratio between 0.85 and 1.15 for natural voice
    effective_ratio = max(0.85, min(1.15, ratio))
    print(f"Stage 6 Sync: {current_duration:.2f}s -> {target_duration:.2f}s (Ratio: {ratio:.2f}, Locked: {effective_ratio:.2f})")
    
    try:
        import subprocess
        # Clarity Booster: highpass + loudnorm
        clarity_filter = f"atempo={effective_ratio},highpass=f=200,loudnorm"
        
        cmd = [
            'ffmpeg', '-i', audio_path,
            '-filter:a', clarity_filter,
            '-y', output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Smart Padding: If locked duration is shorter than target, pad with silence
        final_duration = get_duration(output_path)
        if final_duration < target_duration - 0.1: # Threshold
            print(f"Applying Smart Padding: +{target_duration - final_duration:.2f}s silence...")
            pad_cmd = [
                'ffmpeg', '-i', output_path,
                '-af', f'apad=pad_dur={target_duration - final_duration}',
                '-y', output_path + "_padded.wav"
            ]
            subprocess.run(pad_cmd, check=True, capture_output=True)
            import shutil
            shutil.move(output_path + "_padded.wav", output_path)
            
        return output_path
    except Exception as e:
        print("FFmpeg duration match error:", e)
        import shutil
        shutil.copy(audio_path, output_path)
        return output_path
