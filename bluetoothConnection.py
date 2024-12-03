import asyncio
import bleak
import tkinter as tk
from tkinter import messagebox
from threading import Thread

# Variables globales
dispositivos = []


# Función para buscar dispositivos Bluetooth
async def buscar_dispositivos_async():
    global dispositivos
    dispositivos = []  # Reiniciar la lista de dispositivos

    # Mostrar estado de búsqueda
    btn_buscar.config(state=tk.DISABLED, text="Buscando...")
    listbox.delete(0, tk.END)

    try:
        async with bleak.BleakScanner() as scanner:
            dispositivos = await scanner.discover()

        # Llenar la lista con los dispositivos encontrados
        for dispositivo in dispositivos:
            listbox.insert(tk.END, f"{dispositivo.name} ({dispositivo.address})")

        if not dispositivos:
            listbox.insert(tk.END, "No se encontraron dispositivos.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al buscar dispositivos: {e}")
    finally:
        btn_buscar.config(state=tk.NORMAL, text="Buscar Dispositivos")


def buscar_dispositivos():
    asyncio.run(buscar_dispositivos_async())


# Función para conectar al dispositivo seleccionado
async def conectar_dispositivo_async():
    global dispositivos
    seleccionado = listbox.curselection()
    if seleccionado:
        index = seleccionado[0]
        dispositivo = dispositivos[index]
        direccion = dispositivo.address

        try:
            cliente = bleak.BleakClient(direccion)
            await cliente.connect()
            messagebox.showinfo("Conexión Exitosa", f"Conectado a {dispositivo.name} ({direccion})")
            await cliente.disconnect()
        except bleak.BleakError as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a {dispositivo.name}: {e}")
    else:
        messagebox.showwarning("Selección", "Por favor, selecciona un dispositivo para conectar.")


def conectar_dispositivo():
    asyncio.run(conectar_dispositivo_async())


# Ejecución en un hilo separado para evitar conflictos
def ejecutar_busqueda_en_hilo():
    hilo = Thread(target=buscar_dispositivos)
    hilo.start()


def ejecutar_conexion_en_hilo():
    hilo = Thread(target=conectar_dispositivo)
    hilo.start()


# Crear la ventana principal
root = tk.Tk()
root.title("Conectar a Dispositivo Bluetooth")

# Crear un botón para buscar dispositivos
btn_buscar = tk.Button(root, text="Buscar Dispositivos", command=ejecutar_busqueda_en_hilo)
btn_buscar.pack(pady=10)

# Crear una lista para mostrar los dispositivos encontrados
listbox = tk.Listbox(root, width=50, height=15)
listbox.pack(pady=10)

# Crear un botón para conectar al dispositivo seleccionado
btn_conectar = tk.Button(root, text="Conectar", command=ejecutar_conexion_en_hilo)
btn_conectar.pack(pady=10)

# Ejecutar la aplicación tkinter
root.mainloop()
