import fastapi
import init

app = fastapi.FastAPI(
    openapi_url=f'{init.PREFIX}/users/openapi.json', 
    docs_url=f'{init.PREFIX}/users/docs'
)
router = fastapi.APIRouter(prefix=f'{init.PREFIX}/users')

@router.get('/health')
async def health_check():
    return {
        'error': False,
    }

app.include_router(router)