from pathlib import Path
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


class VizPanel:
    def __init__(self):
        self.app = FastAPI()
        self.app.mount('/', StaticFiles(directory=Path(__file__).parent.joinpath('web'), html=True), name='VizPanel')

    def run(self):
        print('Running VizPanel')
        uvicorn.run(self.app, host='0.0.0.0', port=8901, log_level='info', access_log=False)
