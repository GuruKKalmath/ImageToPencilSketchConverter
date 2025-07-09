# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/sketches'

# Ensure the sketches directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def convert_to_sketch(image_path):
    # Read the image
    img = cv2.imread(image_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv_gray = 255 - gray_img
    blurred = cv2.GaussianBlur(inv_gray, (21, 21), 0)
    inv_blur = 255 - blurred
    sketch = cv2.divide(gray_img, inv_blur, scale=256.0)
    return sketch

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Convert to pencil sketch
            sketch = convert_to_sketch(filepath)
            sketch_filename = f"sketch_{filename}"
            sketch_filepath = os.path.join(app.config['UPLOAD_FOLDER'], sketch_filename)
            cv2.imwrite(sketch_filepath, sketch)

            return render_template('index.html', sketch_url=url_for('static', filename=f'sketches/{sketch_filename}'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
