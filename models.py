from sqlalchemy import (create_engine, Column, Integer, String,
                        Float, DateTime, Boolean)
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import configparser
from datetime import datetime


# Crear la clase base de la tabla
class Base(DeclarativeBase):
    pass


# Datos de configuración
config = configparser.ConfigParser()
config.read("proyecto.cfg")
db = config["db"]["db"]
if db == "sqlite":
    system = config["db"]["sqlite"]
elif db == "postgresql":
    system = config["db"]["postgresql"]


# Definir el modelo TestData
class TestData(Base):
    __tablename__ = "data_proyecto"

    id = Column(Integer, primary_key=True)
    # Campo obligatorio
    group = Column(String, nullable=False)
    # Campo obligatorio
    timestamp = Column(DateTime, nullable=False)
    # Indica si hay luz solar
    sunlight = Column(Boolean, nullable=False)
    # Almacena cada muestra de datos
    value = Column(Float, nullable=False)
    minutes = Column(Integer, nullable=False)

    def __repr__(self):
        return (f"<TestData(id={self.id}, group={self.group}, "
                "timestamp={self.timestamp}, "
                f"sunlight={self.sunlight}, value={self.value}), "
                " minutes={self.minutes})>")

    # Calcula los minutos automáticamente al asignar el timestamp
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.timestamp:
            self.minutes = self.calculate_minutes(self.timestamp)

    @staticmethod
    def calculate_minutes(timestamp: datetime) -> int:
        """Calcula los minutos desde la medianoche"""
        return timestamp.hour * 60 + timestamp.minute


# Crear la conexión a la base de datos (SQLite o PostgreSQL)
engine = create_engine(system)
Session = sessionmaker(bind=engine)
session = Session()

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)
