# Brand Exposure Analyzer - Demo Application

This directory contains the complete Brand Exposure Analyzer application, structured with a modern **backend/frontend separation** using FastAPI and Streamlit.

## 📋 Architecture Overview

The application follows a microservices-inspired architecture with clear separation of concerns:

```
src/demo/
├── backend/          # FastAPI REST API service
├── frontend/         # Streamlit web UI service
├── common/           # Shared utilities (logging, helpers)
├── settings.py       # Configuration management
└── README.md         # This file
```

### Application Flow

```
User Browser (Port 8501)
         ↓
    Streamlit Frontend
         ↓
    HTTP/REST (Port 8000)
         ↓
    FastAPI Backend
         ↓
    PostgreSQL (Externalized)
```

---

## 🚀 Services

### Backend (`backend/`)

**FastAPI REST API** providing video analysis endpoints with streaming progress support.

**Key Files:**
- `main.py` - REST API endpoints with NDJSON streaming
- `model_worker.py` - YOLO brand detection engine with frame-by-frame analysis
- `database_manager.py` - SQLAlchemy ORM for PostgreSQL operations
- `models.py` - SQLAlchemy table definitions (Video, Detection)

**Endpoints:**
- `GET /model-info/` - Returns detectable brands
- `POST /analyze/` - Upload video file for analysis (streaming)
- `POST /analyze-stream/` - Analyze YouTube URL (streaming)
- `GET /results/{video_id}` - Retrieve analysis results
- `DELETE /results/{video_id}` - Delete analysis record
- `POST /save-analysis/` - Verify analysis is persisted

**Technology Stack:**
- FastAPI + Uvicorn
- YOLO (Ultralytics) for brand detection
- SQLAlchemy ORM
- OpenCV for video processing
- yt-dlp for YouTube streaming
- PostgreSQL (external)

**Port:** `8000`

---

### Frontend (`frontend/`)

**Streamlit Web UI** providing user-friendly interface for video analysis submission and results visualization.

**Key Files:**
- `app.py` - Main Streamlit application with UI components

**Features:**
- Two-tab interface (YouTube URL input / File upload)
- Real-time progress streaming during analysis
- Results visualization with brand metrics
- Action buttons (Copy ID, View in Database, Start New)
- Session state management for results caching

**Technology Stack:**
- Streamlit for rapid UI development
- requests for HTTP communication
- JSON/NDJSON parsing for streaming responses

**Port:** `8501`

**Note:** Frontend requires backend to be running; it communicates via `BACKEND_URL` environment variable.

---

### Common Utilities (`common/`)

Shared modules used by both backend and frontend services.

**Key Files:**
- `logger.py` - Structured logging with colorlog
- `log_setup.py` - Log configuration initialization

**Features:**
- Consistent logging across services
- Color-coded log levels (DEBUG, INFO, WARNING, ERROR)
- Centralized log management

---

## ⚙️ Configuration (`settings.py`)

Centralized configuration management using environment variables with fallback defaults.

**Key Settings:**
```python
# Database
POSTGRES_DB          # PostgreSQL database name
POSTGRES_USER        # PostgreSQL username
POSTGRES_PASSWORD    # PostgreSQL password
POSTGRES_HOST        # PostgreSQL hostname (externalized)
POSTGRES_PORT        # PostgreSQL port

# Backend
BACKEND_URL          # Backend API base URL (http://localhost:8000)

# YOLO Model
YOLO_MODEL_ORG       # Path to YOLO model weights

# Logging
LOG_FILE_NAME        # Log filename
LOG_LEVEL            # Log verbosity (DEBUG, INFO, etc.)
LOG_BASE_DIR         # Log directory
```

All settings are loaded from `.env` file via `python-dotenv`.

---

## 🐳 Docker Deployment

### Dockerfile.demo

Multi-stage Docker build supporting both backend and frontend services:

```bash
# Build backend service
docker build -t brand-analyzer:backend --target backend -f Dockerfile.demo .

# Build frontend service
docker build -t brand-analyzer:frontend --target frontend -f Dockerfile.demo .
```

### docker-compose-demo.yml

Orchestrates both services with proper networking:

```bash
# Start both services
docker-compose -f docker-compose-demo.yml up -d

# View logs
docker-compose -f docker-compose-demo.yml logs -f

# Stop services
docker-compose -f docker-compose-demo.yml down
```

