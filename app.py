from flask import Flask, render_template, request, jsonify, send_file
from paddleocr import PaddleOCR
from gtts import gTTS
import os

app = Flask(__name__)

ocr = PaddleOCR(use_gpu=True)

# Initialize extracted_text as an empty list
extracted_text = []

def extract_text(image_path):
    try:
        global extracted_text  # Use the global extracted_text variable

        # Perform OCR on the image
        results = ocr.ocr(image_path)

        # Extract and process text from the OCR results
        extracted_text = []
        for result in results:
            for line in result:
                extracted_text.append(line[1][0])

        return extracted_text

    except Exception as e:
        error_message = str(e)
        return []

@app.route('/')
def index():
    return render_template('index.html', ocr_results=extracted_text)

@app.route('/process', methods=['POST'])
def process_prescription():
    try:
        global extracted_text  # Use the global extracted_text variable

        if 'image' not in request.files:
            return jsonify({'error': 'No image part'}), 400

        image = request.files['image']
        if image.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the image to a temporary file
        image_path = 'amoxicillin.jpeg'
        image.save(image_path)

        # Extract text from the image
        extracted_text = extract_text(image_path)

        # Render the template with the extracted text
        return render_template('index.html', ocr_results=extracted_text)

    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500

@app.route('/get_audio')
def get_audio():
    try:
        text_to_speak = ' '.join(extracted_text)
        audio_path = 'output.mp3'
        tts = gTTS(text_to_speak)
        tts.save(audio_path)
        return send_file(audio_path, as_attachment=True)

    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500
    
@app.route('/test_audio')
def test_audio():
    try:
        image_path = 'amoxicillin.jpeg'
        extracted_text = extract_text(image_path)
        
        text_to_speak = ' '.join(extracted_text)
        audio_path = 'output.mp3'
        tts = gTTS(text_to_speak)
        tts.save(audio_path)
        return send_file(audio_path, as_attachment=True)

    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)
 