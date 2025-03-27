from flask import Flask, request, jsonify  # Make sure 'request' is imported
from leaf_analysis import analyze_leaf
import os
app = Flask(__name__, static_folder='static')
from flask import Flask
from whitenoise import WhiteNoise
import os
from leaf_analysis import analyze_leaf

app = Flask(__name__, static_folder='static')
app.wsgi_app = WhiteNoise(app.wsgi_app, root=app.static_folder)
app.config['WHITENOISE_AUTOREFRESH'] = True
app.config['WHITENOISE_USE_FINDERS'] = True

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(filepath)

    try:
        severity_data = analyze_leaf(filepath)
        return jsonify({
            'severity': f"{severity_data['percentage']:.2f}% ({severity_data['level']})",
            'image_url': f'/uploads/{file.filename}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)