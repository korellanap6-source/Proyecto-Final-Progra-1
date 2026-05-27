import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def conexion():
    try:
        # Asegúrate de que tu variable en el .env se llame DATABASE_URL
        URL_CONEXION = os.getenv("DATABASE_URL")
        return psycopg2.connect(URL_CONEXION)
    except Exception as e:
        print(f"Error de conexion en calculo_T: {e}")
        return None

def buscar_medida(combustible, pulgadas):
    """
    Busca los galones en la tabla de calibración según las pulgadas.
    Se usa para el ingreso de medidas nuevas.
    """
    conn = conexion()
    if not conn: return 0, 0
    try:
        cursor = conn.cursor()
        pulg_f = float(pulgadas) if pulgadas else 0.0
        
        # Buscamos el valor más cercano en la tabla de calibración
        cursor.execute("""
            SELECT galones 
            FROM calibracion_tanques 
            ORDER BY ABS(pulgadas - %s) ASC 
            LIMIT 1
        """, (pulg_f,))
        
        resultado = cursor.fetchone()
        galones = float(resultado[0]) if resultado else 0.0
        
        # Cálculo de venta (puedes ajustar esta fórmula según tu negocio)
        # Por defecto: Capacidad máxima (ej. 8000) - galones actuales
        venta = 8000.0 - galones 
        
        return galones, venta
    except:
        return 0, 0
    finally:
        conn.close()

def actualizar_registro_completo(id_registro, nuevo_combustible, nuevas_pulgadas, nueva_fecha):
    """
    Esta es la función que usa el botón GUARDAR CAMBIOS de la pestaña Editar.
    Maneja el caso donde el usuario escribe 'DIESEL' en lugar de un número.
    """
    bd_conexion = conexion()
    if bd_conexion is None: return False
    
    try:
        cursor = bd_conexion.cursor()
        
        # 1. Limpiar y validar el ID y las Pulgadas
        id_limpio = int(str(id_registro).strip())
        pulg_limpia = float(str(nuevas_pulgadas).strip())

        # 2. Buscar galones correspondientes a las nuevas pulgadas
        cursor.execute("""
            SELECT galones 
            FROM calibracion_tanques 
            ORDER BY ABS(pulgadas - %s) ASC 
            LIMIT 1
        """, (pulg_limpia,))
        
        resultado = cursor.fetchone()
        gls_actuales = float(resultado[0]) if resultado else 0.0

        # 3. LÓGICA ESPECIAL PARA LA VENTA
        # Si el usuario escribió la palabra "DIESEL", usamos un inventario base
        if str(nuevo_combustible).upper() == "DIESEL":
            # --- AJUSTA ESTE VALOR SEGÚN TU TANQUE REAL ---
            capacidad_base = 8000.0 
            venta_calculada = capacidad_base - gls_actuales
        else:
            # Si el usuario escribió un número, restamos ese número
            try:
                # Intentamos convertir lo que escribió el usuario a número
                inventario_manual = float(nuevo_combustible)
                venta_calculada = inventario_manual - gls_actuales
            except ValueError:
                # Si escribió cualquier otro texto que no sea DIESEL, ponemos venta 0
                venta_calculada = 0.0

        # 4. Ejecutar el UPDATE en la tabla de registros_medidas en Neon
        sql = """
            UPDATE registros_medidas 
            SET diesel_pulg = %s, 
                diesel_gls = %s, 
                diesel_venta = %s, 
                fecha = %s 
            WHERE id = %s
        """
        cursor.execute(sql, (pulg_limpia, gls_actuales, venta_calculada, nueva_fecha, id_limpio))
        
        bd_conexion.commit()
        
        # Imprime en la consola para que veas qué se envió
        print(f"DEBUG Neon: ID {id_limpio} actualizado. Gls: {gls_actuales}, Venta: {venta_calculada}")
        
        return cursor.rowcount > 0

    except Exception as e:
        print(f"Error crítico en actualizar_registro_completo: {e}")
        return False
    finally:
        bd_conexion.close()