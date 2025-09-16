import subprocess
import os
import tempfile
from pathlib import Path

def merge_video_audio(video_path, audio_path, output_path=None):
    """
    Merge video and audio files, cutting to audio duration plus 0.5 seconds.
    
    Args:
        video_path: Path to input video file
        audio_path: Path to input audio file  
        output_path: Path for output file (optional, will generate if not provided)
    
    Returns:
        Path to the output file
    """
    video_path = Path(video_path)
    audio_path = Path(audio_path)
    
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    if output_path is None:
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"merged_{video_path.stem}.mp4"
    else:
        output_path = Path(output_path)
    
    # Get audio duration and add 0.5 seconds
    audio_duration = get_duration(audio_path)
    if audio_duration:
        target_duration = audio_duration + 0.5
    else:
        # Fallback to using -shortest if we can't get duration
        target_duration = None
    
    # FFmpeg command to merge video and audio
    if target_duration:
        # Use explicit duration with -t flag
        cmd = [
            "ffmpeg",
            "-i", str(video_path),  # Input video
            "-i", str(audio_path),  # Input audio
            "-c:v", "copy",         # Copy video codec (no re-encoding for speed)
            "-c:a", "aac",          # Encode audio to AAC
            "-map", "0:v:0",        # Use video from first input
            "-map", "1:a:0",        # Use audio from second input
            "-t", str(target_duration),  # Set output duration to audio + 0.5s
            "-y",                   # Overwrite output file if exists
            str(output_path)
        ]
    else:
        # Fallback to original behavior
        cmd = [
            "ffmpeg",
            "-i", str(video_path),  # Input video
            "-i", str(audio_path),  # Input audio
            "-c:v", "copy",         # Copy video codec (no re-encoding for speed)
            "-c:a", "aac",          # Encode audio to AAC
            "-map", "0:v:0",        # Use video from first input
            "-map", "1:a:0",        # Use audio from second input
            "-shortest",            # Stop when shortest stream (audio) ends
            "-y",                   # Overwrite output file if exists
            str(output_path)
        ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Successfully merged video and audio to: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error merging files: {e.stderr}")
        raise

def get_duration(file_path):
    """Get duration of video or audio file in seconds."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError):
        return None

if __name__ == "__main__":
    # Test the merge function
    import sys
    if len(sys.argv) < 3:
        print("Usage: python merge.py <video_file> <audio_file> [output_file]")
        sys.exit(1)
    
    video = sys.argv[1]
    audio = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else None
    
    try:
        # Show durations before merge
        video_duration = get_duration(video)
        audio_duration = get_duration(audio)
        if video_duration and audio_duration:
            print(f"Video duration: {video_duration:.2f} seconds")
            print(f"Audio duration: {audio_duration:.2f} seconds")
            print(f"Output will be: {audio_duration + 0.5:.2f} seconds (audio + 0.5s)")
        
        output_file = merge_video_audio(video, audio, output)
        
        # Show output duration
        output_duration = get_duration(output_file)
        if output_duration:
            print(f"Output duration: {output_duration:.2f} seconds")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)