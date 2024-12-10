# mimg
Multimodal interactive music generator


## Setup development
- Install UV python dependencies management: https://docs.astral.sh/uv/
- Install python version using UV as set in .python-version file
- Install dependencies: `uv pip install -r requirements.txt`
- Export dependencies to requirements.txt format: `uv pip compile pyproject.toml -o requirements.txt`

### Setup server development
- Install python dependencies: `uv install`
- Activate python env: `pipenv shell`
- Run fastapi server: `uvicorn server.main:app --port 8000 --reload`
- 


### Setup client development
- Go to client folder and install dependencies: `npm ci`
- To run application: `npm run dev`