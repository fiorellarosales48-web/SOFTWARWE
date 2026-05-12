import tkinter as tk
from tkinter import messagebox
import re


# -------------------------------
# CONSTANTES DEL SISTEMA
MAX_INTENTOS = 3


# -------------------------------
# CLASE USUARIO
class Usuario:
    """
    Representa un usuario del sistema con credenciales seguras.
    Aplica encapsulamiento para proteger los datos.
    """

    def __init__(self, nombre_usuario, contrasena):
        self.__nombre_usuario = nombre_usuario
        self.__contrasena = contrasena

    def validar_acceso(self, usuario, contrasena):
        """
        Valida si las credenciales ingresadas son correctas.

        Retorna:
            bool: True si coinciden, False en caso contrario.
        """
        return (
            self.__nombre_usuario == usuario
            and self.__contrasena == contrasena
        )


# -------------------------------
# CLASE SISTEMA DE ACCESO
class SistemaAcceso:
    """
    Gestiona usuarios, validación de login y seguridad de contraseñas.
    Aplica abstracción para ocultar la lógica interna.
    """

    def __init__(self):
        self.__usuarios = []
        self.__intentos = 0

    def agregar_usuario(self, usuario):
        """
        Agrega un usuario al sistema.
        """
        self.__usuarios.append(usuario)

    def validar_credenciales(self, usuario, contrasena):
        """
        Verifica si el usuario existe y la contraseña es correcta.
        """
        for user in self.__usuarios:
            if user.validar_acceso(usuario, contrasena):
                return True
        return False

    def validar_seguridad_contrasena(self, contrasena):
        """
        Valida que la contraseña cumpla con los requisitos de seguridad:
        - mínimo 8 caracteres
        - una mayúscula
        - un número
        - un símbolo
        """
        if len(contrasena) < 8:
            return False
        if not re.search(r"[A-Z]", contrasena):
            return False
        if not re.search(r"[0-9]", contrasena):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", contrasena):
            return False
        return True

    def intentar_login(self, usuario, contrasena):
        """
        Controla el proceso de inicio de sesión y los intentos permitidos.
        """
        if self.__intentos >= MAX_INTENTOS:
            return "bloqueado"

        if not self.validar_seguridad_contrasena(contrasena):
            return "seguridad"

        if self.validar_credenciales(usuario, contrasena):
            return "correcto"
        else:
            self.__intentos += 1
            return "incorrecto"


# -------------------------------
# INTERFAZ GRÁFICA
class Interfaz:
    """
    Interfaz gráfica del sistema de login.
    Permite interacción con el usuario.
    """

    def __init__(self, sistema):
        self.sistema = sistema

        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Acceso")
        self.ventana.geometry("400x320")
        self.ventana.configure(bg="#1e1e2f")

        fuente = ("Arial", 12)

        # Título
        tk.Label(
            self.ventana,
            text="Inicio de Sesión",
            bg="#1e1e2f",
            fg="white",
            font=("Arial", 16, "bold"),
        ).pack(pady=10)

        # Usuario
        tk.Label(
            self.ventana,
            text="Usuario",
            bg="#1e1e2f",
            fg="white",
            font=fuente,
        ).pack()

        self.usuario_entry = tk.Entry(self.ventana, font=fuente)
        self.usuario_entry.pack(pady=5)

        # Contraseña
        tk.Label(
            self.ventana,
            text="Contraseña",
            bg="#1e1e2f",
            fg="white",
            font=fuente,
        ).pack()

        self.contrasena_entry = tk.Entry(
            self.ventana,
            show="*",
            font=fuente,
        )
        self.contrasena_entry.pack(pady=5)

        # Mostrar contraseña
        self.mostrar_contrasena = tk.BooleanVar()

        tk.Checkbutton(
            self.ventana,
            text="Mostrar contraseña",
            variable=self.mostrar_contrasena,
            command=self.toggle_password,
            bg="#1e1e2f",
            fg="white",
            selectcolor="#1e1e2f",
        ).pack()

        # Botón login
        tk.Button(
            self.ventana,
            text="Ingresar",
            bg="#4CAF50",
            fg="white",
            font=fuente,
            command=self.login,
        ).pack(pady=15)

    def toggle_password(self):
        """
        Muestra u oculta la contraseña en el campo de entrada.
        """
        if self.mostrar_contrasena.get():
            self.contrasena_entry.config(show="")
        else:
            self.contrasena_entry.config(show="*")

    def login(self):
        """
        Procesa el intento de inicio de sesión.
        """
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()

        resultado = self.sistema.intentar_login(usuario, contrasena)

        if resultado == "correcto":
            messagebox.showinfo("Éxito", "Acceso concedido")
        elif resultado == "incorrecto":
            messagebox.showerror("Error", "Datos incorrectos")
        elif resultado == "seguridad":
            messagebox.showwarning(
                "Advertencia",
                "La contraseña no cumple con los requisitos:\n"
                "- 8 caracteres\n- Mayúscula\n- Número\n- Símbolo",
            )
        elif resultado == "bloqueado":
            messagebox.showerror("Bloqueado", "Demasiados intentos")


# -------------------------------
# PROGRAMA PRINCIPAL
if __name__ == "__main__":
    sistema = SistemaAcceso()

    sistema.agregar_usuario(Usuario("Nathaly", "Nathaly03@"))
    sistema.agregar_usuario(Usuario("Genesis", "Genesis123$"))
    sistema.agregar_usuario(Usuario("Santiago", "Cedeno123"))

    interfaz = Interfaz(sistema)
    interfaz.ventana.mainloop()
