import tkinter as tk  # librería para interfaz gráfica
from tkinter import messagebox  # mensajes emergentes (alertas, info)
import os  # manejo de archivos del sistema
import re  # expresiones regulares (validación de correo)


# -------------------------------
# 📌 USUARIOS DEL SISTEMA (LOGIN)
# aquí se definen los usuarios permitidos para entrar al sistema
USUARIOS_SISTEMA = {
    "Nathaly": "Nathaly03@",
    "Genesis": "Genesis123$",
    "Santiago":"Cedeno123"
}

# archivo donde se guardan los clientes
ARCHIVO_CLIENTES = "clientes.txt"


# -------------------------------
# 📌 CLASE PRINCIPAL DEL SISTEMA DE CLIENTES
# aquí se maneja toda la lógica de clientes (guardar, validar, buscar)
class SistemaClientes:

    def __init__(self):
        # lista en memoria donde se guardan los clientes cargados
        self.clientes = []

        # al iniciar el sistema, carga clientes desde el archivo
        self.cargar_clientes()

    # ---------------------------
    # carga los clientes desde el archivo txt a la lista en memoria
    def cargar_clientes(self):

        # verifica si el archivo existe
        if os.path.exists(ARCHIVO_CLIENTES):

            # abre el archivo en modo lectura
            with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as file:

                # lee cada línea del archivo
                for linea in file:

                    # separa los datos por coma
                    datos = linea.strip().split(",")

                    # valida que tenga todos los campos
                    if len(datos) == 4:

                        # guarda cliente en lista como diccionario
                        self.clientes.append({
                            "nombres": datos[0],
                            "cedula": datos[1],
                            "celular": datos[2],
                            "correo": datos[3]
                        })

    # ---------------------------
    # guarda un cliente en el archivo txt
    def guardar_cliente(self, nombres, cedula, celular, correo):

        # abre archivo en modo agregar (append)
        with open(ARCHIVO_CLIENTES, "a", encoding="utf-8") as file:

            # escribe el cliente en formato separado por comas
            file.write(f"{nombres},{cedula},{celular},{correo}\n")

    # ---------------------------
    # valida todos los datos ingresados del cliente
    def validar_datos(self, nombres, cedula, celular, correo):

        # debe tener 4 palabras (2 nombres + 2 apellidos)
        if len(nombres.strip().split()) != 4:
            return "nombre_invalido"

        # cédula debe ser numérica y de 10 dígitos
        if not cedula.isdigit() or len(cedula) != 10:
            return "cedula_invalida"

        # celular debe ser numérico y de 10 dígitos
        if not celular.isdigit() or len(celular) != 10:
            return "celular_invalido"

        # validación básica de correo electrónico
        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            return "correo_invalido"

        # si todo está correcto
        return "ok"

    # ---------------------------
    # registra un cliente nuevo en memoria y archivo
    def registrar_cliente(self, nombres, cedula, celular, correo):

        # verifica si la cédula ya existe (evita duplicados)
        for c in self.clientes:
            if c["cedula"] == cedula:
                return "duplicado"

        # agrega cliente a la lista en memoria
        self.clientes.append({
            "nombres": nombres,
            "cedula": cedula,
            "celular": celular,
            "correo": correo
        })

        # guarda cliente en archivo
        self.guardar_cliente(nombres, cedula, celular, correo)

        return "ok"

    # ---------------------------
    # busca un cliente por número de cédula
    def buscar_afiliado(self, cedula):

        # recorre la lista de clientes
        for c in self.clientes:

            # si encuentra coincidencia
            if c["cedula"] == cedula:
                return c

        # si no encuentra nada
        return None


# -------------------------------
# 📌 VENTANA DE LOGIN
class LoginWindow:

    def __init__(self, sistema):
        self.sistema = sistema  # referencia al sistema de clientes

        # crea ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("LOGIN SISTEMA")
        self.ventana.geometry("320x230")
        self.ventana.configure(bg="#d6eaf8")

        # etiqueta usuario
        tk.Label(self.ventana, text="Usuario", bg="#d6eaf8").pack()

        # campo de entrada usuario
        self.user = tk.Entry(self.ventana)
        self.user.pack(pady=3)

        # etiqueta contraseña
        tk.Label(self.ventana, text="Contraseña", bg="#d6eaf8").pack()

        # frame para organizar contraseña + botón ver
        frame_pass = tk.Frame(self.ventana, bg="#d6eaf8")
        frame_pass.pack()

        # campo contraseña (oculta texto con *)
        self.passw = tk.Entry(frame_pass, show="*")
        self.passw.grid(row=0, column=0)

        # variable para saber si está visible o no
        self.ver = False

        # botón para mostrar/ocultar contraseña
        tk.Button(
            frame_pass,
            text="👁",
            command=self.toggle_pass,
            bg="#aed6f1"
        ).grid(row=0, column=1, padx=5)

        # botón de login
        tk.Button(
            self.ventana,
            text="Ingresar",
            bg="#85c1e9",
            command=self.login
        ).pack(pady=10)

        # inicia la ventana
        self.ventana.mainloop()

    # ---------------------------
    # muestra u oculta la contraseña
    def toggle_pass(self):

        if self.ver:
            self.passw.config(show="*")
            self.ver = False
        else:
            self.passw.config(show="")
            self.ver = True

    # ---------------------------
    # valida el login del sistema
    def login(self):

        # obtiene datos ingresados
        u = self.user.get()
        p = self.passw.get()

        # valida contra diccionario de usuarios
        if u in USUARIOS_SISTEMA and USUARIOS_SISTEMA[u] == p:

            messagebox.showinfo("OK", "Acceso concedido")

            # cierra login
            self.ventana.destroy()

            # abre menú principal
            MenuWindow(self.sistema)

        else:
            messagebox.showerror("Error", "Credenciales incorrectas")


