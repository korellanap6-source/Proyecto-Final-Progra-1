import psycopg2
import os
from dotenv import load_dotenv
import csv

load_dotenv()

def conexion():
    try:
        URL_CONEXION = os.getenv("DATABASE_URL")
        return psycopg2.connect(URL_CONEXION)
    except Exception as e:
        print(f"Error de conexion: {e}")
        return None
    
def crear_tabla_calibraciones():

    conexion_bd=conexion()

    if conexion_bd is None:
        return
    
    try:
        cursor=conexion_bd.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calibracion_tanques(
                id SERIAL PRIMARY KEY,
                combustible VARCHAR(20) NOT NULL,
                pulgadas REAL NOT NULL,
                galones REAL NOT NULL
            );
        ''')
        conexion_bd.commit()
        print("Tabla 'calibracion_tanques' lista en la nube")
    except Exception as e:
        print(f"Error al crear tabla: {e}")
    finally:
        cursor.close()
        conexion_bd.close()

def migrar_archivos(nombre_archivo, tipo_combustible):
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    ruta_absoluta = os.path.join(ruta_script, nombre_archivo)

    conexion_db=conexion()
    if conexion_db is None:
        return
    
    try:
        cursor=conexion_db.cursor()

        with open(ruta_absoluta, mode="r") as archivo:
            lector=csv.reader(archivo)
            next(lector)

            for fila in lector:
                pulgadas=float(fila[0])
                galones=float(fila[1])

                cursor.execute('''
                    INSERT INTO calibracion_tanques (combustible, pulgadas, galones)
                        VALUES (%s, %s, %s);
                ''', (tipo_combustible, pulgadas, galones))
        conexion_db.commit()
        print(f"Datos de {tipo_combustible} migrados con éxito")

    except FileExistsError:
        print(f" No se encontró el archivo: {ruta_absoluta}")
    except Exception as e:
        print(f"Error migrando {tipo_combustible}: {e}")
    finally:
        cursor.close()
        conexion_db.close()
        
if __name__=="__main__":
    print("Iniciando conexión con la base de datos")

    crear_tabla_calibraciones()

    migrar_archivos("calibracion_diesel.csv", "DIESEL")
    migrar_archivos("calibracion_regular.csv", "REGULAR")
    migrar_archivos("calibracion_super.csv", "SUPER")
    
    print("Migración terminada")
