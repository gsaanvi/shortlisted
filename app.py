# Connects frontend HTML to Python analysis


from flask import Flask, request, jsonify, send_from_directory
from utils import extract_text_from_pdf
from analyzer import run_full_analysis
import os

app = Flask(__name__, static_folder='.')


# Serve the frontend
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


# Analysis endpoint
@app.route('/analyze', methods=['POST'])
def analyze():
    # Validate inputs
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume uploaded'}), 400

    resume_file = request.files['resume']
    jd_text = request.form.get('jd_text', '').strip()

    if not jd_text:
        return jsonify({'error': 'No job description provided'}), 400

    if resume_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not resume_file.filename.endswith('.pdf'):
        return jsonify({'error': 'Please upload a PDF file'}), 400

    try:
        # Extract text from PDF
        resume_text = extract_text_from_pdf(resume_file)

        if not resume_text.strip():
            return jsonify({
                'error': 'Could not extract text from your PDF. Make sure it is not a scanned image.'
            }), 400

        # Run analysis
        results = run_full_analysis(resume_text, jd_text)
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)