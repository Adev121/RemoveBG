from datetime import datetime
from app import db

class ImageProcess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(255), nullable=False)
    processed_filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_size = db.Column(db.Integer)  # Size in bytes
    status = db.Column(db.String(50))  # 'success' or 'failed'
    
    def __repr__(self):
        return f'<ImageProcess {self.original_filename}>'
