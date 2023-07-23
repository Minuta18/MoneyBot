import uvicorn, os
from . import app, engine, Base
from .views import index

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)

    uvicorn.run('main:app', 
        port=os.environ.get('PORT', default=5000), 
        host=os.environ.get('HOST', default='0.0.0.0'), 
        log_level='info'
    )