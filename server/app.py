import os
import tempfile
import subprocess
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class ScreengrabRequest(BaseModel):
    url: str


@app.post("/screengrab")
async def screengrab(request: ScreengrabRequest):
    """
    Capture a screenshot from a YouTube live stream.

    Args:
        request: JSON with 'url' field containing the YouTube URL

    Returns:
        JPEG image of the captured frame or 500 error
    """
    try:
        url = request.url
        logger.info(f"Processing screengrab request for URL: {url}")

        # Create a temporary directory for the download
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "screenshot.jpg")

            # Use yt-dlp to get a screenshot
            # --write-thumbnail writes the thumbnail
            # --skip-download skips downloading the video
            # --convert-thumbnails jpg converts to JPEG format
            cmd = [
                "yt-dlp",
                "--write-thumbnail",
                "--skip-download",
                "--convert-thumbnails", "jpg",
                "-o", output_path,
                url
            ]

            logger.info(f"Executing command: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                error_msg = f"yt-dlp failed: {result.stderr}"
                logger.error(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)

            # Find the generated thumbnail file
            # yt-dlp creates files like screenshot.jpg or screenshot.jpg.jpg
            thumbnail_file = None
            for file in os.listdir(temp_dir):
                if file.endswith(".jpg"):
                    thumbnail_file = os.path.join(temp_dir, file)
                    break

            if not thumbnail_file or not os.path.exists(thumbnail_file):
                error_msg = "Screenshot file not generated"
                logger.error(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)

            # Read the JPEG file
            with open(thumbnail_file, "rb") as f:
                image_data = f.read()

            logger.info(f"Successfully captured screenshot ({len(image_data)} bytes)")
            return Response(content=image_data, media_type="image/jpeg")

    except subprocess.TimeoutExpired:
        error_msg = "Request timeout while processing video"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
    except Exception as e:
        error_msg = f"Error processing request: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}
