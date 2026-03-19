from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import saju, portfolio, rebalance, report, compatibility


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Saju Rebalancer API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(saju.router)
app.include_router(portfolio.router)
app.include_router(rebalance.router)
app.include_router(report.router)
app.include_router(compatibility.router)


@app.get("/health")
def health():
    return {"status": "ok"}
