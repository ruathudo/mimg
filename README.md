# mimg
Multimodal interactive music generator


### Setup server development
- Install UV python dependencies management: https://docs.astral.sh/uv/
- Install python version using UV as set in `.python-version` file
- Install dependencies: `uv pip install -r requirements.txt`
- Run fastapi server: `uvicorn server.main:app --port 8000 --reload`
- To add new package: `uv add {package_name}`
- To export dependencies to requirements.txt format: `uv pip compile pyproject.toml -o requirements.txt`


### Setup client development
- Go to client folder and install dependencies: `npm ci`
- To run application: `npm run dev`