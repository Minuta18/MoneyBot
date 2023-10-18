import fastapi
import app
from app import views

my_app = fastapi.FastAPI(
    openapi_url=app.OPENAPI_URL,
    docs_url=app.DOCS_URL,
)

@my_app.on_event('startup')
async def startup_event():
    await views.destroy_models()

    await views.init_models()

@my_app.on_event('shutdown')
async def shutdown_event():
    await app.engine.dispose()

my_app.include_router(views.router)
