"""
Brand Detection Model Worker using YOLO
========================================

This module provides the BrandInspector class, which integrates the YOLO object detection
model to analyze videos for brand exposure. It supports both local video files and YouTube URL
streaming with real-time frame-by-frame brand detection.

Key Features:
    - Generator-based analysis: yields frame data during processing for real-time updates
    - Adaptive frame sampling: processes 1 frame per second to balance speed and accuracy
    - Brand tracking: accumulates brand detections across frames and counts occurrences
    - Confidence filtering: configurable confidence threshold for detections
    - YouTube support: automatic URL resolution and stream handling with fallback

Analysis Output:
    Each yielded frame dictionary contains:
        - timestamp: current position in video (seconds)
        - brands: dictionary of brands detected in this frame with confidence scores
        - progress: analysis progress as float 0-1
        - detected_seconds: cumulative seconds with any brand detection
        - brand_counts: cumulative count of brand appearances across processed frames
        - title/duration: (YouTube only) video metadata

Dependencies:
    - YOLO: ultralytics model for object detection
    - cv2: OpenCV for video capture and frame processing
    - yt_dlp: YouTube video resolution and downloading
    - Logger: structured logging from common module
"""

import yt_dlp
from settings import YOLO_MODEL_ORG
from ultralytics import YOLO
import numpy as np
import cv2
from common.logger import Logger
from common.log_setup import log_setup
import sys
from pathlib import Path

# Add parent directory to Python path to enable imports from sibling packages
sys.path.insert(0, str(Path(__file__).parent.parent))


log_setup()


