import sys
import json
import os
import requests
import streamlit as st
from pathlib import Path

# Ensure parent `demo/` directory is on sys.path so `common` imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.log_setup import log_setup
from common.logger import Logger
from settings import BACKEND_URL

log_setup()

class BrandAppUI(Logger):
    def __init__(self, backend_url):
        self.url = backend_url
        self._init_session_state()

    def _init_session_state(self):
        if 'results' not in st.session_state:
            st.session_state.results = None
        if 'duplicate_info' not in st.session_state:
            st.session_state.duplicate_info = None

    def _process_raw_detections(self, res_data):
        """
        Converts raw database detections into displayable metrics.
        Handles both the streaming 'complete' format and the DB 'results' format.
        """
        detections = res_data.get("detections", [])
        
        # If the backend already sent a summary, use it; otherwise, calculate it
        if "exposure_seconds" in res_data:
            return res_data

        # Calculate metrics from raw detections
        unique_timestamps = {d["timestamp_sec"] for d in detections}
        brand_counts = {}
        for d in detections:
            brand = d["brand_name"]
            # We count unique seconds per brand
            if brand not in brand_counts:
                brand_counts[brand] = set()
            brand_counts[brand].add(d["timestamp_sec"])
        
        # Convert sets to duration
        brand_durations = {k: len(v) for k, v in brand_counts.items()}
        
        # Estimate total video time from last detection if not provided
        total_time = res_data.get("total_seconds") or (max(unique_timestamps) if unique_timestamps else 0)
        exposure_seconds = len(unique_timestamps)
        
        return {
            "title": res_data.get("title", "Unknown Video"),
            "exposure_seconds": exposure_seconds,
            "total_seconds": total_time,
            "exposure_percent": (exposure_seconds / total_time * 100) if total_time > 0 else 0,
            "brands": brand_durations,
            "video_id": res_data.get("video_id", "N/A"),
            "detections": detections  # Keep original detections with crop_path for image display
        }

    @st.dialog("Duplicate Analysis Found")
    def handle_duplicate_dialog(self, info):
        st.warning(f"⚠️ The video **'{info['title']}'** has already been analyzed.")
        col1, col2, col3 = st.columns(3)
        
        if col1.button("📋 View Existing", use_container_width=True):
            try:
                res = requests.get(f"{self.url}/results/{info['existing_video_id']}")
                if res.status_code == 200:
                    # Crucial: Process the raw DB response before storing
                    st.session_state.results = self._process_raw_detections(res.json())
                    st.session_state.duplicate_info = None
                    st.rerun()
            except Exception as e:
                st.error(f"Error fetching: {e}")

        if col2.button("🗑️ Overwrite", use_container_width=True):
            try:
                requests.delete(f"{self.url}/results/{info['existing_video_id']}")
                st.session_state.duplicate_info = None
                st.info("Deleted. You can now start a new analysis.")
                st.rerun()
            except Exception as e:
                st.error(f"Error deleting: {e}")

        if col3.button("❌ Cancel", use_container_width=True):
            st.session_state.duplicate_info = None
            st.rerun()

    def _process_analysis_stream(self, response):
        status_msg = st.empty()
        progress_bar = st.progress(0)
        
        for line in response.iter_lines():
            if not line: continue
            data = json.loads(line)
            
            if data.get("type") == "duplicate":
                st.session_state.duplicate_info = {
                    "existing_video_id": data.get("existing_video_id"),
                    "title": data.get("title", "Unknown")
                }
                st.rerun()
            elif data.get("type") == "progress":
                progress_bar.progress(min(data.get("progress", 0.0), 1.0))
                status_msg.write(f"Processing... {data.get('timestamp')}s")
            elif data.get("type") == "complete":
                # Process the result before saving
                st.session_state.results = self._process_raw_detections(data.get("result"))
                st.rerun()

    def run(self):
        st.set_page_config(page_title="BrandTracker AI", layout="wide")
        
        if st.session_state.duplicate_info:
            self.handle_duplicate_dialog(st.session_state.duplicate_info)

        st.title("🛡️ BrandTracker AI")
        
        # Add a new tab for viewing previous analyses
        tab1, tab2, tab3 = st.tabs(["YouTube", "Upload", "Previous Analyses"])
        with tab1:
            url = st.text_input("YouTube URL")
            if st.button("Analyze Link"):
                res = requests.post(f"{self.url}/analyze-stream/", params={"url": url}, stream=True)
                self._process_analysis_stream(res)
        
        with tab2:
            file = st.file_uploader("Video File")
            if st.button("Analyze Upload"):
                res = requests.post(f"{self.url}/analyze/", files={"file": file}, stream=True)
                self._process_analysis_stream(res)

        with tab3:
            # Display previous analyses
            st.subheader("Select a previous analysis to view:")
            video_list = self.get_previous_analyses()
            if video_list:
                # Create a mapping of titles to video_ids for easy lookup
                title_to_id = {video['title']: video['video_id'] for video in video_list}
                titles = list(title_to_id.keys())
                
                selected_title = st.selectbox("Choose analysis", titles)
                if st.button("Show Analysis"):
                    selected_video_id = title_to_id[selected_title]
                    self.show_previous_analysis(selected_video_id)
            else:
                st.info("No previous analyses found.")

            if st.session_state.results:
                self.render_results(st.session_state.results)

    def render_results(self, res):
        st.divider()
        st.header(f"📊 Audit Report: {res['title']}")
        
        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Brand Exposure", f"{res['exposure_seconds']}s")
        m2.metric("Total Video", f"{int(res['total_seconds'])}s")
        m3.metric("Visibility Share", f"{res['exposure_percent']:.1f}%")

        # Brands
        st.subheader("Detected Brands")
        if res['brands']:
            cols = st.columns(len(res['brands']))
            for i, (name, sec) in enumerate(res['brands'].items()):
                with cols[i]:
                    st.success(f"**{name}**\n\n{sec}s total")

        # Display images if available
        if res.get('detections'):
            st.subheader("Detected Images")
            image_cols = st.columns(3)
            for i, detection in enumerate(res['detections']):
                if detection.get('crop_path'):
                    with image_cols[i % 3]:
                        st.image(detection['crop_path'], caption=f"{detection['brand_name']} at {detection['timestamp_sec']}s", width=200)

        # Action Bar
        with st.expander("View Raw Data"):
            st.json(res)
            
        if st.button("Start New Analysis"):
            st.session_state.results = None
            st.rerun()

    def get_previous_analyses(self):
        """Get list of previous analysis video titles and IDs from the backend"""
        try:
            res = requests.get(f"{self.url}/results/")
            if res.status_code == 200:
                videos = res.json()
                # Return list of dictionaries with title and video_id
                return [{'title': video.get('title', f"Video {video['video_id'][:8]}..."), 'video_id': video['video_id']} for video in videos]
        except Exception as e:
            st.error(f"Error fetching previous analyses: {e}")
        return []

    def show_previous_analysis(self, video_id):
        """Fetch and display a previous analysis"""
        try:
            res = requests.get(f"{self.url}/results/{video_id}")
            if res.status_code == 200:
                st.session_state.results = self._process_raw_detections(res.json())
                st.rerun()
        except Exception as e:
            st.error(f"Error fetching analysis: {e}")

if __name__ == "__main__":
    ui = BrandAppUI(os.getenv("BACKEND_URL", BACKEND_URL))
    ui.run()