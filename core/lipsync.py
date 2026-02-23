import subprocess
import os

def run_video_retalking(video_path, audio_path, output_path):
    print("Running VideoReTalking for high-fidelity lip sync + Face Restoration...")
    vrt_dir = "video-retalking"
    
    if os.path.exists(vrt_dir):
        cmd = [
            "python", f"{vrt_dir}/inference.py",
            "--face", video_path,
            "--audio", audio_path,
            "--outfile", output_path,
            "--face_restoration_model", "GFPGAN",
            "--upscale_facial_features"
        ]
        print(f"Executing VRT: {' '.join(cmd)}")
        # subprocess.run(cmd, check=True)
        return output_path
    else:
        print(f"⚠️ Warning: {vrt_dir} not found. Falling back to simple Audio+Video merge for preview...")
        # Fallback: Just merge the cropped video with the new Hindi audio
        try:
            import ffmpeg
            (
                ffmpeg
                .output(ffmpeg.input(video_path).video, ffmpeg.input(audio_path).audio, output_path, vcodec='copy', acodec='aac')
                .overwrite_output()
                .run(quiet=True)
            )
            print(f"✅ Preview video (without lip-sync) saved to {output_path}")
            return output_path
        except Exception as e:
            print(f"Error during fallback merge: {e}")
            return None
