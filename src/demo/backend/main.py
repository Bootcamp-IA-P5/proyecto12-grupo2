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

import json
import uuid
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Add parent directory to Python path to enable imports from sibling packages
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.log_setup import log_setup
from common.logger import Logger
from backend.database_manager import DatabaseManager
from backend.model_worker import BrandInspector


log_setup()


app = FastAPI()

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Intentar inicializar DatabaseManager, pero permitir que el backend funcione sin él
try:
    db = DatabaseManager()
    log = Logger().log
    log.info("DatabaseManager inicializado correctamente")
except Exception as e:
    db = None
    log = Logger().log
    log.warning(
        f"DatabaseManager no disponible (PostgreSQL no está corriendo): {e}")
    log.info("El backend funcionará sin guardar en base de datos")

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


@app.post("/analyze-image/")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze a single uploaded image for brand detection using YOLO.

    This endpoint accepts an image file upload (jpg, png, etc.), processes it with YOLO
    object detection, and returns all detected brands with confidence scores and locations.

    Args:
        file (UploadFile): Image file to analyze (supported formats: jpg, png, jpeg, bmp, etc.)

    Returns:
        dict: Detection results with keys:
            - status (str): "success" or "error"
            - video_id (str): UUID for this analysis (can be saved to DB)
            - title (str): Original filename
            - total_duration (float): 1 (images are treated as 1 second)
            - total_exposure_time (float): 1 if brands detected, 0 otherwise
            - visibility_percentage (float): 100 if brands detected, 0 otherwise
            - brands (dict): {brand_name: {detections, exposure_time, visibility}} for each brand
            - detections (list): Detailed list of all detections with brand, confidence, bbox

    Raises:
        HTTPException: 500 error if file processing or analysis fails
    """
    try:
        # Generate UUID for this image analysis
        image_id = str(uuid.uuid4())
        
        # Save uploaded file to temporary location for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # Run YOLO analysis on the image
            results = yolo.analyze_image(tmp_path, conf=0.25)
            
            if results is None:
                raise HTTPException(status_code=400, detail="Could not process image")

            # Transform results to match video analysis structure (for consistency)
            brands_detailed = {}
            for brand_name, confidences in results["brands"].items():
                brands_detailed[brand_name] = {
                    "detections": results["brand_counts"].get(brand_name, 0),
                    "exposure_time": 1.0,  # Image is "1 second" of exposure
                    "visibility": 100.0 if results["total_detections"] > 0 else 0.0,
                    "sample_images": []
                }

            return {
                "status": "success",
                "video_id": image_id,  # UUID for saving to database
                "title": file.filename,
                "total_duration": 1.0,  # Treat image as 1 second
                "total_exposure_time": 1.0 if results["total_detections"] > 0 else 0.0,
                "visibility_percentage": 100.0 if results["total_detections"] > 0 else 0.0,
                "brands": brands_detailed,
                "detections": results["detections_detail"]  # Extra info for debugging
            }

        finally:
            # Clean up temporary file
            Path(tmp_path).unlink(missing_ok=True)

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Image analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/")
async def analyze_video(file: UploadFile = File(...)):
    """
    Analyze an uploaded video file for brand exposure using YOLO detection.

    This endpoint accepts a video file upload, processes it frame-by-frame, and returns
    real-time streaming updates as a StreamingResponse with NDJSON format.

    Streaming Progress Format:
        - Progress objects (type="progress"): Sent during analysis with current frame metrics
        - Complete object (type="complete"): Sent at end with final results and video_id for storage
        - Error object (type="error"): Sent if analysis fails

    Args:
        file (UploadFile): Video file to analyze (supported formats: mp4, avi, mov, etc.)

    Returns:
        StreamingResponse: NDJSON-formatted stream with analysis progress and final results.
            Each line contains a JSON object with:
            - type: "progress", "complete", or "error"
            - For progress: timestamp, brands detected in frame, progress percentage, detected_seconds
            - For complete: video_id (UUID), title, exposure metrics, and brand breakdown

    Raises:
        HTTPException: 500 error if file processing or analysis fails
    """
    try:
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
                    # Rough estimate from frame count
                    total_duration = frame_info.get("frame_index", 0) / 30
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
                exposure_percent = (
                    total_detected / max(total_duration, 1) * 100) if total_duration > 0 else 0

                # Transform brands data to match frontend expectations
                # Frontend expects: {brand_name: {detections, exposure_time, visibility, sample_images}}
                # Backend has: {brand_name: count}
                brands_detailed = {}
                for brand_name, count in final_brands.items():
                    # Approximate exposure time per brand (proportional to detections)
                    brand_exposure = total_detected * (count / sum(final_brands.values())) if sum(final_brands.values()) > 0 else 0
                    brands_detailed[brand_name] = {
                        "detections": count,
                        "exposure_time": round(brand_exposure, 2),
                        "visibility": round((brand_exposure / max(total_duration, 1) * 100), 2) if total_duration > 0 else 0,
                        "sample_images": []  # TODO: implement frame capture for sample images
                    }

                # Save analysis to database for later retrieval (if database is available)
                analysis_record = {
                    "video_id": video_id,
                    "title": file.filename,
                    "detected_seconds": total_detected,
                    "total_duration": total_duration,
                    "brand_exposure_percent": exposure_percent,
                    "brands": final_brands,
                    "frames_data": frames_data
                }

                if db:
                    try:
                        db.create_analysis(analysis_record)
                        log.info(
                            f"Analysis saved to database with video_id: {video_id}")
                    except Exception as e:
                        log.warning(f"Failed to save to database: {e}")

                # Yield final result as NDJSON object (type="complete") with video_id for storage
                # Use frontend-expected field names: total_duration, total_exposure_time, visibility_percentage
                final_result = {
                    "status": "success",
                    "video_id": video_id,
                    "title": file.filename,
                    "total_duration": round(total_duration, 2),
                    "total_exposure_time": round(total_detected, 2),
                    "visibility_percentage": round(exposure_percent, 2),
                    "brands": brands_detailed
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

    Streaming Progress Format:
        - Progress objects (type="progress"): Sent during analysis with current frame metrics
        - Complete object (type="complete"): Sent at end with final results and video_id
        - Error object (type="error"): Sent if download or analysis fails

    Args:
        url (str): YouTube video URL to analyze

    Returns:
        StreamingResponse: NDJSON-formatted stream with analysis progress and final results.
            Each line contains a JSON object with:
            - type: "progress", "complete", or "error"
            - For progress: timestamp, brands detected, progress percentage, detected_seconds
            - For complete: video_id (UUID), title, exposure metrics, and brand breakdown

    Raises:
        HTTPException: 500 error if URL is invalid or analysis fails
    """
    try:
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
                exposure_percent = (
                    total_detected / max(total_duration, 1) * 100) if total_duration > 0 else 0

                # Transform brands data to match frontend expectations
                brands_detailed = {}
                for brand_name, count in final_brands.items():
                    brand_exposure = total_detected * (count / sum(final_brands.values())) if sum(final_brands.values()) > 0 else 0
                    brands_detailed[brand_name] = {
                        "detections": count,
                        "exposure_time": round(brand_exposure, 2),
                        "visibility": round((brand_exposure / max(total_duration, 1) * 100), 2) if total_duration > 0 else 0,
                        "sample_images": []
                    }

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

                # Store analysis results in database for later retrieval (if database is available)
                if db:
                    try:
                        db.create_analysis(analysis_record)
                        log.info(
                            f"Analysis saved to database with video_id: {video_id}")
                    except Exception as e:
                        log.warning(f"Failed to save to database: {e}")

                # Yield final result as NDJSON object (type="complete") with video_id for storage
                final_result = {
                    "status": "success",
                    "video_id": video_id,
                    "title": title,
                    "total_duration": round(total_duration, 2),
                    "total_exposure_time": round(total_detected, 2),
                    "visibility_percentage": round(exposure_percent, 2),
                    "brands": brands_detailed
                }

                yield json.dumps({"type": "complete", "result": final_result}) + "\n"

            except Exception as e:
                log.error(f"Stream analysis error: {e}")
                # Yield error as NDJSON object (type="error") so frontend can display error message
                yield json.dumps({"type": "error", "detail": str(e)}) + "\n"

        return StreamingResponse(generate_analysis(), media_type="application/x-ndjson")

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
        HTTPException: 404 if video_id is not found in database or database is unavailable
    """
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")

    results = db.read_analysis(video_id)
    if not results:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Transform database results to match frontend expectations
    detections = results.get("detections", [])
    
    # Group detections by brand and calculate metrics
    brand_stats = {}
    for detection in detections:
        brand = detection["brand_name"]
        if brand not in brand_stats:
            brand_stats[brand] = {
                "detections": 0,
                "timestamps": []
            }
        brand_stats[brand]["detections"] += 1
        brand_stats[brand]["timestamps"].append(detection["timestamp_sec"])
    
    # Calculate total video duration (max timestamp + 1 second buffer)
    all_timestamps = [d["timestamp_sec"] for d in detections]
    total_duration = max(all_timestamps) + 1 if all_timestamps else 0
    
    # Calculate exposure time (unique seconds with detections)
    unique_seconds = len(set(all_timestamps))
    total_exposure_time = unique_seconds
    
    # Calculate visibility percentage
    visibility_percentage = (total_exposure_time / max(total_duration, 1) * 100) if total_duration > 0 else 0
    
    # Build detailed brand data matching frontend structure
    brands_detailed = {}
    for brand_name, stats in brand_stats.items():
        unique_brand_seconds = len(set(stats["timestamps"]))
        brand_exposure = unique_brand_seconds
        brands_detailed[brand_name] = {
            "detections": stats["detections"],
            "exposure_time": round(brand_exposure, 2),
            "visibility": round((brand_exposure / max(total_duration, 1) * 100), 2) if total_duration > 0 else 0,
            "sample_images": []
        }
    
    # Return transformed data with frontend-expected field names
    return {
        "video_id": results["video_id"],
        "title": results["title"],
        "total_duration": round(total_duration, 2),
        "total_exposure_time": round(total_exposure_time, 2),
        "visibility_percentage": round(visibility_percentage, 2),
        "brands": brands_detailed
    }


@app.delete("/results/{video_id}")
async def delete_video(video_id: str):
    """
    Delete analysis results for a video from the database.

    Args:
        video_id (str): Unique identifier (UUID) of the analyzed video to delete

    Returns:
        dict: Confirmation status

    Raises:
        HTTPException: 503 if database is not available
    """
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")

    db.delete_analysis(video_id)
    return {"status": "deleted"}


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
        HTTPException: 503 if database is not available
    """
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")

    results = db.read_analysis(video_id)
    if not results:
        raise HTTPException(status_code=404, detail="Video not found")
    return {"status": "saved", "data": results}
