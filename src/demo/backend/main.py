"""
FastAPI Backend for Brand Exposure Analyzer
============================================

This module provides a REST API for analyzing videos to detect brand exposure using YOLO object detection.
The API supports both local file uploads and YouTube URL analysis with real-time streaming progress updates.

Architecture:
    - Each analysis endpoint returns a StreamingResponse with NDJSON format (newline-delimited JSON)
    - During analysis, progress objects are streamed for real-time UI updates with type="progress"
    - After analysis completes, a final result object is sent with type="complete"
    - If errors occur, error objects are sent with type="error"
    - The frontend (Streamlit app) parses these NDJSON objects line-by-line for live progress display

API Endpoints:
    GET /model-info/: Returns detectable brands and model metadata
    POST /analyze/: Upload and analyze a video file with streaming progress
    POST /analyze-stream/: Analyze YouTube URL with streaming progress
    GET /results/{video_id}: Retrieve stored analysis results by video UUID
    DELETE /results/{video_id}: Delete analysis results from database
    POST /save-analysis/: Verify analysis is saved to database

Dependencies:
    - FastAPI: REST framework and streaming support
    - DatabaseManager: PostgreSQL persistence layer
    - BrandInspector: YOLO model for brand detection
    - Logger: Structured logging with colorlog
"""

import sys
from pathlib import Path
import tempfile
import uuid
import json

# Add parent directory to Python path to enable imports from sibling packages
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.log_setup import log_setup
from common.logger import Logger

log_setup()

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from backend.database_manager import DatabaseManager
from backend.model_worker import BrandInspector

app = FastAPI()
db = DatabaseManager()
yolo = BrandInspector()
log = Logger().log

@app.get("/model-info/")
async def get_model_info():
    """
    Retrieve information about the brand detection model.
    
    Returns:
        dict: Model metadata including detectable brands, confidence thresholds, and model version.
    """
    return yolo.get_model_info()

@app.post("/analyze/")
async def analyze_video(file: UploadFile = File(...)):
    """
    Analyze an uploaded video file for brand exposure using YOLO detection.
    
    This endpoint accepts a video file upload, processes it frame-by-frame, and returns
    real-time streaming updates as a StreamingResponse with NDJSON format.
    
    Before starting analysis, it checks if a video with the same name already exists
    in the database. If found, it returns a duplicate detection response.
    
    Streaming Progress Format:
        - Duplicate object (type="duplicate"): Sent if video already exists with existing video_id
        - Progress objects (type="progress"): Sent during analysis with current frame metrics
        - Complete object (type="complete"): Sent at end with final results and video_id for storage
        - Error object (type="error"): Sent if analysis fails
    
    Args:
        file (UploadFile): Video file to analyze (supported formats: mp4, avi, mov, etc.)
    
    Returns:
        StreamingResponse: NDJSON-formatted stream with analysis progress and final results.
            Each line contains a JSON object with:
            - type: "duplicate", "progress", "complete", or "error"
            - For duplicate: existing_video_id (UUID) of the already stored analysis
            - For progress: timestamp, brands detected in frame, progress percentage, detected_seconds
            - For complete: video_id (UUID), title, exposure metrics, and brand breakdown
    
    Raises:
        HTTPException: 500 error if file processing or analysis fails
    """
    try:
        # Check if video already exists in database by filename
        existing_analysis = db.read_analysis(file.filename)
        if existing_analysis:
            # Video already exists, return duplicate response
            duplicate_response = {
                "type": "duplicate",
                "existing_video_id": existing_analysis["video_id"],
                "title": existing_analysis["title"],
                "message": f"Video '{file.filename}' already exists in database with ID: {existing_analysis['video_id']}"
            }
            return StreamingResponse(
                [json.dumps(duplicate_response) + "\n"],
                media_type="application/x-ndjson"
            )
        
        # Save uploaded file to temporary location for processing
        video_id = str(uuid.uuid4())
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Define generator function for streaming analysis progress
        def generate_analysis():
            """
            Generator that yields NDJSON-formatted progress updates during video analysis.
            
            Yields:
                str: JSON line containing progress or final result objects
            """
            try:
                frames_data = []
                total_duration = 0
                total_detected = 0
                final_brands = {}
                
                # Stream progress for each frame as it's analyzed (BrandInspector yields frame data)
                for frame_info in yolo.analyze_local_video_stream(tmp_path):
                    frames_data.append(frame_info)
                    total_duration = frame_info.get("frame_index", 0) / 30  # Rough estimate from frame count
                    total_detected = frame_info.get("detected_seconds", 0)
                    final_brands = frame_info.get("brand_counts", {})
                    
                    # Yield progress update as NDJSON object (type="progress")
                    progress_data = {
                        "type": "progress",
                        "timestamp": frame_info.get("timestamp", 0),
                        "brands": frame_info.get("brands", {}),
                        "progress": frame_info.get("progress", 0),
                        "detected_seconds": total_detected
                    }
                    yield json.dumps(progress_data) + "\n"
                
                # Get final metrics from last frame
                if frames_data:
                    last_frame = frames_data[-1]
                    total_detected = last_frame.get("detected_seconds", 0)
                    final_brands = last_frame.get("brand_counts", {})
                
                # Calculate brand exposure as percentage of total video duration
                exposure_percent = (total_detected / max(total_duration, 1) * 100) if total_duration > 0 else 0
                
                # Save analysis to database for later retrieval
                analysis_record = {
                    "video_id": video_id,
                    "title": file.filename,
                    "detected_seconds": total_detected,
                    "total_duration": total_duration,
                    "brand_exposure_percent": exposure_percent,
                    "brands": final_brands,
                    "frames_data": frames_data
                }
                
                db.create_analysis(analysis_record)
                
                # Yield final result as NDJSON object (type="complete") with video_id for storage
                final_result = {
                    "status": "success",
                    "video_id": video_id,
                    "title": file.filename,
                    "exposure_seconds": total_detected,
                    "total_seconds": total_duration,
                    "exposure_percent": exposure_percent,
                    "brands": final_brands
                }
                
                yield json.dumps({"type": "complete", "result": final_result}) + "\n"
                
            except Exception as e:
                log.error(f"Analysis error: {e}")
                # Yield error as NDJSON object (type="error") so frontend can display error message
                yield json.dumps({"type": "error", "detail": str(e)}) + "\n"
            finally:
                # Clean up temporary video file after analysis completes
                Path(tmp_path).unlink(missing_ok=True)
        
        return StreamingResponse(generate_analysis(), media_type="application/x-ndjson")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-stream/")
