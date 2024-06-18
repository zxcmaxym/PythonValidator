import os
import subprocess
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi_versioning import VersionedFastAPI, version

app = FastAPI()

def create_container(task):
    try:
        print(task)
        container = subprocess.run(f"./Docker/createcontainer.sh {task}", shell=True, capture_output=True, text=True)
        if container.returncode != 0:
            raise Exception(container.stderr)
        return container.stdout
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Container creation failed: {str(e)}")

def container_exists(task):
    result = subprocess.run(
        ["docker", "ps", "-a", "--filter", f"name={task}", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )
    return task in result.stdout.splitlines()

@app.post("/student/validate")
@version(1)
async def student_upload(name: str, task: str, file: UploadFile = File(...)):
    task_path = f"./Tasks/{task}"
    if not os.path.exists(task_path):
        raise HTTPException(status_code=400, detail="Task does not exist")
    file_location = f"{task_path}/{name}.py"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    if not container_exists(task):
        create_container(task)
    subprocess.run(f'./Scripts/validate.sh {task} {name}', shell=True)
    result = subprocess.run(f'cat ./Output/{task}/final/{name}.final', shell=True, capture_output=True, text=True)
    output = result.stdout
    return {"output": output}

@app.post("/teacher/task/create")
@version(1)
async def create_task(task: str, file: UploadFile = File(...)):
    task_path = f"./Tasks/{task}/teacher"
    os.makedirs(task_path, exist_ok=True)
    file_location = f"{task_path}/teacher.py"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    if not container_exists(task):
        create_container(task)
    return {"detail": "Task created and container started"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(VersionedFastAPI(app), host="0.0.0.0", port=4444)

