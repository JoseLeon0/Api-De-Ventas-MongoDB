# Conecta a MongoDB Atlas leyendo las variables de entorno
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME")

# Cliente de MongoDB
client = AsyncIOMotorClient(MONGODB_URL)

# Base de datos
db = client[DB_NAME]

# Colección opiniones
coleccion_opiniones = db["opiniones"]