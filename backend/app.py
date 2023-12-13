from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from querysearch import thesearch
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/search": {"origins": "http://localhost:3000"}})
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,POST,GET'
    return response


# Mock data (replace this with your actual search logic)


# Define the fixed upload directory
UPLOAD_DIRECTORY = r'E:\salmandsa\DSA_Project\forward_index_directory'

# Ensure the fixed upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query = data.get('query', '')
        print(query)
        # Mock search logic (replace with your actual search function)
        results = thesearch(query)
        print(results)
        return jsonify({'results': results})

    except Exception as e:
        return jsonify({'error': f'Error during search: {str(e)}'})

# ... (rest of the code remains the same)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Get the uploaded file
        uploaded_file = request.files['file']

        # Save the file to the fixed directory
        if uploaded_file:
            file_path = os.path.join(UPLOAD_DIRECTORY, uploaded_file.filename)
            uploaded_file.save(file_path)
            return jsonify({'message': 'File uploaded successfully!', 'file_path': file_path})
        else:
            return jsonify({'error': 'No file provided!'})

    except Exception as e:
        return jsonify({'error': f'Error uploading file: {str(e)}'})


if __name__ == '__main__':
    app.run(port=5000)
