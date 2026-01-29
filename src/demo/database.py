import psycopg2
import os

from settings import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT


def get_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT
    )

def save_report(video_name, brand, seconds, total_duration, percentage):
    conn = get_connection()
    cur = conn.cursor()
    query = """
    INSERT INTO logo_detections (video_name, brand_name, appearance_seconds, video_duration_seconds, appearance_percentage)
    VALUES (%s, %s, %s, %s, %s)
    """
    cur.execute(query, (video_name, brand, seconds, total_duration, percentage))
    conn.commit()
    cur.close()
    conn.close()