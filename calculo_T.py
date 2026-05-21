import csv

def buscar_en_csv(nombre_archivo, pulgadas):
    if not pulgadas or pulgadas == "0":
        return 0, 0
        
    try:
        with open(f"Medidas_Tanques/{nombre_archivo}", mode="r") as archivo:
            lector = csv.reader(archivo)
            next(lector) 
            
            for fila in lector:
                if fila[0] == pulgadas:
                    galones_totales = int(float(fila[1]))
                    galones_venta = galones_totales - 300 # Se restan 300 de la reserva del tanque
                    
                    if galones_venta < 0: 
                        galones_venta = 0
                    return galones_totales, galones_venta
                    
    except FileNotFoundError:
        print(f"Error: No encuentro el archivo {nombre_archivo}")
    
    # si escriben un número que no existe en la tabla
    return 0, 0