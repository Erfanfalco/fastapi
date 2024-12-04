from App.routers.Database.dependencies import app
from App.routers import users

app.include_router(users.router)
