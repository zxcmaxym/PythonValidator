import os
from flask import Flask, request

app = Flask(__name__)

UPLOAD_FOLDER = './testenv/StudentWork'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/hehe', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    # Run container.sh
    os.system('./container.sh')
    
    return 'File uploaded successfully'


if __name__ == '__main__':
    app.run(host='localhost', port=4444)

