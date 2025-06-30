from flask import Flask, request, jsonify, send_file, render_template  # add render_template
from ultralytics import YOLO
import os

app = Flask(__name__)

model = YOLO(r'best.pt')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    image = request.files['image']
    img_path = 'temp.jpg'
    image.save(img_path)

    results = model.predict(img_path, save=True)

    latest_result_dir = 'runs/detect/predict'
    result_img = os.path.join(latest_result_dir, os.listdir(latest_result_dir)[0])

    return send_file(result_img, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
