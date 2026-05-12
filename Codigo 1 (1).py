import tkinter as tk
from tkinter import messagebox

# -------------------------------
# CONSTANTES DEL SISTEMA DE AUTENTICACIÓN
USUARIOS_VALIDOS = {
    "Nathaly": "Nathaly03@",
    "Genesis": "Genesis123$"
    "Fiorella": "fiorell123"
}

MAX_INTENTOS = 3


# -------------------------------
# FUNCIONES DEL SISTEMA
def validar_credenciales(usuario, contrasena):
    """
    Valida si las credenciales ingresadas existen en el sistema.
    Retorna:
        bool: True si son correctas, False si no lo son.
    """
    if usuario in USUARIOS_VALIDOS:
        if USUARIOS_VALIDOS[usuario] == contrasena:
            return True
    return False


def intentar_login(entry_usuario, entry_contrasena, ventana, intentos_info):
    """
    Obtiene los datos de la ventana y valida credenciales.
    Controla el número máximo de intentos.
    """
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    if validar_credenciales(usuario, contrasena):
        messagebox.showinfo("Resultado", "✅ Acceso concedido")
        ventana.destroy()  # Cierra la ventana si el acceso es correcto
    else:
        intentos_info["intentos"] += 1
        if intentos_info["intentos"] >= MAX_INTENTOS:
            messagebox.showerror("Resultado", "❌ Acceso denegado. Límite de intentos alcanzado.")
            ventana.destroy()  # Cierra la ventana si se superan los intentos
        else:
            messagebox.showwarning("Resultado", f"Datos incorrectos. Intento {intentos_info['intentos']} de {MAX_INTENTOS}")


def main():
    """
    Controla el flujo principal del programa de autenticación.
    Crea la ventana gráfica y maneja los intentos de acceso.
    """
    ventana = tk.Tk()
    ventana.title("Sistema de Autenticación")
    ventana.geometry("300x180")

    # Diccionario para contar intentos
    intentos_info = {"intentos": 0}

    # Etiquetas y entradas
    label_usuario = tk.Label(ventana, text="Usuario:")
    label_usuario.pack(pady=5)
    entry_usuario = tk.Entry(ventana)
    entry_usuario.pack(pady=5)

    label_contrasena = tk.Label(ventana, text="Contraseña:")
    label_contrasena.pack(pady=5)
    entry_contrasena = tk.Entry(ventana, show="*")  # oculta la contraseña
    entry_contrasena.pack(pady=5)

    # Botón de login
    btn_login = tk.Button(
        ventana,
        text="Ingresar",
        command=lambda: intentar_login(entry_usuario, entry_contrasena, ventana, intentos_info)
    )
    btn_login.pack(pady=10)

    # Ejecutar ventana
    ventana.mainloop()


# -------------------------------
# EJECUCIÓN DEL PROGRAMA
if __name__ == "__main__":
    main()
