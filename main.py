import os
import sys

from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, make_url

NOMBRE_TABLA = "personas_danielaorregoarcila"
TOTAL_REGISTROS = 100_000
TAMANO_LOTE = 5_000

SQL_CREAR_TABLA = f"""
CREATE TABLE IF NOT EXISTS {NOMBRE_TABLA} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL,
    telefono VARCHAR(50),
    fecha_nacimiento DATE,
    ciudad VARCHAR(100),
    direccion VARCHAR(255),
    profesion VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
"""

SQL_INSERTAR = f"""
INSERT INTO {NOMBRE_TABLA}
    (nombre, apellido, correo, telefono, fecha_nacimiento, ciudad, direccion, profesion)
VALUES
    (:nombre, :apellido, :correo, :telefono, :fecha_nacimiento, :ciudad, :direccion, :profesion)
"""


def obtener_url():
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    if not url:
        print("Error: DATABASE_URL no esta definida en el archivo .env")
        sys.exit(1)
    return url


def asegurar_base_de_datos(url):
    datos = make_url(url)
    nombre_bd = datos.database
    if not nombre_bd:
        print("Error: la URL no incluye el nombre de la base de datos")
        sys.exit(1)

    url_servidor = URL.create(
        drivername=datos.drivername,
        username=datos.username,
        password=datos.password,
        host=datos.host,
        port=datos.port,
    )
    engine_servidor = create_engine(url_servidor)
    with engine_servidor.connect() as conn:
        conn.execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS `{nombre_bd}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        )
        conn.commit()
    engine_servidor.dispose()


def generar_personas(fake, cantidad):
    personas = []
    for _ in range(cantidad):
        personas.append(
            {
                "nombre": fake.first_name(),
                "apellido": fake.last_name(),
                "correo": fake.email(),
                "telefono": fake.phone_number(),
                "fecha_nacimiento": fake.date_of_birth(minimum_age=18, maximum_age=90),
                "ciudad": fake.city(),
                "direccion": fake.address().replace("\n", ", "),
                "profesion": fake.job(),
            }
        )
    return personas


def main():
    url = obtener_url()
    fake = Faker("es_ES")

    try:
        asegurar_base_de_datos(url)
        engine = create_engine(url)

        with engine.begin() as conn:
            conn.execute(text(SQL_CREAR_TABLA))
            conn.execute(text(f"TRUNCATE TABLE {NOMBRE_TABLA}"))

            insertados = 0
            while insertados < TOTAL_REGISTROS:
                cantidad = min(TAMANO_LOTE, TOTAL_REGISTROS - insertados)
                lote = generar_personas(fake, cantidad)
                conn.execute(text(SQL_INSERTAR), lote)
                insertados += cantidad
                print(f"Insertados {insertados} de {TOTAL_REGISTROS}")

            total = conn.execute(text(f"SELECT COUNT(*) FROM {NOMBRE_TABLA}")).scalar()

        print(f"Listo: la tabla {NOMBRE_TABLA} tiene {total} registros.")
    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()