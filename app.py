from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
import uuid
import os
from merge import merge_video_audio, get_duration

app = FastAPI()

# Create necessary directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("output")
TEST_FILES_DIR = Path("test_files")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the upload form."""
    html_path = Path("templates/index.html")
    if html_path.exists():
        return html_path.read_text()
    # Fallback if template doesn't exist yet
    return """
    <html>
        <head><title>Video Audio Merge</title></head>
        <body>
            <h1>Video Audio Merge</h1>
            <form action="/merge" method="post" enctype="multipart/form-data">
                <div>
                    <label>Video file: <input name="video" type="file" accept="video/*" required></label>
                </div>
                <div>
                    <label>Audio file: <input name="audio" type="file" accept="audio/*" required></label>
                </div>
                <button type="submit">Merge Files</button>
            </form>
        </body>
    </html>
    """

@app.post("/merge")
async def merge_files(
    video: UploadFile = File(...),
    audio: UploadFile = File(...)
):
    """Merge uploaded video and audio files."""
    
    # Generate unique filenames
    unique_id = str(uuid.uuid4())
    video_path = UPLOAD_DIR / f"{unique_id}_{video.filename}"
    audio_path = UPLOAD_DIR / f"{unique_id}_{audio.filename}"
    
    try:
        # Save uploaded files
        with video_path.open("wb") as f:
            shutil.copyfileobj(video.file, f)
        
        with audio_path.open("wb") as f:
            shutil.copyfileobj(audio.file, f)
        
        # Get durations for info
        video_duration = get_duration(video_path)
        audio_duration = get_duration(audio_path)
        
        # Merge video and audio
        output_filename = f"merged_{unique_id}.mp4"
        output_path = OUTPUT_DIR / output_filename
        
        merge_video_audio(video_path, audio_path, output_path)
        
        # Get output duration
        output_duration = get_duration(output_path)
        
        # Clean up uploaded files
        video_path.unlink()
        audio_path.unlink()
        
        # Return file info and download link
        return {
            "success": True,
            "message": "Files merged successfully",
            "video_duration": f"{video_duration:.2f} seconds" if video_duration else "Unknown",
            "audio_duration": f"{audio_duration:.2f} seconds" if audio_duration else "Unknown", 
            "output_duration": f"{output_duration:.2f} seconds" if output_duration else "Unknown",
            "download_url": f"/download/{output_filename}"
        }
        
    except Exception as e:
        # Clean up on error
        if video_path.exists():
            video_path.unlink()
        if audio_path.exists():
            audio_path.unlink()
        
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download the merged file."""
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=filename
    )

@app.get("/test-file/{filename}")
async def get_test_file(filename: str):
    """Serve test files."""
    file_path = TEST_FILES_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Determine media type based on extension
    ext = filename.lower().split('.')[-1]
    media_types = {
        'mp4': 'video/mp4',
        'mp3': 'audio/mpeg',
        'wav': 'audio/wav',
        'mov': 'video/quicktime',
        'avi': 'video/x-msvideo'
    }
    media_type = media_types.get(ext, 'application/octet-stream')
    
    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=filename
    )

@app.get("/test-files")
async def list_test_files():
    """List available test files."""
    files = {
        "video_files": [],
        "audio_files": []
    }
    
    if TEST_FILES_DIR.exists():
        for file in TEST_FILES_DIR.iterdir():
            if file.is_file():
                ext = file.suffix.lower()
                if ext in ['.mp4', '.mov', '.avi', '.mkv']:
                    files["video_files"].append(file.name)
                elif ext in ['.mp3', '.wav', '.m4a', '.aac']:
                    files["audio_files"].append(file.name)
    
    return files

@app.delete("/cleanup")
async def cleanup_old_files():
    """Clean up old output files (optional endpoint)."""
    import time
    current_time = time.time()
    deleted = 0
    
    for file_path in OUTPUT_DIR.glob("*.mp4"):
        # Delete files older than 1 hour
        if current_time - file_path.stat().st_mtime > 3600:
            file_path.unlink()
            deleted += 1
    
    return {"deleted_files": deleted}

if __name__ == "__main__":
    import uvicorn
    print("Starting server at http://localhost:8000")
    print("Upload your video and audio files to merge them!")
    uvicorn.run(app, host="0.0.0.0", port=8000)