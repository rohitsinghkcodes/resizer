from flask import Flask, request, jsonify
import cv2
import numpy as np
import os

app = Flask(__name__)

def resize_image(image_path, scale_percent):
    src = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    new_width = int(src.shape[1] * scale_percent / 100)
    new_height = int(src.shape[0] * scale_percent / 100)
    dsize = (new_width, new_height)
    resized_img = cv2.resize(src, dsize)
    return resized_img

@app.route('/resize-image', methods=['POST'])
def resize_image_api():
    try:
        # Get the uploaded image file
        file = request.files['image']
        
        # Get the percentage scale from the request
        scale_percent = 100 - int(request.form['scale'])

        # Save the uploaded image to a temporary file
        temp_path = 'temp_image.jpg'
        file.save(temp_path)

        # Resize the image
        resized_image = resize_image(temp_path, scale_percent)

        # Save the resized image
        resized_path = 'resized_image.jpg'
        cv2.imwrite(resized_path, resized_image)

        # Return the resized image file path
        return jsonify({'resized_image_path': resized_path})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