**Service Configuration:**
- Backend: `localhost:8000` (http://backend:8000 internal network)
- Frontend: `localhost:8501` (http://backend:8000 via internal network)
- Shared network: `brand_analyzer_network` (bridge driver)
- Environment: Loaded from `.env` file
- Volumes: Read-only models mount, logs directory

---

## 📦 Installation & Setup

### Local Development

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your PostgreSQL credentials
   ```

3. **Run Backend:**
   ```bash
   cd /workspaces/proyecto12-grupo2
   uvicorn src.demo.backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Run Frontend (in another terminal):**
   ```bash
   cd /workspaces/proyecto12-grupo2
   streamlit run src/demo/frontend/app.py
   ```

5. **Access UI:**
   - Frontend: http://localhost:8501
   - Backend API docs: http://localhost:8000/docs

### Docker Deployment

```bash
# Build images
docker-compose -f docker-compose-demo.yml build

# Start services
docker-compose -f docker-compose-demo.yml up -d

# Access UI
# Frontend: http://localhost:8501
# Backend API docs: http://localhost:8000/docs
```

---

## 🔄 Data Flow

### Video Analysis Workflow

1. **User Submission** (Frontend)
   - User uploads video file or provides YouTube URL
   - Frontend sends request to backend

2. **Analysis Processing** (Backend)
   - Backend receives request and generates unique `video_id` (UUID)
   - YOLO model processes video frame-by-frame (1 frame/sec)
   - Detections streamed as NDJSON objects with progress

3. **Real-time Updates** (Frontend)
   - Frontend receives NDJSON stream
   - Parses each line (progress objects)
   - Updates progress bar in real-time

4. **Persistence** (Backend)
   - Final results saved to PostgreSQL
   - Video and Detection records created
   - video_uuid used for API lookups

5. **Results Display** (Frontend)
   - Displays final metrics and brand breakdown
   - Allows user to copy video_id or view in database
   - Enables new analysis or exit

---

## 🗄️ Database Schema

### Video Table
```sql
CREATE TABLE video (
    id SERIAL PRIMARY KEY,
    video_uuid VARCHAR UNIQUE NOT NULL,  -- UUID for API responses
    name VARCHAR NOT NULL,                 -- Video title/filename
    processed_at TIMESTAMP DEFAULT NOW()   -- Analysis completion time
);
```

### Detection Table
```sql
CREATE TABLE detection (
    id SERIAL PRIMARY KEY,
    video_id INTEGER FOREIGN KEY,          -- References Video.id
    brand_name VARCHAR NOT NULL,           -- Detected brand name
    confidence FLOAT NOT NULL,             -- Detection score (0-1)
    timestamp_sec INTEGER NOT NULL,        -- Position in video (seconds)
    geometry_box JSON,                     -- Bounding box coordinates
    exposure_percentage FLOAT              -- Brand exposure percentage
);
```

---

## 🔐 Security Considerations

- Database credentials stored in `.env` (never committed)
- YOLO inference runs on CPU (configure GPU in settings if available)
- File uploads cleaned up after analysis
- All inputs validated by Streamlit and FastAPI

---

## 📊 Logging

All services use structured logging with color-coded output:

```
[DEBUG] - Detailed debugging information
[INFO]  - General information
[WARNING] - Warning messages
[ERROR] - Error messages
```

Logs stored in `log/` directory (mounted in Docker containers).

---

## 🛠️ Development Notes

### Code Structure

- **Generator-based streaming** in `model_worker.py` for real-time progress
- **NDJSON format** for efficient streaming (newline-delimited JSON)
- **Session state management** in Streamlit for results caching
- **UUID-based tracking** for reliable video identification across API/database

### Key Patterns

1. **Streaming Analysis:**
   - Backend yields frame data during processing
   - Frontend consumes NDJSON objects line-by-line
   - Real-time UI updates without blocking

2. **Database Flexibility:**
   - UUID primary method for lookups
   - Fallback to numeric ID or video name
   - Transaction safety with rollback on errors

3. **Error Handling:**
   - Graceful degradation in frontend
   - Detailed error logging in backend
   - Atomic database operations

---

## 📝 Documentation

Each Python file includes comprehensive docstrings:

- **Module level:** Architecture and key concepts
- **Class level:** Purpose, attributes, responsibilities
- **Function level:** Parameters, returns, raises, examples
- **Inline comments:** Complex logic and business decisions

---

## 🚧 Future Enhancements

- [ ] GPU acceleration for YOLO inference
- [ ] Batch video processing queue
- [ ] Advanced filtering and search in results
- [ ] Export reports (PDF, CSV)
- [ ] User authentication and multi-tenancy
- [ ] Webhook notifications on analysis completion
- [ ] API rate limiting and monitoring

---

## 📞 Support

For issues or questions:
1. Check logs in `log/` directory
2. Review API documentation at `http://localhost:8000/docs`
3. Verify `.env` configuration matches PostgreSQL settings
4. Ensure YOLO model weights exist at path specified in settings

---

## 📄 License

See root repository LICENSE file.
