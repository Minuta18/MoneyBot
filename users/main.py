import fastapi
import init

app = fastapi.FastAPI(
    openapi_url=init.OPENAPI_URL,
    docs_url=init.DOCS_URL,
)
router = fastapi.APIRouter(prefix=f'{init.PREFIX}/users')

@router.get('/health')
async def health_check():
    '''
    Health check can be used to check if service is available and
    can accept connections
    '''
    return {
        'error': False,
    }

app.include_router(router)
