# Video Audio Merge

A simple web application that merges video and audio files, cutting the video to match the audio duration (plus 0.5 seconds for smooth transitions).

## Features

- 🎬 Merge video files with new audio tracks
- ✂️ Automatically cuts video to audio length + 0.5s
- 🌐 Web interface for easy file uploads
- ⚡ Fast processing using FFmpeg
- 🐳 Docker-ready for deployment

## How It Works

When you upload a video and audio file:
1. The original video's audio is replaced with your new audio file
2. The video is cut to match the audio duration + 0.5 seconds
3. Perfect for when your video is longer than your audio track

## Prerequisites

- Python 3.8+
- FFmpeg installed on your system
- pip for Python package management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kevinfar25/video-audio-merge.git
cd video-audio-merge
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python app.py
```

2. Open your browser to `http://localhost:8000`

3. Upload your video and audio files

4. Click "Merge Files" and download the result

## API Endpoints

- `GET /` - Web interface
- `POST /merge` - Upload and merge video/audio files
- `GET /download/{filename}` - Download merged files
- `GET /test-files` - List available test files
- `GET /test-file/{filename}` - Get test file for testing

## File Structure

```
video-audio-merge/
├── app.py              # FastAPI application
├── merge.py            # Core FFmpeg merge logic
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Web interface
├── test_files/         # Test files directory
├── uploads/            # Temporary upload storage
└── output/             # Merged video outputs
```

## API Usage

The application provides a REST API endpoint for automation tools like n8n:

**Endpoint:** `POST /api/merge`

**Request:**
```json
{
  "video_url": "https://example.com/video.mp4",
  "audio_url": "https://example.com/audio.mp3"
}
```

See [API_DOCS.md](API_DOCS.md) for complete API documentation.

## Docker Deployment

### Local Docker Testing

```bash
docker-compose up --build
```

### Coolify Deployment

1. Push your code to GitHub
2. In Coolify:
   - Create new service
   - Select "Docker Compose" or "Dockerfile"
   - Connect your GitHub repository
   - Set environment variable: `BASE_URL=https://your-domain.com`
   - Deploy

The service will be available at your configured domain with the `/api/merge` endpoint for n8n integration.

## Technical Details

- Uses FFmpeg's `-t` flag to set precise output duration
- Copies video codec without re-encoding for fast processing
- Encodes audio to AAC for compatibility
- Handles various video formats (MP4, MOV, AVI, MKV)
- Supports multiple audio formats (MP3, WAV, M4A, AAC)

## License

MIT

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.