import os
import requests
from flask import Flask, request, send_file, jsonify, render_template
from werkzeug.utils import secure_filename
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

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

        # Call remove.bg API
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(filepath, 'rb')},
            headers={'X-Api-Key': os.getenv('REMOVE_BG_API_KEY')},
        )

        if response.status_code != 200:
            return jsonify({'error': 'Failed to process image'}), 500

        # Save processed image
        output_path = os.path.join(UPLOAD_FOLDER, 'processed_' + filename)
        with open(output_path, 'wb') as out:
            out.write(response.content)

        # Clean up original file
        os.remove(filepath)

        # Return processed image
        return send_file(output_path, mimetype='image/png', as_attachment=False)

    except Exception as e:
        app.logger.error(f"Error processing image: {str(e)}")
        return jsonify({'error': 'Failed to process image'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)