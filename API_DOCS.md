# API Documentation

## Base URL
```
http://your-domain.com
```

## Endpoints

### 1. Health Check
Check if the service is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "video-audio-merge"
}
```

### 2. Merge Video and Audio from URLs (For n8n/Automation)

**Endpoint:** `POST /api/merge`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "video_url": "https://example.com/video.mp4",
  "audio_url": "https://example.com/audio.mp3",
  "output_format": "mp4"  // optional, defaults to "mp4"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Files merged successfully",
  "video_duration": "30.00 seconds",
  "audio_duration": "20.00 seconds",
  "output_duration": "20.50 seconds",
  "download_url": "http://your-domain.com/download/merged_uuid.mp4"
}
```

**Error Response:**
```json
{
  "detail": "Error message here"
}
```

### 3. Download Merged File

**Endpoint:** `GET /download/{filename}`

Downloads the merged video file.

## n8n Integration Example

### HTTP Request Node Configuration:

1. **Method:** POST
2. **URL:** `https://your-coolify-domain.com/api/merge`
3. **Authentication:** None (or add if you implement auth)
4. **Headers:**
   - Content-Type: `application/json`
5. **Body (JSON):**
```json
{
  "video_url": "{{ $json.video_url }}",
  "audio_url": "{{ $json.audio_url }}"
}
```

### Workflow Example:

1. **Trigger:** Webhook or any trigger
2. **HTTP Request:** Call the merge API
3. **Response:** Get the download URL
4. **Optional:** Download the file or pass URL to next step

### Sample n8n JSON Code:
```json
{
  "nodes": [
    {
      "parameters": {
        "method": "POST",
        "url": "https://your-domain.com/api/merge",
        "options": {},
        "bodyParametersUi": {
          "parameter": [
            {
              "name": "video_url",
              "value": "https://example.com/video.mp4"
            },
            {
              "name": "audio_url",
              "value": "https://example.com/audio.mp3"
            }
          ]
        }
      },
      "name": "Merge Video Audio",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 2,
      "position": [420, 260]
    }
  ]
}
```

## Coolify Deployment

### Environment Variables:

Set these in Coolify's environment variables:

```env
BASE_URL=https://your-coolify-domain.com
```

### Deployment Steps:

1. In Coolify, create a new service
2. Choose "Docker Compose" or "Dockerfile"
3. Connect your GitHub repository
4. Set the environment variables
5. Deploy

### Health Check:

Coolify will use the `/health` endpoint to monitor the service.

## Notes:

- Files are processed with FFmpeg
- Video is cut to audio duration + 0.5 seconds
- Temporary files are automatically cleaned up
- Maximum file size depends on server configuration
- Output files are stored temporarily and should be downloaded promptly