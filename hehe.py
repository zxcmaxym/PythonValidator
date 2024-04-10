import os
import docker
from flask import Flask, request

client = docker.from_env()
print(client.containers.list())

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
    
    # Build Docker image from Dockerfile
    image, build_logs = client.images.build(path='./Docker', dockerfile='Dockerfile')
    print(build_logs)
    
    # Run container from the built image
    container = client.containers.run(image.id, detach=True)
    print(container.logs())
    
    return 'File uploaded successfully'


if __name__ == '__main__':
    app.run(host='localhost', port=4444)

