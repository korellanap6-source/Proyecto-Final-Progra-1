import psycopg2
import os
from dotenv import load_dotenv

# CORRECCIÓN: Faltaban los paréntesis aquí
load_dotenv()

# establece conexion con la base de datos
def conexion():
    try: 
        URL_CONEXION= os.getenv("DATABASE_URL")
        return psycopg2.connect(URL_CONEXION)
    except Exception as e:
        print(f"Error en la conexion: {e}")
        return None
    
def buscar_medida(combustible, pulgadas):
    # si el empleado dejó la caja de pulgadas en blanco, o puso un número negativo, el programa automáticamente devuelve 0
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
        if 'cursor' in locals() and cursor:
            cursor.close()
        # CORRECCIÓN: Faltaban los paréntesis en close()
        if bd_conexion:
            bd_conexion.close()
            
    return 0,0

# =======================================================
# NUEVAS FUNCIONES PARA LA PESTAÑA "EDITAR REGISTRO"
# =======================================================

def obtener_registro_por_fecha(fecha):
    """Busca un registro único en la base de datos basado en la fecha"""
    bd_conexion = conexion()
    if bd_conexion is None:
        return None
    
    try:
        cursor = bd_conexion.cursor()
        cursor.execute("SELECT * FROM registros_medidas WHERE fecha = %s;", (fecha,))
        resultado = cursor.fetchone()
        return resultado
    except Exception as e:
        print(f"Error consultando por fecha: {e}")
        return None
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if bd_conexion:
            bd_conexion.close()

def actualizar_registro(fecha, d_pulg, d_gls, d_ven, r_pulg, r_gls, r_ven, s_pulg, s_gls, s_ven):
    """Actualiza los datos de un registro existente usando la fecha como condición"""
    bd_conexion = conexion()
    if bd_conexion is None:
        return False
    
    try:
        cursor = bd_conexion.cursor()
        consulta = """
            UPDATE registros_medidas 
            SET diesel_pulg = %s, diesel_gls = %s, diesel_venta = %s,
                regular_pulg = %s, regular_gls = %s, regular_venta = %s,
                super_pulg = %s, super_gls = %s, super_venta = %s
            WHERE fecha = %s;
        """
        valores = (d_pulg, d_gls, d_ven, r_pulg, r_gls, r_ven, s_pulg, s_gls, s_ven, fecha)
        cursor.execute(consulta, valores)
        bd_conexion.commit()
        # Retorna True si se modificó exitosamente alguna fila
        return cursor.rowcount > 0 
    except Exception as e:
        print(f"Error al actualizar registro: {e}")
        return False
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if bd_conexion:
            bd_conexion.close()

    