# -------------------------------
# 📌 MENÚ PRINCIPAL
class MenuWindow:

    def __init__(self, sistema):
        self.sistema = sistema

        # ventana menú
        self.ventana = tk.Tk()
        self.ventana.title("MENÚ CLIENTES")
        self.ventana.geometry("300x250")
        self.ventana.configure(bg="#d6eaf8")

        # título
        tk.Label(self.ventana, text="GESTIÓN CLIENTES", bg="#d6eaf8").pack(pady=10)

        # botón registrar cliente
        tk.Button(
            self.ventana,
            text="Registrar cliente",
            bg="#85c1e9",
            command=self.abrir_registro
        ).pack(pady=5)

        # botón cliente afiliado
        tk.Button(
            self.ventana,
            text="Cliente afiliado",
            bg="#85c1e9",
            command=self.abrir_afiliado
        ).pack(pady=5)

        self.ventana.mainloop()

    # abre ventana de registro
    def abrir_registro(self):
        RegistroCliente(self.ventana, self.sistema)

    # abre ventana de afiliado
    def abrir_afiliado(self):
        AfiliadoCliente(self.ventana, self.sistema)


# -------------------------------
# 📌 REGISTRO DE CLIENTE
class RegistroCliente:

    def __init__(self, parent, sistema):
        self.sistema = sistema

        # ventana secundaria
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("REGISTRO CLIENTE")
        self.ventana.geometry("350x350")
        self.ventana.configure(bg="#ebf5fb")

        # campos del formulario
        self.crear_input("Nombres y Apellidos", "nombres")
        self.crear_input("Cédula", "cedula")
        self.crear_input("Celular", "celular")
        self.crear_input("Correo", "correo")

        # botón guardar
        tk.Button(
            self.ventana,
            text="Guardar",
            bg="#85c1e9",
            command=self.guardar
        ).pack(pady=10)

    # crea campos de entrada reutilizables
    def crear_input(self, texto, nombre):

        tk.Label(self.ventana, text=texto, bg="#ebf5fb").pack()

        entry = tk.Entry(self.ventana)
        entry.pack(pady=2)

        setattr(self, nombre, entry)

    # guarda cliente
    def guardar(self):

        # obtiene datos
        n = self.nombres.get()
        c = self.cedula.get()
        ce = self.celular.get()
        co = self.correo.get()

        # valida datos
        val = self.sistema.validar_datos(n, c, ce, co)

        if val != "ok":
            messagebox.showerror("Error", "Datos inválidos")
            return

        # registra cliente
        res = self.sistema.registrar_cliente(n, c, ce, co)

        if res == "duplicado":
            messagebox.showerror("Error", "Cliente ya existe")
        else:
            messagebox.showinfo("OK", "Cliente registrado")
            self.ventana.destroy()


# -------------------------------
# 📌 CLIENTE AFILIADO
class AfiliadoCliente:

    def __init__(self, parent, sistema):
        self.sistema = sistema

        # ventana búsqueda
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("CLIENTE AFILIADO")
        self.ventana.geometry("300x200")
        self.ventana.configure(bg="#ebf5fb")

        # campo cédula
        tk.Label(self.ventana, text="Cédula", bg="#ebf5fb").pack()

        self.cedula = tk.Entry(self.ventana)
        self.cedula.pack()

        # botón buscar
        tk.Button(
            self.ventana,
            text="Buscar",
            bg="#85c1e9",
            command=self.buscar
        ).pack(pady=10)

    # busca cliente
    def buscar(self):

        cedula = self.cedula.get()

        cliente = self.sistema.buscar_afiliado(cedula)

        if cliente:
            messagebox.showinfo(
                "Cliente",
                f"{cliente['nombres']}\n{cliente['celular']}\n{cliente['correo']}"
            )
        else:
            messagebox.showerror("Error", "No encontrado")


# -------------------------------
# 📌 INICIO DEL PROGRAMA
if __name__ == "__main__":

    # crea sistema de clientes
    sistema = SistemaClientes()

    # abre login
    LoginWindow(sistema)
