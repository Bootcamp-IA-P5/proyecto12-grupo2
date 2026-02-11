import sys
import json
import os
import requests
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# Ensure parent `demo/` directory is on sys.path so `common` imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.log_setup import log_setup
from common.logger import Logger
from settings import BACKEND_URL, DEFAULT_CONFIDENCE

log_setup()

class BrandAppUI(Logger):
    def __init__(self, backend_url):
        self.url = backend_url
        self._init_session_state()

    def _init_session_state(self):
        # Initialize session state variables for results
        if 'youtube_results' not in st.session_state:
            st.session_state.youtube_results = None
        if 'upload_results' not in st.session_state:
            st.session_state.upload_results = None
        if 'previous_results' not in st.session_state:
            st.session_state.previous_results = None

        # Duplicate info is stored separately to trigger the dialog when needed
        if 'duplicate_info' not in st.session_state:
            st.session_state.duplicate_info = None
        if 'duplicate_info' not in st.session_state:
            st.session_state.duplicate_info = None

        # Track which tab is currently active to manage results display context
        if 'current_tab' not in st.session_state:
            st.session_state.current_tab = 'youtube'
        if 'youtube_results' not in st.session_state:
            st.session_state.youtube_results = None
        if 'upload_results' not in st.session_state:
            st.session_state.upload_results = None
        if 'previous_results' not in st.session_state:
            st.session_state.previous_results = None

    def _process_raw_detections(self, res_data):
        """
        Converts raw database detections into displayable metrics.
        Handles both the streaming 'complete' format and the DB 'results' format.
        """
        detections = res_data.get("detections", [])
        
        # If the backend already sent a summary, use it; otherwise, calculate it
        if "exposure_seconds" in res_data:
            # Ensure backward compatibility: if brand_visibility_percent is missing, calculate it
            if "brand_visibility_percent" not in res_data and "brands" in res_data and "total_seconds" in res_data:
                brand_visibility_percent = {}
                total_duration = res_data.get("total_seconds", 0)
                if total_duration > 0:
                    for brand, seconds in res_data["brands"].items():
                        brand_visibility_percent[brand] = (seconds / total_duration) * 100
                res_data["brand_visibility_percent"] = brand_visibility_percent
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
        
        # Calculate per-brand visibility percentages for backward compatibility
        brand_visibility_percent = {}
        if total_time > 0:
            for brand, seconds in brand_durations.items():
                brand_visibility_percent[brand] = (seconds / total_time) * 100
        
        return {
            "title": res_data.get("title", "Unknown Video"),
            "exposure_seconds": exposure_seconds,
            "total_seconds": total_time,
            "exposure_percent": (exposure_seconds / total_time * 100) if total_time > 0 else 0,
            "brands": brand_durations,
            "brand_visibility_percent": brand_visibility_percent,
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

    def _process_analysis_stream(self, response, tab_type):
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
                results = self._process_raw_detections(data.get("result"))

                if tab_type == 'youtube':
                    st.session_state.youtube_results = results
                    st.session_state.upload_results = None
                    st.session_state.previous_results = None
                elif tab_type == 'upload':
                    st.session_state.upload_results = results
                    st.session_state.youtube_results = None
                    st.session_state.previous_results = None
                elif tab_type == 'previous':
                    st.session_state.previous_results = results
                    st.session_state.youtube_results = None
                    st.session_state.upload_results = None

                st.rerun()

    def run(self):
        st.set_page_config(page_title="BrandTracker AI", layout="wide")
        
        if st.session_state.duplicate_info:
            self.handle_duplicate_dialog(st.session_state.duplicate_info)

        st.title("🛡️ BrandTracker AI")

        # Set current tab based on which tab is active
        tab1, tab2, tab3 = st.tabs(["YouTube", "Upload", "Previous Analyses"])
        
        with tab1:
            st.session_state.current_tab = 'youtube'
            url = st.text_input("YouTube URL")

            # Add confidence slider
            confidence = st.slider(
                "Confidence Threshold",
                key="tab01",
                min_value=0.0,
                max_value=1.0,
                value=DEFAULT_CONFIDENCE,
                step=0.05,
                help="Minimum confidence score for brand detection (0.0 = very sensitive, 1.0 = very strict)"
            )

            if st.button("Analyze Link"):
                res = requests.post(f"{self.url}/analyze-stream/", 
                                    params={"url": url, "confidence": confidence}, 
                                    stream=True)
                self._process_analysis_stream(res, 'youtube')

            if st.session_state.youtube_results:
                self.render_results(st.session_state.youtube_results)
        
        with tab2:
            st.session_state.current_tab = 'upload'
            file = st.file_uploader("Video/Image File")

            # Add confidence slider
            confidence = st.slider(
                "Confidence Threshold",
                key="tab2",
                min_value=0.0,
                max_value=1.0,
                value=DEFAULT_CONFIDENCE,
                step=0.05,
                help="Minimum confidence score for brand detection (0.0 = very sensitive, 1.0 = very strict)"
            )

            if st.button("Analyze Upload"):
                res = requests.post(f"{self.url}/analyze/", 
                                    files={"file": file}, 
                                    params={"confidence": confidence},
                                    stream=True)
                self._process_analysis_stream(res, 'upload')

            if st.session_state.upload_results:
                self.render_results(st.session_state.upload_results)

        with tab3:
            # Display previous analyses
            st.session_state.current_tab = 'previous'
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

            if st.session_state.previous_results:
                self.render_results(st.session_state.previous_results)

    def render_results(self, res):
        st.divider()
        
        # Determine if this is an image or video analysis
        is_image = res.get('total_seconds', 0) == 0 and res.get('exposure_seconds', 0) > 0
        
        if is_image:
            st.header(f"📸 Image Analysis: {res['title']}")
        else:
            st.header(f"📊 Audit Report: {res['title']}")
        
        # Metrics
        m1, m2, m3 = st.columns(3)
        if is_image:
            m1.metric("Brand Detections", f"{res['exposure_seconds']}")
            m2.metric("Analysis Type", "Image")
            m3.metric("Detection Rate", f"{res['exposure_percent']:.1f}%")
        else:
            m1.metric("Brand Exposure", f"{res['exposure_seconds']}s")
            m2.metric("Total Video", f"{int(res['total_seconds'])}s")
            m3.metric("Visibility Share", f"{res['exposure_percent']:.1f}%")

        # Brands
        st.subheader("Detected Brands")
        if res['brands']:
            # Create visualization for brand visibility distribution (video only)
            if not is_image and res.get('brand_visibility_percent'):
                # Prepare data for visualization
                brands = list(res['brands'].keys())
                visibility_percentages = [res['brand_visibility_percent'].get(brand, 0) for brand in brands]
                total_seconds = [res['brands'][brand] for brand in brands]
                
                # Display brand cards
                cols = st.columns(len(res['brands']))
                for i, (name, count_or_sec) in enumerate(res['brands'].items()):
                    with cols[i]:
                        # Display brand name, total seconds, and visibility percentage
                        brand_seconds = count_or_sec
                        brand_visibility = res.get('brand_visibility_percent', {}).get(name, 0)
                        st.success(f"**{name}**\n\n⏱️ {brand_seconds}s total\n\n📊 {brand_visibility:.1f}% visibility")
                
                # Create pie chart for brand visibility distribution
                fig = px.pie(
                    values=visibility_percentages,
                    names=brands,
                    title="Brand Visibility Distribution",
                    hole=0.3,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(
                    title_font_size=16,
                    showlegend=True,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                # For images or when no visibility data, use original layout
                cols = st.columns(len(res['brands']))
                for i, (name, count_or_sec) in enumerate(res['brands'].items()):
                    with cols[i]:
                        if is_image:
                            st.success(f"**{name}**\n\n{count_or_sec} detections")
                        else:
                            # Display brand name, total seconds, and visibility percentage
                            brand_seconds = count_or_sec
                            brand_visibility = res.get('brand_visibility_percent', {}).get(name, 0)
                            st.success(f"**{name}**\n\n⏱️ {brand_seconds}s total\n\n📊 {brand_visibility:.1f}% visibility")

        # Display images if available
        if res.get('detections'):
            st.subheader("Detected Images")
            image_cols = st.columns(3)
            for i, detection in enumerate(res['detections']):
                if detection.get('crop_path'):
                    with image_cols[i % 3]:
                        # Extract confidence from the detection data
                        confidence = detection.get('confidence', 0.0)
                        confidence_percent = f"{confidence * 100:.1f}%"
                        
                        # Display image
                        st.image(detection['crop_path'], width=200)
                        
                        # Display information below the image using markdown
                        st.markdown(f"**{detection['brand_name']}**")
                        if is_image:
                            st.markdown(f"🎯 Confidence: {confidence_percent}")
                        else:
                            st.markdown(f"⏱️ {detection['timestamp_sec']}s")
                            st.markdown(f"🎯 Confidence: {confidence_percent}")

        # Action Bar
        with st.expander("View Raw Data"):
            st.json(res)
            
        if st.button("Start New Analysis"):
            st.session_state.youtube_results = None
            st.session_state.upload_results = None
            st.session_state.previous_results = None
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
                st.session_state.youtube_results = None
                st.session_state.upload_results = None
                st.session_state.previous_results = st.session_state.results
                st.rerun()
        except Exception as e:
            st.error(f"Error fetching analysis: {e}")

if __name__ == "__main__":
    ui = BrandAppUI(os.getenv("BACKEND_URL", BACKEND_URL))
    ui.run()