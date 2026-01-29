import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import yt_dlp
from database import save_report
from settings import YOLO_MODEL_ORG
import time

# --- Page Setup ---
st.set_page_config(page_title="BrandTracker AI", layout="wide", page_icon="🛡️")

# Clean, premium CSS for Light Theme
st.markdown("""
<style>
    .report-card {
        padding: 20px;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
    }
    .brand-tag {
        display: inline-block;
        background-color: #dbeafe;
        color: #1e40af;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: bold;
        margin: 5px;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return YOLO(YOLO_MODEL_ORG)

# --- Video Analysis Logic ---
def analyze_video_stream(url):
    st.info("🔍 Connecting to video stream...")
    
    ydl_opts = {
        'format': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=False)
            stream_url = meta.get('url')
            title = meta.get('title', 'Video Stream')
            duration = meta.get('duration', 0)
            fps = meta.get('fps', 30) or 30
    except Exception as e:
        st.error(f"Stream Error: {e}")
        return None

    # Try opening the stream with a timeout or different backends if needed
    cap = cv2.VideoCapture(stream_url)
    
    if not cap.isOpened():
        # Fallback: sometimes HLS URLs need special handling or are too long
        st.warning("Primary stream failed. Attempting alternative format...")
        ydl_opts['format'] = 'best[height<=480]' # More permissive
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                meta = ydl.extract_info(url, download=False)
                stream_url = meta.get('url')
                cap = cv2.VideoCapture(stream_url)
        except:
            pass

    if not cap.isOpened():
        st.error("Could not open stream. This video format might not be supported in this environment.")
        return None

    # UI Elements: Centered 50% width container
    _, col_vid, _ = st.columns([1, 2, 1])
    with col_vid:
        video_placeholder = st.empty()
    
    status_msg = st.empty()
    progress_bar = st.progress(0)
    
    detected_seconds = 0
    brand_counts = {} # To track specific brands
    frame_count = 0
    model = load_model()
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            frame_count += 1
            
            # Process 1 frame per second
            if frame_count % int(fps) == 0:
                current_sec = int(frame_count / fps)
                
                # Inference
                results = model.predict(frame, conf=0.25, device='cpu', verbose=False)
                
                # Visuals
                annotated = results[0].plot()
                rgb_frame = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                
                # Show in centered placeholder (50% width)
                video_placeholder.image(rgb_frame, caption=f"AI Audit: {title}", width='stretch')
                
                # Tracking
                if len(results[0].boxes) > 0:
                    detected_seconds += 1
                    
                    # Track specific brands in this frame
                    brands_this_frame = set()
                    for box in results[0].boxes:
                        cls_id = int(box.cls[0])
                        brand_name = model.names[cls_id]
                        brands_this_frame.add(brand_name)
                    
                    for br in brands_this_frame:
                        brand_counts[br] = brand_counts.get(br, 0) + 1
                
                # Update Status
                found_str = ", ".join(brand_counts.keys()) if brand_counts else "None"
                status_msg.markdown(f"**Pos:** {current_sec}s | **Detected:** {detected_seconds}s | **Brands:** `{found_str}`")
                
                if duration > 0:
                    progress_bar.progress(min(current_sec / duration, 1.0))

    finally:
        cap.release()
        
    return {
        "title": title,
        "exposure_s": detected_seconds,
        "total_s": duration,
        "brands": brand_counts
    }

# --- Main App ---
def main():
    st.title("🛡️ BrandTracker AI")
    st.markdown("Automated recognition and branding exposure analytics.")
    
    if 'results' not in st.session_state:
        st.session_state.results = None

    with st.sidebar:
        st.header("Inspection Module")
        model = load_model()
        st.write("**Detectable Brands:**")
        for n in model.names.values():
            st.code(n)

    url = st.text_input("YouTube URL:", placeholder="Paste link here...")
    
    if st.button("🚀 Start Audit", type="primary"):
        if url:
            st.session_state.results = analyze_video_stream(url)
        else:
            st.warning("Please enter a URL.")

    # Results Section
    if st.session_state.results:
        res = st.session_state.results
        title = res['title']
        exposure = res['exposure_s']
        total = res['total_s']
        brands = res['brands']
        percent = (exposure / total * 100) if total > 0 else 0

        st.divider()
        st.header(f"📊 Audit Report: {title}")
        
        # Metrics Row
        m1, m2, m3 = st.columns(3)
        m1.metric("Brand Exposure", f"{exposure}s")
        m2.metric("Total Video Time", f"{int(total)}s")
        m3.metric("Visibility Share", f"{percent:.1f}%")

        # Brand Breakdown
        st.subheader("Brand Recognition Breakdown")
        if brands:
            cols = st.columns(len(brands) if len(brands) < 4 else 4)
            for i, (name, sec) in enumerate(brands.items()):
                with cols[i % len(cols)]:
                    st.markdown(f"""
                    <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; padding: 10px; border-radius: 8px; text-align: center;">
                        <div style="color: #1e40af; font-weight: bold;">{name.upper()}</div>
                        <div style="font-size: 20px;">{sec}s</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.write("No specific brands identified.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Finalize & Save to DB"):
            try:
                # Save primary brand or a summary to the DB
                main_brand = list(brands.keys())[0] if brands else "None"
                save_report(title, main_brand, exposure, total, percent)
                st.success(f"Report for '{main_brand}' saved successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Database error: {e}")

if __name__ == "__main__":
    main()