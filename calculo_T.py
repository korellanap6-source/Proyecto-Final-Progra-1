import psycopg2

import os

from dotenv import load_dotenv



load_dotenv



#establece conexion con la base de datos

def conexion():

    try:

        URL_CONEXION= os.getenv("DATABASE_URL")

        return psycopg2.connect(URL_CONEXION)

    except Exception as e:

        print(f"Error en la conexion: {e}")

        return None

   

def buscar_medida(combustible, pulgadas):

    #si el empleado dejó la caja de pulgadas en blanco, o puso un número negativo, el programa automáticamente devuelve 0

    if not pulgadas or float(pulgadas) <= 0:

        return 0,0

   

    bd_conexion=conexion()

    if bd_conexion is None:

        return 0,0

   

    try:

        cursor=bd_conexion.cursor()

        cursor.execute('''

                       SELECT galones FROM calibracion_tanques

                       WHERE combustible =%s AND pulgadas =%s;

                       ''', (combustible, float(pulgadas)))

        resultado= cursor.fetchone()



        if resultado:

            galones_totales= int(resultado[0])

            # Restamos la reserva para saber cuántos se pueden vender

            galones_venta = galones_totales-300



            if galones_venta<0:

                galones_venta=0

            return galones_totales, galones_venta

       

    except Exception as e:

        print(f"Error consultando la base de datos: {e}")

    finally:

        cursor.close()

        bd_conexion.close

    return 0,0 

def editar_registro_completo(id_registro, nuevo_combustible, nuevas_pulgadas, nueva_fecha):
    bd_conexion = conexion()
    if bd_conexion is None:
        return False
    try:
        cursor = bd_conexion.cursor()
       
        sql = "UPDATE calibracion_tanques SET combustible = %s, pulgadas = %s, fecha_registro = %s WHERE id = %s"
        cursor.execute(sql, (nuevo_combustible, float(nuevas_pulgadas), nueva_fecha, id_registro))
        bd_conexion.commit()
        return True
    except Exception as e:
        print(f"Error al editar: {e}")
        return False
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if bd_conexion and not bd_conexion.closed:
            bd_conexion.close()
