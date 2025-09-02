import sqlite3
from tkinter import *
from tkinter import messagebox

conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

ventana = Tk()
ventana.title("Sistema de Reservas de Hotel")
ventana.geometry("550x550")

hab_tipo = StringVar()
hab_numero = StringVar()
hab_precio = StringVar()

res_nombre = StringVar()
res_dni = StringVar()
res_fecha = StringVar()
res_habitaciones = StringVar()

def alta_habitacion():
    try:
        conn.execute("INSERT INTO habitaciones (tipo, numero, precio) VALUES (?,?,?)",
                     (hab_tipo.get(), hab_numero.get(), float(hab_precio.get())))
        conn.commit()
        messagebox.showinfo("OK", "Habitación guardada")
        hab_tipo.set(""); hab_numero.set(""); hab_precio.set("")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def alta_reserva():
    try:
        conn.execute("INSERT INTO reserva (nombre, dni, fecha, habitaciones) VALUES (?,?,?,?)",
                     (res_nombre.get(), res_dni.get(), res_fecha.get(), int(res_habitaciones.get())))
        conn.commit()
        messagebox.showinfo("OK", "Reserva guardada")
        res_nombre.set(""); res_dni.set(""); res_fecha.set(""); res_habitaciones.set("")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def mostrar_join():
    cursor.execute("""
    SELECT reserva.id, nombre, dni, fecha, habitaciones.numero, habitaciones.tipo, habitaciones.precio
    FROM reserva
    INNER JOIN habitaciones ON reserva.habitaciones = habitaciones.id
    """)
    filas = cursor.fetchall()
    texto = ""
    for f in filas:
        texto += f"Reserva {f[0]} - Cliente: {f[1]}, DNI: {f[2]}, Fecha: {f[3]}, Habitación: {f[4]} ({f[5]}) ${f[6]}\n"
    if texto == "":
        texto = "No hay reservas registradas."
    messagebox.showinfo("Reservas con Habitaciones", texto)

marco = Frame(ventana, padx=10, pady=10, bd=5, relief=SOLID)
marco.pack(side=TOP, fill=X)
Label(marco, text="Alta Habitación").pack()
Entry(marco, textvariable=hab_tipo, justify="center").pack()
Entry(marco, textvariable=hab_numero, justify="center").pack()
Entry(marco, textvariable=hab_precio, justify="center").pack()
Button(marco, text="Guardar Habitación", command=alta_habitacion).pack()

Label(marco, text="Alta Reserva").pack()
Entry(marco, textvariable=res_nombre, justify="center").pack()
Entry(marco, textvariable=res_dni, justify="center").pack()
Entry(marco, textvariable=res_fecha, justify="center").pack()
Entry(marco, textvariable=res_habitaciones, justify="center").pack()
Button(marco, text="Guardar Reserva", command=alta_reserva).pack()

Button(marco, text="Mostrar Reservas con Habitaciones", command=mostrar_join).pack()
ventana.mainloop()
conn.close()
