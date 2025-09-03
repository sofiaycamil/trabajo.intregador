import sqlite3
from tkinter import *
from tkinter import messagebox

conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

def agregar_habitacion():
    try:
        cursor.execute("INSERT INTO habitaciones (id, tipo, numero, precio) VALUES (?, ?, ?, ?)",
                       (id_hab.get(), tipo_hab.get(), numero_hab.get(), precio_hab.get()))
        conn.commit()
        messagebox.showinfo("Éxito", "Habitación agregada correctamente")
        limpiar_habitaciones()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar la habitación{e}")

def agregar_reserva():
    try:
        cursor.execute("INSERT INTO reserva (id, nombre, dni, fecha, habitaciones) VALUES (?, ?, ?, ?, ?)",
                       (id_res.get(), nombre_res.get(), dni_res.get(), fecha_res.get(), hab_res.get()))
        conn.commit()
        messagebox.showinfo("Éxito", "Reserva agregada correctamente")
        limpiar_reservas()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar la reserva{e}")

def mostrar_reservas_habitaciones():
    try:
        cursor.execute("""
            SELECT r.nombre, r.dni, r.fecha, h.tipo, h.numero, h.precio
            FROM reserva r
            INNER JOIN habitaciones h ON r.habitaciones = h.id
        """)
        filas = cursor.fetchall()
        if not filas:
            messagebox.showinfo("Resultados", "No hay reservas cargadas todavía")
        else:
            resultado = ""
            for fila in filas:
                resultado += f"Cliente: {fila[0]} | DNI: {fila[1]} | Fecha: {fila[2]} | Habitación: {fila[3]} N°{fila[4]} | Precio: ${fila[5]}"
            messagebox.showinfo("Reservas con habitaciones", resultado)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo realizar el INNER JOIN{e}")

def limpiar_habitaciones():
    id_hab.set("")
    tipo_hab.set("")
    numero_hab.set("")
    precio_hab.set("")

def limpiar_reservas():
    id_res.set("")
    nombre_res.set("")
    dni_res.set("")
    fecha_res.set("")
    hab_res.set("")

ventana = Tk()
ventana.title("Sistema de Reservas de Hotel")
ventana.geometry("600x500")

id_hab = StringVar()
tipo_hab = StringVar()
numero_hab = StringVar()
precio_hab = StringVar()

id_res = StringVar()
nombre_res = StringVar()
dni_res = StringVar()
fecha_res = StringVar()
hab_res = StringVar()


frame_hab = LabelFrame(ventana, text="Habitaciones", padx=10, pady=10)
frame_hab.pack(fill="both", expand="yes", padx=20, pady=10)

Label(frame_hab, text="ID").grid(row=0, column=0)
Entry(frame_hab, textvariable=id_hab).grid(row=0, column=1)

Label(frame_hab, text="Tipo").grid(row=1, column=0)
Entry(frame_hab, textvariable=tipo_hab).grid(row=1, column=1)

Label(frame_hab, text="Número").grid(row=2, column=0)
Entry(frame_hab, textvariable=numero_hab).grid(row=2, column=1)

Label(frame_hab, text="Precio").grid(row=3, column=0)
Entry(frame_hab, textvariable=precio_hab).grid(row=3, column=1)

Button(frame_hab, text="Agregar Habitación", command=agregar_habitacion).grid(row=4, column=0, columnspan=2, pady=5)


frame_res = LabelFrame(ventana, text="Reservas", padx=10, pady=10)
frame_res.pack(fill="both", expand="yes", padx=20, pady=10)

Label(frame_res, text="ID").grid(row=0, column=0)
Entry(frame_res, textvariable=id_res).grid(row=0, column=1)

Label(frame_res, text="Nombre").grid(row=1, column=0)
Entry(frame_res, textvariable=nombre_res).grid(row=1, column=1)

Label(frame_res, text="DNI").grid(row=2, column=0)
Entry(frame_res, textvariable=dni_res).grid(row=2, column=1)

Label(frame_res, text="Fecha").grid(row=3, column=0)
Entry(frame_res, textvariable=fecha_res).grid(row=3, column=1)

Label(frame_res, text="ID Habitación").grid(row=4, column=0)
Entry(frame_res, textvariable=hab_res).grid(row=4, column=1)

Button(frame_res, text="Agregar Reserva", command=agregar_reserva).grid(row=5, column=0, columnspan=2, pady=5)
Button(ventana, text="Mostrar Reservas con Habitaciones", command=mostrar_reservas_habitaciones, bg="lightblue").pack(pady=20)

ventana.mainloop()