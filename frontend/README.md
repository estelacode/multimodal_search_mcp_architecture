# Frontend

## 1. Create the virtual environment
```bash
py -3.12 -m venv .venv
```

## 2. Activate the virtual environment
```bash
.venv\Scripts\activate
where python # Confirm the virtual environment is active by checking the Python interpreter location
deactivate # Use this to deactivate the environment
```

## 3. Install dependencies
```bash
gradio==6.2.0
strands-agents==1.21.0
python-dotenv==1.2.1
faster-whisper==1.2.1
soundfile==0.13.1
```


## 4. Install the project in editable mode
This allows us to modify the source code and have changes applied immediately without reinstalling the package.
```bash
pip install -e .  # After creating the setup.py file, run:
```


# Devops

## 1. Create Docker Image
```bash 
docker build -t frontend .
```

## 2. List all created Docker Images
```bash
docker images
```

## 3. Create and run a container from the created image
```bash
docker run -d -p 3000:3000 --name frontend_container frontend
```

## 4. List all created Docker containers
```bash
docker ps
```

## 5. Access to the frontend_container 
```bash 
http://localhost:3000
```