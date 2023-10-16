import fastapi
import app
import dotenv
import os
from app import views

dotenv.load_dotenv()

print(os.environ)

my_app = fastapi.FastAPI(
    openapi_url=app.OPENAPI_URL,
    docs_url=app.DOCS_URL,
)

async def init_models():
    async with app.engine.begin() as conn:
        await conn.run_sync(app.base.metadata.create_all)

@my_app.on_event('startup')
async def startup_event():
    await init_models()

@my_app.on_event('shutdown')
async def shutdown_event():
    await app.engine.dispose()

my_app.include_router(views.router)