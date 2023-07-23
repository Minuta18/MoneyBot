from init import app

@app.get('/')
async def root():
    return {'test': True}