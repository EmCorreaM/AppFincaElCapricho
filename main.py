import tkinter as tk
from tkinter import messagebox, simpledialog
import gestion_insumos

def abrir_gestion_insumos():
    ventana_menu.withdraw()
    ventana_insumos = tk.Toplevel()
    ventana_insumos.title("Gestión de Insumos")
    ventana_insumos.geometry("600x500")
    ventana_insumos.configure(bg="#F0F5E1")  # Verde suave para un look más limpio y natural
    
    def actualizar_inventario():
        df = gestion_insumos.cargar_datos()
        lista.delete(0, tk.END)
        for index, row in df.iterrows():
            lista.insert(tk.END, f" {index}-   {row['Insumo']}     {row['Cantidad']} {row['Unidad']}     {row['Categoría']}")
        verificar_alertas(df)

    def agregar_insumo():
        df = gestion_insumos.cargar_datos()
        try:
            datos = [
                simpledialog.askstring("Insumo", "Nombre del insumo:").capitalize(),
                simpledialog.askstring("Categoría", "Categoría:").capitalize(),
                int(simpledialog.askstring("Cantidad", "Cantidad:")),  # Cambiado a askstring + conversión
                simpledialog.askstring("Unidad", "Unidad:").lower(),
                int(simpledialog.askstring("Stock Mínimo", "Stock mínimo:")),
                float(simpledialog.askstring("Costo", "Costo por unidad:"))
            ]
            
            # Validar números positivos
            if any(valor < 0 for valor in [datos[2], datos[4], datos[5]]):
                messagebox.showerror("Error", "Los valores numéricos no pueden ser negativos")
                return
                
            nuevo_registro = gestion_insumos.pd.DataFrame([datos], columns=gestion_insumos.COLUMNAS)
            df = gestion_insumos.pd.concat([df, nuevo_registro], ignore_index=True)
            gestion_insumos.guardar_datos(df)
            actualizar_inventario()
            
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un valor numérico válido")
        except AttributeError:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

        
    def modificar_insumo():
        df = gestion_insumos.cargar_datos()
        try:
            insumo = simpledialog.askstring("Modificar", "Nombre exacto del insumo:").capitalize()
            if insumo not in df["Insumo"].values:
                messagebox.showerror("Error", "El insumo no existe")
                return
                
            # Nueva validación numérica
            nueva_cantidad = simpledialog.askstring("Modificar", "Nueva cantidad:")
            if not nueva_cantidad.isdigit():
                messagebox.showerror("Error", "Debe ingresar un número entero")
                return
                
            df.loc[df["Insumo"] == insumo, "Cantidad"] = int(nueva_cantidad)
            gestion_insumos.guardar_datos(df)
            actualizar_inventario()
            
        except AttributeError:
            messagebox.showerror("Error", "Debe ingresar un nombre válido")
        
    def eliminar_insumo():
        df = gestion_insumos.cargar_datos()
        try:
            insumo = simpledialog.askstring("Eliminar", "Nombre exacto del insumo:").capitalize()
            if insumo not in df["Insumo"].values:
                messagebox.showerror("Error", "El insumo no existe")
                return
                
            confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar TODOS los registros de '{insumo}'?")
            if confirmar:
                df = df[df["Insumo"] != insumo]
                gestion_insumos.guardar_datos(df)
                actualizar_inventario()
                
        except AttributeError:
            messagebox.showerror("Error", "Debe ingresar un nombre válido")
    
    def verificar_alertas(df):
        for _, fila in df.iterrows():
            if fila["Cantidad"] <= fila["Stock Mínimo"]:
                messagebox.showwarning("ALERTA", 
                    f"{fila['Insumo']} bajo stock ({fila['Cantidad']}) {fila['Unidad']}")
        
    tk.Label(ventana_insumos, text="Inventario de Insumos", font=("Arial", 18, "bold"), bg="#F0F5E1", fg="#2C5F2D").pack(pady=10)
    
    header_frame = tk.Frame(ventana_insumos, bg="#F0F5E1")
    header_frame.pack()
    tk.Label(header_frame, text="Indice, Insumo, Cantidad, Categoria", font=("Arial", 12, "bold"), bg="#F0F5E1", fg="#2C5F2D", width=0).grid(row=0, column=0)
     
    lista = tk.Listbox(ventana_insumos, width=50, height=10, font=("Arial", 12), bd=2, relief="solid", bg="#E1F0DA", fg="#2C5F2D")
    lista.pack(pady=10, padx=10)
    
    botones_frame = tk.Frame(ventana_insumos, bg="#F0F5E1")
    botones_frame.pack(pady=10)
    
    estilo_botones = {"font": ("Arial", 12, "bold"), "bg": "#4CAF50", "fg": "white", "width": 18, "height": 2, "bd": 2, "relief": "raised"}
    
    btn_agregar = tk.Button(botones_frame, text="Agregar Insumo", command=agregar_insumo, **estilo_botones)
    btn_agregar.grid(row=0, column=0, padx=10, pady=5)
    
    btn_modificar = tk.Button(botones_frame, text="Modificar Insumo", command=modificar_insumo, **estilo_botones)
    btn_modificar.grid(row=1, column=0, padx=10, pady=5)
    
    btn_eliminar = tk.Button(botones_frame, text="Eliminar Insumo", command=eliminar_insumo, **estilo_botones)
    btn_eliminar.grid(row=0, column=1, padx=10, pady=5)
    
    btn_volver = tk.Button(botones_frame, text="Volver", command=lambda: [ventana_insumos.destroy(), ventana_menu.deiconify()], **estilo_botones)
    btn_volver.grid(row=1, column=1, padx=10, pady=5)
    
    actualizar_inventario()

def cerrar_programa():
    ventana_menu.destroy()

ventana_menu = tk.Tk()
ventana_menu.title("Finca El Capricho")
ventana_menu.geometry("600x450")
ventana_menu.configure(bg="#F0F5E1")

tk.Label(ventana_menu, text="Finca El Capricho", font=("Arial", 18, "bold"), bg="#F0F5E1", fg="#2C5F2D").pack(pady=10)

btn_insumos = tk.Button(ventana_menu, text="Inventario de Insumos", command=abrir_gestion_insumos, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=30, height=2, bd=2, relief="raised")
btn_insumos.pack(pady=5)

btn_animales = tk.Button(ventana_menu, text="Inventario Animal (No Implementado)", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=30, height=2, bd=2, relief="raised")
btn_animales.pack(pady=5)

btn_cerrar = tk.Button(ventana_menu, text="Cerrar Programa", command=cerrar_programa, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=30, height=2, bd=2, relief="raised")
btn_cerrar.pack(pady=5)

ventana_menu.mainloop()
