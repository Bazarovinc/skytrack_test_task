import uvicorn

from app.fast_api_app import app
from source.api.views import router

app.include_router(router, prefix='/api')


@app.get('/')
async def root():
    return {'message': 'Hello world!'}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
