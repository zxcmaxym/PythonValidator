import os
from flask import Flask, request
import subprocess


app = Flask(__name__)

UPLOAD_FOLDER = './Docker/StudentWork'
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
    
    return 'File uploaded successfully'
@app.route('/validate', methods =['GET'])
def start_validation():
    print("JAKOO")
    subprocess.run("./Docker/validate.sh", shell=True) 
    return "Validation finished"
if __name__ == '__main__':
    app.run(host='localhost', port=4444)

