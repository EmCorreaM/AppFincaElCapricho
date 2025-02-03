import gestion_insumos

def mostrar_menu_principal():
    while True:
        print("\nFinca El Capricho")
        print("1. Inventario de Insumos")
        print("2. Inventario Animal")
        print("3. Cerrar programa")
        opcion = input("Opción: ")
        
        if opcion == "1":
            gestion_insumos.menu()
        elif opcion == "2":
            print("\nFunción no implementada")
            continue
        elif opcion == "3":
            break
        else:
            print("\nOpción inválida")

if __name__ == "__main__":
    mostrar_menu_principal()