from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB limit

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# In-memory storage for videos (Replace with a database in production)
videos = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'message': 'No video part in the request.'}), 400

    video = request.files['video']
    title = request.form.get('title')

    if video.filename == '':
        return jsonify({'message': 'No selected video.'}), 400

    if video and allowed_file(video.filename):
        filename = secure_filename(video.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        video.save(video_path)

        # Create a video entry
        new_video = {
            'id': len(videos) + 1,
            'title': title,
            'video_url': f"/uploads/{unique_filename}",
            'thumbnail_url': "/assets/thumbnail.jpg",  # Placeholder thumbnail
            'views': 0,  # Initialize views to 0
            'uploaded_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        videos.append(new_video)

        return jsonify({'message': 'Video uploaded successfully!', 'video': new_video}), 200
    else:
        return jsonify({'message': 'Invalid file type. Only video files are allowed.'}), 400

@app.route('/videos', methods=['GET'])
def get_videos():
    return jsonify(videos), 200

@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Serve assets (e.g., thumbnails)
@app.route('/assets/<path:filename>', methods=['GET'])
def assets(filename):
    return send_from_directory('../frontend/assets', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
