import os
from flask import Flask, request, jsonify, send_file
import subprocess
import csv

app = Flask(__name__)

UPLOAD_FOLDER = './Docker/StudentWork'
VALIDATION_FOLDER = './Docker/StudentValidations'
OUTPUT_FOLDER = './output'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(VALIDATION_FOLDER):
    os.makedirs(VALIDATION_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

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

@app.route('/validate', methods=['GET'])
def start_validation():
    print("JAKOO")
    subprocess.run("./Docker/validate.sh", shell=True)
    return "Validation finished"

@app.route('/display', methods=['GET'])
def display_files():
    files_data = {}
    
    for filename in os.listdir(VALIDATION_FOLDER):
        filepath = os.path.join(VALIDATION_FOLDER, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                lines = file.readlines()
                if lines:
                    last_line = lines[-1].strip()
                else:
                    last_line = ''
            files_data[filename] = last_line
    
    # Save data to CSV
    csv_file_path = os.path.join(OUTPUT_FOLDER, 'files_data.csv')
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['FileName', 'LastLine'])
        for filename, last_line in files_data.items():
            csv_writer.writerow([filename, last_line])
    
    return send_file(csv_file_path, as_attachment=True, download_name='files_data.csv')

if __name__ == '__main__':
    app.run(host='localhost', port=4444)

