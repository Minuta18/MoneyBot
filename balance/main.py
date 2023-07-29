import init
import uvicorn
import fastapi

import models

app = fastapi.FastAPI()

@app.on_event('startup')
async def init_():
    init.Base.metadata.create_all(bind=init.engine)

@app.get('/')
async def root():
    return {
        'error': False,
        'version': '0.4.1',
        'component_version': '0.1.0',
    }

if __name__ == '__main__':
    uvicorn.run('main:app', 
        port=int(init.os.environ.get('PORT', default=17012)), 
        host=init.os.environ.get('HOST', default='0.0.0.0'), 
        log_level='info'
    ) #