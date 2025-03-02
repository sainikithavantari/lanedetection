from flask import Flask, request, jsonify
import cv2
import numpy as np
import os

app = Flask(__name__)

# Function to process image
def process_image(file):
    # Save the uploaded file
    file_path = "uploaded_image.jpg"
    file.save(file_path)

    # Process the image
    image = cv2.imread(file_path)
    output_image = process_image(image)  # Use your lane detection function here

    # Save the output image
    output_path = "output_image.jpg"
    cv2.imwrite(output_path, output_image)

    return output_path

# Function to process video
def process_video(file):
    # Save the uploaded file
    file_path = "uploaded_video.mp4"
    file.save(file_path)

    # Process the video
    output_video_path = "output_video.mp4"
    process_video(file_path, output_video_path)  # Use your lane detection function here

    return output_video_path

# API endpoint for image processing
@app.route('/process-image', methods=['POST'])
def handle_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    output_path = process_image(file)

    return jsonify({"output_url": output_path})

# API endpoint for video processing
@app.route('/process-video', methods=['POST'])
def handle_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    output_path = process_video(file)

    return jsonify({"output_url": output_path})

if __name__ == "__main__":
    app.run(debug=True)