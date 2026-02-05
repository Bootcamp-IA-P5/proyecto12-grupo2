from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Video(Base):
    """Stores metadata for each processed video."""
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    video_uuid = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    processed_at = Column(DateTime, default=func.now())
    
    # Relationship to allow: video_instance.detections
    detections = relationship("Detection", back_populates="video")

class Detection(Base):
    """Stores detailed brand exposure data per frame."""
    __tablename__ = 'detections'
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey('videos.id'))
    brand_name = Column(String, nullable=False) # e.g., 'Adidas', 'CocaCola'
    confidence = Column(Float, nullable=False)
    timestamp_sec = Column(Float, nullable=False) # When it occurred
    geometry_box = Column(JSON, nullable=False) # Where it occurred (xmin, ymin, xmax, ymax)
    exposure_percentage = Column(Float, nullable=False) # How much space it occupied
    crop_path = Column(String) # Path to the bounding box image
    
    video = relationship("Video", back_populates="detections")