from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.routes import users, assets, auth
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Middlware
origins_env = os.getenv("BACKEND_CORS_ORIGINS", "")
origins = [o.strip() for o in origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # lista explícita de orígenes permitidos
    allow_credentials=True,       # si usas cookies/autenticación basada en sesión
    allow_methods=["*"],          # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],          # Authorization, Content-Type, etc.
)

# Incluir routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(assets.router, prefix="/assets", tags=["Assets"])

@app.get("/")
def root():
    print("Entra main.py")
    return {"message": "API funcionando 🚀"}
