"""Frontend UI for BrandTracker AI.

This Streamlit application provides the user-facing interface to:
- submit YouTube URLs or upload video files,
- display a live progress bar and simple live results during analysis,
- and show/store final analysis results.

The heavy lifting is delegated to the FastAPI backend (`/analyze/` and
`/analyze-stream/`), which performs frame-by-frame YOLO inference and
returns newline-delimited JSON (NDJSON) progress updates. The frontend
parses the stream and updates UI elements in real time.

Usage:
    streamlit run src/demo/frontend/app.py

Notes:
    - Backend URL is provided by `BACKEND_URL` from `settings` (or
      environment). Ensure the backend is running before starting the UI.
    - The app stores results in `st.session_state.results` once analysis
      completes so the user can view stored data and the analysis ID.
"""

import sys
from pathlib import Path
import os
import json

# Ensure parent `demo/` directory is on sys.path so `common` imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import requests

from common.log_setup import log_setup
from common.logger import Logger
from settings import BACKEND_URL

log_setup()


class BrandAppUI(Logger):
    """Streamlit UI wrapper for the BrandTracker demo.

    Inherits a lightweight `Logger` to make debugging easier. The UI
    itself is implemented in the `run()` method which constructs the
    sidebar, the two analysis tabs (YouTube URL / Upload), and the
    results view.
    """

    def __init__(self, backend_url):
        """Store backend URL used for API calls.

        Args:
            backend_url (str): Base URL for the FastAPI backend.
        """
        self.url = backend_url

    def run(self):
        """Render the Streamlit interface and handle user interactions.

        The function builds three main areas:
        1. Sidebar: shows model information (brands available)
        2. Main tabs: allow entering a YouTube URL or uploading a file
           to analyze
        3. Results area: displays metrics and a small action panel
        for each completed analysis.
        """

        # --- Page Setup ---
        st.set_page_config(page_title="BrandTracker AI", layout="wide", page_icon="🛡️")

        # Tiny CSS to improve visual polish (keeps same look as original)
        st.markdown("""
        <style>
            .report-card { padding: 20px; background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; text-align: center; margin-bottom: 20px; }
            .brand-tag { display: inline-block; background-color: #dbeafe; color: #1e40af; padding: 5px 12px; border-radius: 20px; font-weight: bold; margin: 5px; }
            div[data-testid="stMetric"] { background-color: #ffffff; border: 1px solid #e2e8f0; padding: 15px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        </style>
        """, unsafe_allow_html=True)

        # Log and header
        self.log.debug("Starting Brand Recognition Demo UI")
        st.title("🛡️ BrandTracker AI")
        st.markdown("Automated recognition and branding exposure analytics.")

        # Keep results cached in session state so the user can inspect them
        if 'results' not in st.session_state:
            st.session_state.results = None
        
        # Initialize duplicate detection state
        if 'duplicate_detected' not in st.session_state:
            st.session_state.duplicate_detected = False
        if 'existing_video_id' not in st.session_state:
            st.session_state.existing_video_id = None
        if 'duplicate_title' not in st.session_state:
            st.session_state.duplicate_title = None

        # --- Sidebar: Model Info ---
        # This section calls the backend to retrieve model metadata (brands)
        with st.sidebar:
            st.header("Inspection Module")
            try:
                model_info = requests.get(f"{self.url}/model-info/").json()
                st.write("**Detectable Brands:**")
                for brand in model_info.get("brands", []):
                    st.code(brand)
            except Exception as e:
                # Fail gracefully if backend not reachable
                st.error(f"Could not load model info: {e}")

        # --- Main Input Section ---
        st.header("Analysis Mode")

        # Two tabs: one for YouTube URL analysis and one for file uploads
        tab1, tab2 = st.tabs(["YouTube URL", "Upload Video"])

        # --- YouTube URL tab ---
        with tab1:
            st.subheader("Analyze YouTube Video")
            
            # Check if we're handling a duplicate from a previous session
            if st.session_state.duplicate_detected and st.session_state.duplicate_title:
                st.warning(f"⚠️ Video '{st.session_state.duplicate_title}' already exists in database")
                
                # Create action buttons for duplicate handling
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📋 View Existing Analysis", key=f"view_existing_yt_session_{st.session_state.existing_video_id}"):
                        # Fetch and display existing analysis
                        try:
                            existing_response = requests.get(f"{self.url}/results/{st.session_state.existing_video_id}")
                            if existing_response.status_code == 200:
                                st.session_state.results = existing_response.json()
                                st.session_state.duplicate_detected = False
                                st.session_state.existing_video_id = None
                                st.session_state.duplicate_title = None
                                st.rerun()
                            else:
                                st.error("Could not retrieve existing analysis")
                        except Exception as e:
                            st.error(f"Error fetching existing analysis: {e}")
                
                with col2:
                    if st.button("🗑️ Delete Existing & Re-analyze", key=f"delete_existing_yt_session_{st.session_state.existing_video_id}"):
                        # Delete existing analysis and continue with new analysis
                        try:
                            delete_response = requests.delete(f"{self.url}/results/{st.session_state.existing_video_id}")
                            if delete_response.status_code == 200:
                                st.success("Existing analysis deleted. Starting new analysis...")
                                # Clear duplicate state and start analysis
                                st.session_state.duplicate_detected = False
                                st.session_state.existing_video_id = None
                                st.session_state.duplicate_title = None
                                st.session_state.analysis_started = True
                                st.rerun()
                            else:
                                st.error("Could not delete existing analysis")
                        except Exception as e:
                            st.error(f"Error deleting existing analysis: {e}")
                
                with col3:
                    if st.button("❌ Cancel", key=f"cancel_yt_session"):
                        st.info("Analysis cancelled. No changes made.")
                        st.session_state.duplicate_detected = False
                        st.session_state.existing_video_id = None
                        st.session_state.duplicate_title = None
                        st.session_state.analysis_started = False
                        st.rerun()
                
                # Don't show the analysis interface when handling duplicates
                return

            url = st.text_input("YouTube URL:", placeholder="Paste link here...")

            if st.button("🚀 Start Audit (YouTube)", type="primary", key="audit_yt"):
                if url:
                    try:
                        # Build a compact progress area (center column)
                        _, col_vid, _ = st.columns([1, 2, 1])
                        with col_vid:
                            video_placeholder = st.empty()

                        status_msg = st.empty()
                        progress_bar = st.progress(0)

                        # Request the backend endpoint that streams NDJSON progress
                        response = requests.post(
                            f"{self.url}/analyze-stream/",
                            params={"url": url},
                            stream=True,
                        )

                        # Parse and display streaming NDJSON lines as they arrive
                        if response.status_code == 200:
                            for line in response.iter_lines():
                                if not line:
                                    continue
                                data = json.loads(line)

                                if data.get("type") == "duplicate":
                                    # Handle duplicate video detection
                                    self.log.debug("Duplicate video detected in stream")
                                    existing_video_id = data.get("existing_video_id")
                                    title = data.get("title", "Unknown")
                                    message = data.get("message", "Video already exists")
                                    
                                    # Store duplicate state in session and trigger rerun to show duplicate interface
                                    st.session_state.duplicate_detected = True
                                    st.session_state.existing_video_id = existing_video_id
                                    st.session_state.duplicate_title = title
                                    
                                    # Show warning and break to display duplicate interface
                                    st.warning(f"⚠️ {message}")
                                    st.info("Please choose an action below:")
                                    st.rerun()

                                elif data.get("type") == "progress":
                                    progress = data.get("progress", 0)
                                    progress_bar.progress(min(progress, 1.0))

                                    timestamp = data.get("timestamp", 0)
                                    brands = data.get("brands", {})
                                    found_str = ", ".join(brands.keys()) if brands else "None"
                                    status_msg.markdown(f"**Time:** {timestamp}s | **Detected:** {data.get('detected_seconds', 0)}s | **Brands:** `{found_str}`")

                                elif data.get("type") == "complete":
                                    # Save the final result in session state
                                    st.session_state.results = data.get("result")
                                    progress_bar.progress(1.0)
                                    st.success("Analysis complete!")

                                elif data.get("type") == "error":
                                    st.error(f"Error: {data.get('detail')}")
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")
                else:
                    st.warning("Please enter a URL.")

        # --- Upload tab ---
        with tab2:
            st.subheader("Analyze Uploaded Video")
            
            # Check if we're handling a duplicate from a previous session
            if st.session_state.duplicate_detected and st.session_state.duplicate_title:
                st.warning(f"⚠️ Video '{st.session_state.duplicate_title}' already exists in database")
                
                # Create action buttons for duplicate handling
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📋 View Existing Analysis", key=f"view_existing_upload_session_{st.session_state.existing_video_id}"):
                        # Fetch and display existing analysis
                        try:
                            existing_response = requests.get(f"{self.url}/results/{st.session_state.existing_video_id}")
                            if existing_response.status_code == 200:
                                st.session_state.results = existing_response.json()
                                st.session_state.duplicate_detected = False
                                st.session_state.existing_video_id = None
                                st.session_state.duplicate_title = None
                                st.rerun()
                            else:
                                st.error("Could not retrieve existing analysis")
                        except Exception as e:
                            st.error(f"Error fetching existing analysis: {e}")
                
                with col2:
                    if st.button("🗑️ Delete Existing & Re-analyze", key=f"delete_existing_upload_session_{st.session_state.existing_video_id}"):
                        # Delete existing analysis and continue with new analysis
                        try:
                            delete_response = requests.delete(f"{self.url}/results/{st.session_state.existing_video_id}")
                            if delete_response.status_code == 200:
                                st.success("Existing analysis deleted. Starting new analysis...")
                                # Clear duplicate state and start analysis
                                st.session_state.duplicate_detected = False
                                st.session_state.existing_video_id = None
                                st.session_state.duplicate_title = None
                                st.session_state.analysis_started = True
                                st.rerun()
                            else:
                                st.error("Could not delete existing analysis")
                        except Exception as e:
                            st.error(f"Error deleting existing analysis: {e}")
                
                with col3:
                    if st.button("❌ Cancel", key=f"cancel_upload_session"):
                        st.info("Analysis cancelled. No changes made.")
                        st.session_state.duplicate_detected = False
                        st.session_state.existing_video_id = None
                        st.session_state.duplicate_title = None
                        st.session_state.analysis_started = False
                        st.rerun()
                
                # Don't show the analysis interface when handling duplicates
                return

            uploaded_file = st.file_uploader("Upload Video", type=['mp4', 'avi', 'mov', 'mkv'])

            if st.button("🚀 Start Audit (Upload)", type="primary", key="audit_upload"):
                if uploaded_file:
                    try:
                        _, col_vid, _ = st.columns([1, 2, 1])
                        with col_vid:
                            video_placeholder = st.empty()

                        status_msg = st.empty()
                        progress_bar = st.progress(0)

                        # Send file to backend analyze endpoint and stream progress
                        files = {"file": uploaded_file}
                        response = requests.post(
                            f"{self.url}/analyze/",
                            files=files,
                            stream=True,
                        )

                        if response.status_code == 200:
                            for line in response.iter_lines():
                                if not line:
                                    continue
                                data = json.loads(line)

                                if data.get("type") == "duplicate":
                                    # Handle duplicate video detection
                                    self.log.debug("Duplicate video detected in stream")
                                    existing_video_id = data.get("existing_video_id")
                                    title = data.get("title", "Unknown")
                                    message = data.get("message", "Video already exists")
                                    
                                    # Store duplicate state in session and trigger rerun to show duplicate interface
                                    st.session_state.duplicate_detected = True
                                    st.session_state.existing_video_id = existing_video_id
                                    st.session_state.duplicate_title = title
                                    
                                    # Show warning and break to display duplicate interface
                                    st.warning(f"⚠️ {message}")
                                    st.info("Please choose an action below:")
                                    st.rerun()

                                elif data.get("type") == "progress":
                                    progress = data.get("progress", 0)
                                    progress_bar.progress(min(progress, 1.0))

                                    timestamp = data.get("timestamp", 0)
                                    brands = data.get("brands", {})
                                    found_str = ", ".join(brands.keys()) if brands else "None"
                                    status_msg.markdown(f"**Time:** {timestamp}s | **Detected:** {data.get('detected_seconds', 0)}s | **Brands:** `{found_str}`")

                                elif data.get("type") == "complete":
                                    st.session_state.results = data.get("result")
                                    progress_bar.progress(1.0)
                                    st.success("Analysis complete!")
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Upload error: {e}")
                else:
                    st.warning("Please select a video file.")

        # --- Results Section ---
        if st.session_state.results:
            res = st.session_state.results
            title = res.get('title', 'Video Analysis')
            exposure = res.get('exposure_seconds', 0)
            total = res.get('total_seconds', 0)
            brands = res.get('brands', {})
            percent = res.get('exposure_percent', 0)
            video_id = res.get('video_id', 'N/A')

            st.divider()
            st.header(f"📊 Audit Report: {title}")

            # Metrics Row
            m1, m2, m3 = st.columns(3)
            m1.metric("Brand Exposure", f"{exposure}s")
            m2.metric("Total Video Time", f"{int(total)}s")
            m3.metric("Visibility Share", f"{percent:.1f}%")

            # Video ID (useful to query backend or the DB)
            st.write(f"**Analysis ID:** `{video_id}`")

            # Brand Breakdown (simple cards)
            st.subheader("Brand Recognition Breakdown")
            if brands:
                cols = st.columns(len(brands) if len(brands) < 4 else 4)
                for i, (name, count) in enumerate(brands.items()):
                    with cols[i % len(cols)]:
                        st.markdown(f"""
                        <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; padding: 10px; border-radius: 8px; text-align: center;">
                            <div style="color: #1e40af; font-weight: bold;">{name.upper()}</div>
                            <div style="font-size: 20px;">{count}s</div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.write("No specific brands identified.")

            st.markdown("<br>", unsafe_allow_html=True)

            # Actions: provide useful operations for the completed analysis
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📋 Copy Analysis ID"):
                    # Display the ID in code block so user can copy it
                    st.code(video_id)
                    st.info("Analysis ID copied to clipboard (visible above)")

            with col2:
                if st.button("🔍 View in Database"):
                    # Show the stored JSON result for verification
                    if st.session_state.results:
                        st.write("**Stored Data:**")
                        st.json(st.session_state.results)

            with col3:
                if st.button("🔄 Start New Analysis"):
                    st.session_state.results = None
                    st.rerun()


if __name__ == "__main__":
    # Default backend URL is taken from settings; override via environment
    backend = os.getenv("BACKEND_URL", BACKEND_URL)
    ui = BrandAppUI(backend_url=backend)
    ui.run()