async def analyze_stream(url: str):
    """
    Analyze a video from a YouTube URL for brand exposure using YOLO detection.
    
    This endpoint downloads and processes a YouTube video frame-by-frame, returning
    real-time streaming updates as a StreamingResponse with NDJSON format.
    
    Before starting analysis, it checks if a video with the same URL already exists
    in the database. If found, it returns a duplicate detection response.
    
    Streaming Progress Format:
        - Duplicate object (type="duplicate"): Sent if video already exists with existing video_id
        - Progress objects (type="progress"): Sent during analysis with current frame metrics
        - Complete object (type="complete"): Sent at end with final results and video_id
        - Error object (type="error"): Sent if download or analysis fails
    
    Args:
        url (str): YouTube video URL to analyze
    
    Returns:
        StreamingResponse: NDJSON-formatted stream with analysis progress and final results.
            Each line contains a JSON object with:
            - type: "duplicate", "progress", "complete", or "error"
            - For duplicate: existing_video_id (UUID) of the already stored analysis
            - For progress: timestamp, brands detected, progress percentage, detected_seconds
            - For complete: video_id (UUID), title, exposure metrics, and brand breakdown
    
    Raises:
        HTTPException: 500 error if URL is invalid or analysis fails
    """
    try:
        # Check if video already exists in database by URL (we'll use URL as a unique identifier)
        # For YouTube URLs, we'll check if any video with the same title exists
        # This is a simple approach - in a production system you might want to store URL hashes
        
        # First, try to get video title from URL to check for duplicates
        try:
            import yt_dlp
            ydl_opts = {
                'format': 'best[height<=480]',
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                meta = ydl.extract_info(url, download=False)
                video_title = meta.get('title', '')
        except:
            video_title = ""
        
        # Check if video with same title exists
        if video_title:
            existing_analysis = db.read_analysis(video_title)
            if existing_analysis:
                # Video already exists, return duplicate response
                duplicate_response = {
                    "type": "duplicate",
                    "existing_video_id": existing_analysis["video_id"],
                    "title": existing_analysis["title"],
                    "message": f"Video '{video_title}' already exists in database with ID: {existing_analysis['video_id']}"
                }
                return StreamingResponse(
                    [json.dumps(duplicate_response) + "\n"],
                    media_type="application/x-ndjson"
                )
        
        def generate_analysis():
            """
            Generator that yields NDJSON-formatted progress updates during YouTube video analysis.
            
            Yields:
                str: JSON line containing progress or final result objects
            """
            try:
                frames_data = []
                total_duration = 0
                total_detected = 0
                final_brands = {}
                title = ""
                
                # Stream progress for each frame as it's analyzed (BrandInspector handles YouTube download)
                for frame_info in yolo.analyze_stream(url):
                    frames_data.append(frame_info)
                    total_duration = frame_info.get("duration", 0)
                    total_detected = frame_info.get("detected_seconds", 0)
                    final_brands = frame_info.get("brand_counts", {})
                    title = frame_info.get("title", "")
                    
                    # Yield progress update as NDJSON object (type="progress")
                    progress_data = {
                        "type": "progress",
                        "timestamp": frame_info.get("timestamp", 0),
                        "brands": frame_info.get("brands", {}),
                        "progress": frame_info.get("progress", 0),
                        "detected_seconds": total_detected
                    }
                    yield json.dumps(progress_data) + "\n"
                
                # Calculate brand exposure as percentage of total video duration
                exposure_percent = (total_detected / max(total_duration, 1) * 100) if total_duration > 0 else 0
                
                # Create analysis record with unique video_id for database storage
                video_id = str(uuid.uuid4())
                analysis_record = {
                    "video_id": video_id,
                    "title": title,
                    "detected_seconds": total_detected,
                    "total_duration": total_duration,
                    "brand_exposure_percent": exposure_percent,
                    "brands": final_brands,
                    "frames_data": frames_data
                }
                
                # Store analysis results in database for later retrieval
                db.create_analysis(analysis_record)
                
                # Yield final result as NDJSON object (type="complete") with video_id for storage
                final_result = {
                    "status": "success",
                    "video_id": video_id,
                    "title": title,
                    "exposure_seconds": total_detected,
                    "total_seconds": total_duration,
                    "exposure_percent": exposure_percent,
                    "brands": final_brands
                }
                
                yield json.dumps({"type": "complete", "result": final_result}) + "\n"
                
            except Exception as e:
                log.error(f"Stream analysis error: {e}")
                # Yield error as NDJSON object (type="error") so frontend can display error message
                yield json.dumps({"type": "error", "detail": str(e)}) + "\n"
        
        return StreamingResponse(generate_analysis(), media_type="application/x-ndjson")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results/")
async def list_results():
    """
    List all stored analysis results.
    
    Returns:
        list: List of all analysis records with video_id and title
    """
    try:
        # Get all videos from database
        videos = db.get_all_videos()
        return videos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results/{video_id}")
async def get_results(video_id: str):
    """
    Retrieve stored analysis results for a video by UUID.
    
    Args:
        video_id (str): Unique identifier (UUID) of the analyzed video
    
    Returns:
        dict: Analysis results including detections, brand breakdown, and metrics
    
    Raises:
        HTTPException: 404 if video_id is not found in database
    """
    results = db.read_analysis(video_id)
    if not results:
        raise HTTPException(status_code=404, detail="Video not found")
    return results

@app.delete("/results/{video_id}")
async def delete_video(video_id: str):
    """
    Delete analysis results for a video from the database.
    
    Args:
        video_id (str): Unique identifier (UUID) of the analyzed video to delete
    
    Returns:
        dict: Confirmation status
    """
    db.delete_analysis(video_id)
    return {"status": "deleted"}

@app.post("/reanalyze/")
async def reanalyze_video(video_id: str):
    """
    Trigger re-analysis of a video after deletion.
    
    This endpoint is used when a user wants to delete an existing analysis
    and immediately start a new analysis of the same video.
    
    Args:
        video_id (str): The video_id of the video to re-analyze
    
    Returns:
        dict: Message indicating re-analysis should be triggered on frontend
    """
    return {"message": "Video deleted successfully. Please restart analysis.", "video_id": video_id}

@app.post("/save-analysis/")
async def save_analysis(video_id: str):
    """
    Verify that analysis results are saved to database.
    
    Note: Analysis is automatically saved during the /analyze/ and /analyze-stream/ endpoints,
    so this endpoint primarily serves as a verification and retrieval endpoint.
    
    Args:
        video_id (str): Unique identifier (UUID) of the analyzed video
    
    Returns:
        dict: Status confirmation and retrieved analysis data
    
    Raises:
        HTTPException: 404 if video_id is not found in database
    """
    results = db.read_analysis(video_id)
    if not results:
        raise HTTPException(status_code=404, detail="Video not found")
    return {"status": "saved", "data": results}