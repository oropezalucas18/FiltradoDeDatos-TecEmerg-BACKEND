from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache

# Routers
from app.adapters.input.fastapi.auth_controller import router as auth_router
from app.adapters.input.fastapi.ingest_controller import router as ingest_router
from app.adapters.input.fastapi.query_controller import router as query_router
from app.adapters.input.fastapi.analytics_controller import router as analytics_router
from app.adapters.input.fastapi.reports_controller import router as reports_router

# Adapters (Repos y servicios externos)
from app.adapters.output.firebase_repository import FirebaseRepository
from app.adapters.output.supabase_repository import SupabaseRepository
from app.adapters.output.spark_file_parser import SparkFileParser
from app.adapters.output.rabbitmq_queue import RabbitMQQueue
from app.adapters.output.firebase_user_repository import FirebaseUserRepository

# UseCases
from app.application.ingest_usecase import IngestUseCase
from app.application.query_usecase import QueryUseCase
from app.application.analytics_usecase import AnalyticsUseCase
from app.application.auth_usecase import AuthUseCase
from app.application.reports_usecase import ReportsUseCase



# =====================================================================
# 🔥 SINGLETONS PARA EVITAR PICKLING Y DUPLICACIÓN DE CLIENTES FIREBASE
# =====================================================================

@lru_cache()
def get_firebase_repo():
    return FirebaseRepository()

@lru_cache()
def get_supabase_repo():
    return SupabaseRepository()

@lru_cache()
def get_user_repo():
    return FirebaseUserRepository()

@lru_cache()
def get_spark_parser():
    return SparkFileParser()

@lru_cache()
def get_rabbitmq_queue():
    return RabbitMQQueue()



# =====================================================================
# FASTAPI APP
# =====================================================================

app = FastAPI(
    title="GAMC - Sistema de Monitoreo Subterráneo",
    description="Backend de monitoreo ambiental del GAMC",
    version="1.0.0"
)

# =====================================================================
# CORS
# =====================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================================
# DEPENDENCY OVERRIDES (SEGUROS)
# =====================================================================

# Ingesta
app.dependency_overrides[IngestUseCase] = lambda: IngestUseCase(
    get_spark_parser(),
    get_rabbitmq_queue()
)

# Consultas simples
app.dependency_overrides[QueryUseCase] = lambda: QueryUseCase(
    get_firebase_repo()
)

# Analíticas
app.dependency_overrides[AnalyticsUseCase] = lambda: AnalyticsUseCase(
    get_firebase_repo()
)

# Autenticación
app.dependency_overrides[AuthUseCase] = lambda: AuthUseCase(
    get_user_repo()
)

# Reportes
app.dependency_overrides[ReportsUseCase] = lambda: ReportsUseCase()



# =====================================================================
# REGISTRAR ROUTERS
# =====================================================================

app.include_router(auth_router, tags=["Auth"])
app.include_router(ingest_router, tags=["Ingesta"])
app.include_router(query_router, tags=["Consultas"])
app.include_router(analytics_router, tags=["Analíticas"])
app.include_router(reports_router, tags=["Reportes"])



# =====================================================================
# ROOT
# =====================================================================

@app.get("/")
def root():
    return {
        "status": "online",
        "message": "GAMC - Backend operativo",
        "docs": "/docs"
    }
