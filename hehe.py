import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import subprocess
import csv

app = FastAPI()

UPLOAD_FOLDER = './Docker/StudentWork'
VALIDATION_FOLDER = './Docker/StudentValidations'
OUTPUT_FOLDER = './output'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(VALIDATION_FOLDER):
    os.makedirs(VALIDATION_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@app.post('/hehe')
async def upload_file(file: UploadFile = File(...)):
    if not file:
        return {"error": "No file part"}

    if file.filename == '':
        return {"error": "No selected file"}

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filepath, 'wb') as f:
        f.write(await file.read())
    
    return {"message": "File uploaded successfully"}

@app.get('/validate')
async def start_validation():
    subprocess.run("./Docker/validate.sh", shell=True)
    return {"message": "Validation finished"}

@app.get('/display')
async def display_files():
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

    return FileResponse(csv_file_path, filename='files_data.csv')

@app.get('/remove')
async def remove_files():
    # Remove files in UPLOAD_FOLDER
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Remove files in VALIDATION_FOLDER
    for filename in os.listdir(VALIDATION_FOLDER):
        file_path = os.path.join(VALIDATION_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Remove files in OUTPUT_FOLDER
    for filename in os.listdir(OUTPUT_FOLDER):
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    return {"message": "All files in StudentWork, StudentValidations, and output directories have been removed"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=4444)

