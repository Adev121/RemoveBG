import os
import requests
from flask import Flask, request, send_file, jsonify, render_template
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import logging
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import models after db initialization
from models import ImageProcess

# Configure upload folder
UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Create database record
        image_process = ImageProcess(
            original_filename=filename,
            processed_filename='processed_' + filename,
            file_size=os.path.getsize(filepath),
            status='processing'
        )
        db.session.add(image_process)
        db.session.commit()

        # Call remove.bg API
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(filepath, 'rb')},
            headers={'X-Api-Key': os.getenv('REMOVE_BG_API_KEY')},
        )

        if response.status_code != 200:
            image_process.status = 'failed'
            db.session.commit()
            return jsonify({'error': 'Failed to process image'}), 500

        # Save processed image
        output_path = os.path.join(UPLOAD_FOLDER, 'processed_' + filename)
        with open(output_path, 'wb') as out:
            out.write(response.content)

        # Update database record
        image_process.status = 'success'
        db.session.commit()

        # Clean up original file
        os.remove(filepath)

        # Return processed image
        return send_file(output_path, mimetype='image/png', as_attachment=False)

    except Exception as e:
        app.logger.error(f"Error processing image: {str(e)}")
        if 'image_process' in locals():
            image_process.status = 'failed'
            db.session.commit()
        return jsonify({'error': 'Failed to process image'}), 500

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)