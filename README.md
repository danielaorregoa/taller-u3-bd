# Taller U3 - Automatización de BD con Python, Faker y Git

## ¿Qué hace este proyecto?

Un script de Python (`main.py`) que automatiza la creación y el poblado de una base de datos MySQL local:

1. Lee la URL de conexión desde un archivo `.env`.
2. Crea la base de datos `taller_u3` si no existe.
3. Crea la tabla `personas_danielaorregoarcila` si no existe.
4. Genera 100.000 personas falsas con **Faker** y las inserta con **SQLAlchemy**, por lotes de 5.000.

Cada vez que se ejecuta, la tabla se vacía antes de insertar, así que siempre quedan exactamente 100.000 registros.

## Estructura de la tabla

| Columna | Tipo | Origen |
|---|---|---|
| id | INT, clave primaria, auto incremento | MySQL |
| nombre | VARCHAR(100) | Faker |
| apellido | VARCHAR(100) | Faker |
| correo | VARCHAR(150) | Faker |
| telefono | VARCHAR(50) | Faker |
| fecha_nacimiento | DATE | Faker |
| ciudad | VARCHAR(100) | Faker |
| direccion | VARCHAR(255) | Faker |
| profesion | VARCHAR(150) | Faker |
| created_at | TIMESTAMP | MySQL |
| updated_at | TIMESTAMP | MySQL |

## Requisitos

- Python 3.10 o superior
- MySQL Server instalado y en ejecución en el computador local
- Git

## Instalación

```
git clone https://github.com/danielaorregoa/taller-u3-bd.git
cd taller-u3-bd
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Los comandos de activación son para Windows (PowerShell).

## Configuración

Copia la plantilla `.env.example` a un archivo `.env` y reemplaza `usuario` y `password` por los datos reales de tu MySQL:

```
copy .env.example .env
```

El archivo `.env` debe quedar así (el nombre de la base de datos es `taller_u3`):

```
DATABASE_URL=mysql+pymysql://usuario:password@localhost:3306/taller_u3
```

El archivo `.env` está en el `.gitignore`, por lo que nunca se sube al repositorio.

## Ejecución

```
python main.py
```

Al terminar debe mostrar: `Listo: la tabla personas_danielaorregoarcila tiene 100000 registros.`

## Verificación

En DBeaver o en el cliente de MySQL:

```
SELECT COUNT(*) FROM personas_danielaorregoarcila;
```

El resultado debe ser 100000.

## Librerías usadas

SQLAlchemy, PyMySQL, Faker, python-dotenv y cryptography (necesaria para que PyMySQL se conecte a MySQL 8).