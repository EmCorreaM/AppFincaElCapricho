import pandas as pd
import os

ARCHIVO = "insumos.xlsx"
COLUMNAS = ["Insumo", "Categoría", "Cantidad", "Unidad", "Stock Mínimo", "Costo por unidad"]

def cargar_datos():
    if os.path.exists(ARCHIVO):
        return pd.read_excel(ARCHIVO)
    return pd.DataFrame(columns=COLUMNAS)

def guardar_datos(df):
    df.to_excel(ARCHIVO, index=False)

def agregar(df):
    datos = [
        input("Insumo: ").capitalize(),
        input("Categoría: ").capitalize(),
        int(input("Cantidad: ")),
        input("Unidad: ").lower(),
        int(input("Stock Mínimo: ")),
        float(input("Costo por unidad: "))
    ]
    nuevo_registro = pd.DataFrame([datos], columns=COLUMNAS)
    return pd.concat([df, nuevo_registro], ignore_index=True)

def actualizar(df):
    print(df.to_string())
    try:
        insumo = input("\nInsumo a modificar: ").capitalize()
        if insumo not in df["Insumo"].values:
            print("El insumo no existe.")
            return df

        indice = df[df["Insumo"] == insumo].index[0]

        cantidad_actual = df.at[indice, 'Cantidad']
        
        nueva_cantidad = input(f"Cantidad ({cantidad_actual}): ") 
        
        if nueva_cantidad[0] == "+":
            incremento = int(nueva_cantidad)
            nueva_cantidad = cantidad_actual + incremento
        elif nueva_cantidad[0] =="-":
            decremento = int(nueva_cantidad)
            nueva_cantidad = cantidad_actual + decremento
        else:
            nueva_cantidad = int(nueva_cantidad)
        
        df.at[indice, 'Cantidad'] = nueva_cantidad
        print(f"Cantidad actualizada correctamente. Nueva cantidad: {nueva_cantidad}")
    except Exception as e:
        print(f"Error en actualización: {e}")
    return df


def eliminar(df):
    print(df.to_string())
    try:
        indice = int(input("\nÍndice a eliminar: "))
        return df.drop(index=indice).reset_index(drop=True)
    except:
        return df

def verificar_alertas(df):
    for _, fila in df.iterrows():
        porcentaje = (fila["Cantidad"] - fila["Stock Mínimo"]) / fila["Stock Mínimo"]
        if porcentaje <= 0.15:
            print(f"\nALERTA: El {fila['Insumo']} está por agotarse. Cantidad disponible: {fila['Cantidad']}")

def listar(df):
    print("\n" + df.to_string())
    

def menu():
    df = cargar_datos()
    while True:
        print("\nGestión de Insumos")
        print("1. Agregar insumo")
        print("2. Modificar cantidad de insumo")
        print("3. Eliminar insumo")
        print("4. Mostrar inventario")
        print("5. Salir")

        verificar_alertas(df)
        
        opcion = input("Opción: ")
        if opcion == "1":
            df = agregar(df)
            guardar_datos(df)
        elif opcion == "2":
            df = actualizar(df)
            guardar_datos(df)
        elif opcion == "3":
            df = eliminar(df)
            guardar_datos(df)
        elif opcion == "4":
            listar(df)
        elif opcion == "5":
            break
        else:
            print("Opción inválida")