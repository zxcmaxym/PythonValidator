import os
import shutil
from fastapi import FastAPI, File, UploadFile, Form, Query
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
async def upload_file(file: UploadFile = File(...), task: str = Form(...)):
    if not file:
        return {"error": "No file part"}

    if file.filename == '':
        return {"error": "No selected file"}

    task_folder = os.path.join(UPLOAD_FOLDER, task)
    if not os.path.exists(task_folder):
        os.makedirs(task_folder)

    filepath = os.path.join(task_folder, file.filename)
    with open(filepath, 'wb') as f:
        f.write(await file.read())

    return {"message": "File uploaded successfully to task folder"}

@app.get('/validate')
async def start_validation(task: str = Query(...), libraries: str = Query(...)):
    result = subprocess.run(f"./Docker/validate.sh {task} {libraries}", shell=True)
    if result.returncode == 0:
        return {"message": "Validation finished successfully"}
    else:
        return {"error": "Validation script failed", "returncode": result.returncode}

@app.get('/display')
async def display_files(task: str = Query(...)):
    task_folder = os.path.join(VALIDATION_FOLDER, task)
    if not os.path.exists(task_folder):
        return {"error": "Task folder does not exist"}

    files_data = {}

    for filename in os.listdir(task_folder):
        filepath = os.path.join(task_folder, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                lines = file.readlines()
                if lines:
                    last_line = lines[-1].strip()
                else:
                    last_line = ''
            files_data[filename] = last_line

    # Save data to CSV in the task-specific output folder
    task_output_folder = os.path.join(OUTPUT_FOLDER, task)
    if not os.path.exists(task_output_folder):
        os.makedirs(task_output_folder)
        
    csv_file_path = os.path.join(task_output_folder, 'files_data.csv')
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['FileName', 'LastLine'])
        for filename, last_line in files_data.items():
            csv_writer.writerow([filename, last_line])

    return FileResponse(csv_file_path, filename='files_data.csv')

@app.get('/remove')
async def remove_files():
    # Remove files and directories in UPLOAD_FOLDER
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    # Remove files and directories in VALIDATION_FOLDER
    for filename in os.listdir(VALIDATION_FOLDER):
        file_path = os.path.join(VALIDATION_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    # Remove files and directories in OUTPUT_FOLDER
    for filename in os.listdir(OUTPUT_FOLDER):
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    return {"message": "All files and directories in StudentWork, StudentValidations, and output directories have been removed"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=4444)

