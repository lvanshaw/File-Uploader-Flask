from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
import jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
JSON_FILE = 'uploads.json'

# create upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# define helper functions
def save_upload(username, filename, filetype, description, priority):
    uploads = load_uploads()

    upload_data = {
        'username': username,
        'filename': filename,
        'filetype': filetype,
        'description': description,
        'priority': priority,
        'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'processed': False,
        'result': '',
        'speed': '',
        'detection': ''
    }

    if username in uploads:
        uploads[username].append(upload_data)
    else:
        uploads[username] = [upload_data]

    with open(JSON_FILE, 'w') as f:
        json.dump(uploads, f, indent=2)

def load_uploads():
    if not os.path.exists(JSON_FILE):
        return {}
    with open(JSON_FILE) as f:
        return json.load(f)

def set_upload_info(filename, info):
    uploads = load_uploads()
    for username in uploads:
        for file_info in uploads[username]:
            if file_info['filename'] == filename:
                file_info.update(info)
    with open(JSON_FILE, 'w') as f:
        json.dump(uploads, f, indent=2)

# define routes
@app.route('/')
def index():
    uploads = load_uploads()
    return render_template('index.html', uploads=uploads)

# handle file upload
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    description = request.form['description']
    filetype = request.form['type']
    priority = request.form['priority']
    username = "user1"  # get username from session or login info

    # save file to disk
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # save upload info to JSON file
    save_upload(username, filename, filetype, description, priority)

    return redirect(url_for('index'))

# # process speed
# @app.route("/tracker/process_speed", methods=["POST"])
# def process_speed():
#     filename = request.form["filename"]
#     # TODO: process speed using OpenCV or other libraries
#     # set processed and result in upload info
#     set_upload_info(filename, {"processed": True, "result": "speed data"})
#     return "Speed processing complete"

# # process detection
# @app.route("/tracker/process_detection", methods=["POST"])
# def process_detection():
#     filename = request.form["filename"]
#     # TODO: process object detection using TensorFlow or other libraries
#     # set processed and result in upload info
#     set_upload_info(filename, {"processed": True, "result": "detection data"})
#     return "Detection processing complete"

# define routes for processing speed and detection
@app.route('/tracker/process_speed', methods=['POST'])
def process_speed():
    filename = request.form['filename']
    # call function to process speed
    speed = calculate_speed(filename)
    # update the JSON file with the processed data
    update_json(filename, 'speed', speed)
    return jsonify({'status': 'success'})

@app.route('/tracker/process_detection', methods=['POST'])
def process_detection():
    filename = request.form['filename']
    # call function to process detection
    detection_result = detect_objects(filename)
    # update the JSON file with the processed data
    update_json(filename, 'detection', detection_result)
    return jsonify({'status': 'success'})

# helper function to update JSON file with processed data
def update_json(filename, result_type, result):
    uploads = load_uploads()

    for user in uploads:
        for upload in uploads[user]:
            if upload['filename'] == filename:
                upload[result_type] = result

    with open(JSON_FILE, 'w') as f:
        json.dump(uploads, f, indent=2)

# helper function to process speed
def calculate_speed(filename):
    # perform processing to calculate speed
    speed = '10 mph' # dummy result
    return speed

# helper function to process object detection
def detect_objects(filename):
    # perform object detection processing
    detection_result = 'Cars: 10, Bikes: 5, Pedestrians: 3' # dummy result
    return detection_result

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
