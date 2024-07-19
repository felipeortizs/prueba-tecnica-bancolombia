from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from typing import List

app = FastAPI()

# Configuración de la base de datos
DATABASE_URL = "postgresql://postgres:admin@localhost:5432/banco"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modelo para la consulta de productos
class Producto(BaseModel):
    producto_final: str
    id_producto: str
    tipo_id_producto: str
    tasa_efectiva: float
    valor_final: float
    num_documento: str

# Modelo para la consulta de multiples productos
class MultiplesProductos(BaseModel):
    num_documento: str
    cantidad_productos: int
    total_valor_final: float

# Ruta para la consulta de productos
@app.get("/punto3/{num_documento}", response_model=List[Producto])
def consulta_producto(num_documento: str):
    session = SessionLocal()
    try:
        query = text("""
            SELECT
                producto_final,
                id_producto,
                tipo_id_producto,
                tasa_correspondiente_producto as tasa_efectiva,
                valor_final,
                num_documento
            FROM public.obligaciones_cliente_result
            WHERE num_documento = :num_documento
        """)
        result = session.execute(query, {"num_documento": num_documento}).fetchall()
        session.close()

        if not result:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        # esto es como se esta parseando la salida del endpoint
        productos = [
            Producto(
                producto_final=row[0],
                id_producto=row[1],
                tipo_id_producto=row[2],
                tasa_efectiva=row[3],
                valor_final=row[4],
                num_documento=row[5]
            ) for row in result
        ]

        return productos

    except SQLAlchemyError as e:
        session.close()
        raise HTTPException(status_code=500, detail=str(e))

# Ruta para la consulta de multiples productos
@app.get("/punto4/{num_documento}", response_model=MultiplesProductos)
def consulta_multiples_productos(num_documento: str):
    session = SessionLocal()
    try:
        query = text("""
            SELECT
                num_documento,
                cantidad_productos,
                total_valor_final
            FROM public.multiples_productos
            WHERE num_documento = :num_documento
        """)
        result = session.execute(query, {"num_documento": num_documento}).fetchone()
        session.close()

        if not result:
            raise HTTPException(status_code=404, detail="Registro no encontrado")

        multiples_productos = MultiplesProductos(
            num_documento=result[0],
            cantidad_productos=result[1],
            total_valor_final=result[2]
        )

        return multiples_productos

    except SQLAlchemyError as e:
        session.close()
        raise HTTPException(status_code=500, detail=str(e))

# Ejecutar el servidor con: uvicorn main:app --reload
