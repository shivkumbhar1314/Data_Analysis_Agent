from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tempfile
import json
from pathlib import Path
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_analysis_agent import DataAnalysisAgent

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'csv', 'parquet', 'xls', 'xlsx'}
MAX_FILE_SIZE = 50 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided', 'success': False}), 400

        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected', 'success': False}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format. Allowed: CSV, Parquet, Excel', 'success': False}), 400

        if file.content_length > MAX_FILE_SIZE:
            return jsonify({'error': f'File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB', 'success': False}), 400

        dataset_name = request.form.get('datasetName', 'analysis')
        target_column = request.form.get('targetColumn', None) or None
        agents_str = request.form.get('agents', '[]')
        
        try:
            agents = json.loads(agents_str)
        except:
            agents = None

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, secure_filename(file.filename))
            file.save(filepath)

            agent = DataAnalysisAgent(output_dir=tmpdir)
            
            results = agent.analyze(
                data_source=filepath,
                dataset_name=dataset_name,
                target_column=target_column,
                run_agents=agents,
                generate_reports=True
            )

            if results.get('success'):
                html_report_path = None
                json_report_path = None
                
                for file_path in Path(tmpdir).glob('report_*.html'):
                    html_report_path = str(file_path)
                    break
                
                for file_path in Path(tmpdir).glob('report_*.json'):
                    json_report_path = str(file_path)
                    break

                clean_results = {
                    'success': True,
                    'timestamp': results.get('timestamp'),
                    'dataset_profile': results.get('dataset_profile'),
                    'agent_results': results.get('agent_results'),
                    'summary': results.get('summary'),
                    'html_report': html_report_path,
                    'json_report': json_report_path
                }

                return jsonify(clean_results), 200
            else:
                return jsonify({
                    'success': False,
                    'error': results.get('error', 'Analysis failed')
                }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/', methods=['GET'])
def index():
    return '''
    <h1>Data Analysis Agent API</h1>
    <p>Backend is running successfully!</p>
    <p><a href="/api/health">Health Check</a></p>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
