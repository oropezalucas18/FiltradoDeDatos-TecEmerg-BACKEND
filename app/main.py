from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.adapters.input.fastapi.auth_controller import router as auth_router
from app.adapters.input.fastapi.ingest_controller import router as ingest_router
from app.adapters.input.fastapi.query_controller import router as query_router
from app.adapters.input.fastapi.analytics_controller import router as analytics_router
from app.adapters.input.fastapi.reports_controller import router as reports_router

# Adapters
from app.adapters.output.firebase_repository import FirebaseRepository
from app.adapters.output.supabase_repository import SupabaseRepository
from app.adapters.output.spark_file_parser import SparkFileParser
from app.adapters.output.rabbitmq_queue import RabbitMQQueue
from app.adapters.output.firebase_user_repository import FirebaseUserRepository

# Use Cases
from app.application.ingest_usecase import IngestUseCase
from app.application.query_usecase import QueryUseCase
from app.application.analytics_usecase import AnalyticsUseCase
from app.application.auth_usecase import AuthUseCase
from app.application.reports_usecase import ReportsUseCase

# Dependencies (DI)
from app.dependencies import auth_guard

# ====================================
#  APP INITIALIZATION
# ====================================

app = FastAPI(
    title="GAMC - Sistema de Monitoreo Subterráneo",
    description="Backend de monitoreo ambiental subterráneo para el GAMC",
    version="1.0.0"
)

# ====================================
#  CORS
# ====================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====================================
#  GLOBAL ADAPTER INSTANCES
# ====================================

firebase_repo = FirebaseRepository()
supabase_repo = SupabaseRepository()
user_repo = FirebaseUserRepository()
queue = RabbitMQQueue()
parser = SparkFileParser()

# ====================================
#  OVERRIDES (DEPENDENCY INJECTION)
# ====================================

app.dependency_overrides[IngestUseCase] = lambda: IngestUseCase(parser, queue)
app.dependency_overrides[QueryUseCase] = lambda: QueryUseCase(firebase_repo)
app.dependency_overrides[AnalyticsUseCase] = lambda: AnalyticsUseCase(firebase_repo)
app.dependency_overrides[AuthUseCase] = lambda: AuthUseCase(user_repo)
app.dependency_overrides[ReportsUseCase] = lambda: ReportsUseCase()

# ====================================
#  REGISTER ROUTERS
# ====================================

app.include_router(auth_router, tags=["Autenticación"])
app.include_router(ingest_router, tags=["Ingesta"])
app.include_router(query_router, tags=["Consultas"])
app.include_router(analytics_router, tags=["Analíticas"])
app.include_router(reports_router, tags=["Reportes"])

# ====================================
#  ROOT
# ====================================

@app.get("/")
def root():
    return {
        "status": "online",
        "message": "GAMC - Backend Operativo",
        "endpoints": "/docs"
    }
