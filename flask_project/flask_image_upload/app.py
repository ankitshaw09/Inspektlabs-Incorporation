from flask import Flask, render_template, request, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os


app = Flask(__name__)
limiter = Limiter(    key_func=get_remote_address,
    default_limits=["5 per minute"]
)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = '1234' 

jwt = JWTManager(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('result', image_name=file.filename))
    else:
        return "No file uploaded"

@app.route('/result/<image_name>')
def result(image_name):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
    return render_template('result.html', image_name=image_name, image_path=image_path)

@app.route('/api/upload', methods=['POST'])
@jwt_required()
def api_upload_file():
    current_user = get_jwt_identity()
    if current_user != 'your_api_key':
        return "Unauthorized", 401

    file = request.files['image']
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return "File uploaded successfully", 200
    else:
        return "No file uploaded", 400

@limiter.request_filter
def ip_whitelist():
    # Here you can define a condition to whitelist certain IP addresses
    return True


if __name__ == '__main__':
    app.run(debug=True)

