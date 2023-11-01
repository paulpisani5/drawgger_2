from flask import Flask, render_template, request, send_from_directory
from style_transfer_function import apply_styles_to_image, resize_image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
STYLES_FOLDER = 'styles/'
STYLED_FOLDER = 'styled/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STYLES_FOLDER'] = STYLES_FOLDER
app.config['STYLED_FOLDER'] = STYLED_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Resize the uploaded image
        resize_image(filepath, filepath)

        # Apply styles and get list of (style_image, transformed_image) tuples
        styled_images = apply_styles_to_image(filepath)

        return render_template('display.html', original_filename=filename, styled_images=styled_images)

    return render_template('index.html')

@app.route('/uploads/<filename>')
def send_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/styles/<filename>')
def send_style(filename):
    return send_from_directory(STYLES_FOLDER, filename)

@app.route('/styled/<filename>')
def send_styled(filename):
    return send_from_directory(STYLED_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
