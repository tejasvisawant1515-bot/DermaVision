import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dermavision-ai-super-secret-key-2026')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

    # Database Configuration
    # Defaults to MySQL; auto-falls back to SQLite if MySQL is unavailable
    DB_TYPE = os.environ.get('DB_TYPE', 'mysql')  # 'mysql' or 'sqlite'
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'dermavision_db')

    # SQLite fallback path
    SQLITE_PATH = os.path.join(BASE_DIR, 'dermavision.db')