class BrandInspector(Logger):
    """
    YOLO-based brand detection system for video analysis.

    This class wraps the YOLO object detection model and provides methods to analyze
    videos (both local files and YouTube URLs) for brand exposure. Analysis is performed
    using generator functions that yield frame-by-frame results, enabling real-time
    progress updates in the frontend.

    Attributes:
        model (YOLO): Ultralytics YOLO model instance loaded from checkpoint (lazy-loaded)
    """

    def __init__(self, model_path=YOLO_MODEL_ORG):
        """
        Initialize the BrandInspector with a YOLO model (lazy loading).

        Args:
            model_path (str): Path to YOLO model weights file (default from settings)
        """
        self.model_path = model_path
        self.model = None  # Lazy loading - will load on first use

    def _get_model(self):
        """Load model on first use (lazy loading)."""
        if self.model is None:
            self.log.debug(f"Loading YOLO model from: {self.model_path}")
            self.model = YOLO(self.model_path)
            self.log.info("YOLO model loaded successfully")
        return self.model

    def analyze_local_video_stream(self, video_path, conf=0.25):
        """
        Analyze a local video file frame-by-frame and yield brand detection results.

        This generator function opens a video file and processes it at ~1 frame per second
        to reduce computation while maintaining temporal coverage. For each processed frame,
        it runs YOLO inference and yields detection results with metadata.

        Frame Sampling:
            - Reads all frames from video to maintain accurate frame count
            - Only processes 1 frame per second (based on fps) to optimize performance
            - Maintains frame count for accurate progress percentage calculation

        Args:
            video_path (str): Path to local video file
            conf (float): YOLO confidence threshold for detections (0-1, default 0.25)

        Yields:
            dict: Frame analysis results with keys:
                - timestamp (int): Current time in seconds
                - brands (dict): {brand_name: [confidence_scores]} detected in this frame
                - frame_index (int): Total frame number processed so far
                - progress (float): Completion percentage (0-1)
                - detected_seconds (int): Cumulative seconds with any brand detection
                - brand_counts (dict): {brand_name: count} total detections across all frames

        Raises:
            Returns None if video file cannot be opened
        """
        self.log.debug(f"Analyzing local video: {video_path}")

        # Open video capture from file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            self.log.error(f"Could not open video: {video_path}")
            return None

        # Extract video metadata for progress calculation and frame sampling
        # Default to 30 fps if unavailable
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0

        # Initialize tracking variables
        detected_seconds = 0  # Counter for seconds with brand detections
        brand_counts = {}     # Dictionary to accumulate brand detection counts
        frame_count = 0       # Total frames processed
        processed_frames = 0  # Frames sent for inference (1 per second)

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1

                # Frame sampling: process 1 frame per second to save CPU
                # (e.g., at 30fps, process frames 30, 60, 90, etc.)
                if frame_count % int(fps) == 0:
                    processed_frames += 1
                    current_sec = int(frame_count / fps)

                    # Run YOLO inference on this frame
                    results = self._get_model().predict(frame, conf=conf, device='cpu', verbose=False)

                    # Track brands detected in this specific frame
                    brands_this_frame = {}
                    if len(results[0].boxes) > 0:
                        detected_seconds += 1  # Increment counter since brands were found

                        # Iterate through detections and extract brand info
                        for box in results[0].boxes:
                            cls_id = int(box.cls[0])  # Class ID from detection
                            # Convert ID to brand name
                            brand_name = self._get_model().names[cls_id]
                            # Detection confidence score
                            confidence = float(box.conf[0])

                            # Store confidence scores for this brand in this frame
                            if brand_name not in brands_this_frame:
                                brands_this_frame[brand_name] = []
                            brands_this_frame[brand_name].append(confidence)

                        # Update cumulative brand counts (how many times each brand appears)
                        for br, confidences in brands_this_frame.items():
                            brand_counts[br] = brand_counts.get(br, 0) + 1

                    # Calculate progress percentage for frontend progress bar
                    progress = (
                        frame_count / total_frames) if total_frames > 0 else 0

                    # Yield frame data as NDJSON object for real-time frontend updates
                    yield {
                        "timestamp": current_sec,
                        "brands": brands_this_frame,
                        "frame_index": frame_count,
                        "progress": progress,
                        "detected_seconds": detected_seconds,
                        "brand_counts": dict(brand_counts)
                    }

        finally:
            # Always close video capture to free resources
            cap.release()

        self.log.debug(
            f"Analysis complete: {detected_seconds}s detected, {len(brand_counts)} unique brands")

    def analyze_stream(self, url, conf=0.25):
        """
        Analyze a video from a YouTube URL frame-by-frame and yield brand detection results.

        This generator function handles YouTube URL resolution, stream extraction, and frame-by-frame
        analysis. It uses yt_dlp to extract the best available video stream within bandwidth constraints,
        then processes it similarly to analyze_local_video_stream() with 1 frame per second sampling.

        YouTube Stream Resolution:
            - Primary format: best video [height<=480] + best audio (mp4/m4a)
            - Fallback format: best overall [height<=480] if primary fails
            - Automatic error handling with fallback strategy

        Args:
            url (str): YouTube video URL to analyze
            conf (float): YOLO confidence threshold for detections (0-1, default 0.8)

        Yields:
            dict: Frame analysis results with keys:
                - title (str): Video title from YouTube metadata
                - duration (int): Total video duration in seconds
                - timestamp (int): Current time in seconds
                - brands (dict): {brand_name: [confidence_scores]} detected in this frame
                - progress (float): Completion percentage (0-1)
                - detected_seconds (int): Cumulative seconds with any brand detection
                - brand_counts (dict): {brand_name: count} total detections across all frames

        Raises:
            Returns None if URL is invalid or stream cannot be opened
        """
        self.log.debug(f"Analyzing stream: {url}")

        # Configure yt_dlp options for optimal stream extraction
        ydl_opts = {
            'format': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best',
            'quiet': True,  # Suppress yt_dlp logging
            'no_warnings': True,
            'noplaylist': True,
        }

        try:
            # Extract video metadata and direct stream URL using yt_dlp
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                meta = ydl.extract_info(url, download=False)
                stream_url = meta.get('url')
                title = meta.get('title', 'Video Stream')
                duration = meta.get('duration', 0)
                fps = meta.get('fps', 30) or 30
        except Exception as e:
            self.log.error(f"Stream extraction error: {e}")
            return None

        # Attempt to open the extracted stream URL
        cap = cv2.VideoCapture(stream_url)

        # Fallback: if primary format fails, try alternative format
        if not cap.isOpened():
            self.log.warning("Primary stream failed, attempting fallback")
            # Use best overall instead of separated streams
            ydl_opts['format'] = 'best[height<=480]'
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    meta = ydl.extract_info(url, download=False)
                    stream_url = meta.get('url')
                    cap = cv2.VideoCapture(stream_url)
            except Exception as e:
                self.log.error(f"Fallback stream extraction failed: {e}")
                return None

        # Final check: ensure stream is accessible
        if not cap.isOpened():
            self.log.error("Could not open stream")
            return None

        # Initialize tracking variables
        detected_seconds = 0  # Counter for seconds with brand detections
        brand_counts = {}     # Dictionary to accumulate brand detection counts
        frame_count = 0       # Total frames processed
        processed_frames = 0  # Frames sent for inference (1 per second)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)
                           ) or 3600  # Estimate if unknown

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1

                # Frame sampling: process 1 frame per second to save CPU and bandwidth
                if frame_count % int(fps) == 0:
                    processed_frames += 1
                    current_sec = int(frame_count / fps)

                    # Run YOLO inference on this frame
                    results = self._get_model().predict(frame, conf=conf, device='cpu', verbose=False)

                    # Track brands detected in this specific frame
                    brands_this_frame = {}
                    if len(results[0].boxes) > 0:
                        detected_seconds += 1  # Increment counter since brands were found

                        # Iterate through detections and extract brand info
                        for box in results[0].boxes:
                            cls_id = int(box.cls[0])  # Class ID from detection
                            # Convert ID to brand name
                            brand_name = self._get_model().names[cls_id]
                            # Detection confidence score
                            confidence = float(box.conf[0])

                            # Store confidence scores for this brand in this frame
                            if brand_name not in brands_this_frame:
                                brands_this_frame[brand_name] = []
                            brands_this_frame[brand_name].append(confidence)

                        # Update cumulative brand counts (how many times each brand appears)
                        for br, confidences in brands_this_frame.items():
                            brand_counts[br] = brand_counts.get(br, 0) + 1

                    # Calculate progress percentage for frontend progress bar
                    progress = (
                        frame_count / total_frames) if total_frames > 0 else 0

                    # Yield frame data as NDJSON object for real-time frontend updates
                    yield {
                        "title": title,
                        "duration": duration,
                        "timestamp": current_sec,
                        "brands": brands_this_frame,
                        "progress": progress,
                        "detected_seconds": detected_seconds,
                        "brand_counts": dict(brand_counts)
                    }

        finally:
            # Always close stream to free resources
            cap.release()

        self.log.debug(
            f"Stream analysis complete: {detected_seconds}s detected")

    def analyze_image(self, image_path, conf=0.25):
        """
        Analyze a single image for brand detection using YOLO.

        This method processes a static image and returns all detected brands with their
        confidence scores and bounding box information.

        Args:
            image_path (str): Path to image file to analyze
            conf (float): YOLO confidence threshold for detections (0-1, default 0.25)

        Returns:
            dict: Detection results with keys:
                - brands (dict): {brand_name: [confidence_scores]} detected in image
                - total_detections (int): Total number of brand detections
                - brand_counts (dict): {brand_name: count} occurrences of each brand
                - detections_detail (list): Detailed detection info with boxes and confidence
            Returns None if image cannot be opened

        Raises:
            Logs errors but returns None instead of raising (safe for API responses)
        """
        self.log.debug(f"Analyzing image: {image_path}")

        # Read image file
        image = cv2.imread(image_path)
        if image is None:
            self.log.error(f"Could not open image: {image_path}")
            return None

        try:
            # Run YOLO inference on the image
            results = self._get_model().predict(image, conf=conf, device='cpu', verbose=False)

            # Track brands detected in this image
            brands_in_image = {}
            brand_counts = {}
            detections_detail = []

            if len(results[0].boxes) > 0:
                # Iterate through detections and extract brand info
                for box in results[0].boxes:
                    cls_id = int(box.cls[0])  # Class ID from detection
                    brand_name = self._get_model().names[cls_id]  # Convert ID to brand name
                    confidence = float(box.conf[0])  # Detection confidence score
                    
                    # Get bounding box coordinates [x1, y1, x2, y2]
                    bbox = box.xyxy[0].tolist()

                    # Store confidence scores for this brand
                    if brand_name not in brands_in_image:
                        brands_in_image[brand_name] = []
                        brand_counts[brand_name] = 0
                    
                    brands_in_image[brand_name].append(confidence)
                    brand_counts[brand_name] += 1

                    # Add detailed detection info
                    detections_detail.append({
                        "brand_name": brand_name,
                        "confidence": round(confidence, 3),
                        "bbox": [round(coord, 2) for coord in bbox]
                    })

            self.log.debug(
                f"Image analysis complete: {len(detections_detail)} detections, "
                f"{len(brand_counts)} unique brands"
            )

            return {
                "brands": brands_in_image,
                "total_detections": len(detections_detail),
                "brand_counts": dict(brand_counts),
                "detections_detail": detections_detail
            }

        except Exception as e:
            self.log.error(f"Error analyzing image: {e}")
            return None

    def get_model_info(self):
        """
        Retrieve metadata about the YOLO model and its detectable brands.

        Returns:
            dict: Model information with keys:
                - brands (list): List of all brand names the model can detect
                - num_classes (int): Total number of detectable classes/brands
        """
        return {
            "brands": list(self._get_model().names.values()),
            "num_classes": len(self._get_model().names)
        }
