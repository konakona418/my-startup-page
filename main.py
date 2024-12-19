from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles


async def init():
    import service
    if not service.data_fetched:
        await service.init_all_tables()

async def close():
    import service
    await service.close_service()

app = FastAPI(on_startup=[init], on_shutdown=[close])
app.mount("/assets", StaticFiles(directory="static/dist/assets"), name="assets")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return FileResponse("static/dist/index.html")


@app.get("/api/notifications/count")
@app.post("/api/notifications/count")
async def get_notifications_count():
    import service
    if not service.data_fetched:
        await service.init_all_tables()
    return {"count": await service.get_notification_count()}


@app.get("/api/notifications")
@app.post("/api/notifications")
async def get_notifications():
    import service
    if not service.data_fetched:
        await service.init_all_tables()
    notifications = await service.get_notifications()
    return {"notifications": notifications}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)