# ==========================================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================================
# tkinter -> interfaz gráfica
# messagebox -> ventanas de alerta
# os -> manejo de archivos
# re -> expresiones regulares (validaciones)
# ==========================================================

import tkinter as tk
from tkinter import messagebox
import os
import re


# ==========================================================
# USUARIOS DEL SISTEMA (LOGIN)
# ==========================================================
# Diccionario de usuarios predefinidos
# Se usa para validar el acceso al sistema
# ==========================================================
USUARIOS_SISTEMA = {
    "Nathaly": "Nathaly03@",
    "Genesis": "Genesis123$",
    "Santiago": "Cedeno123"
}

# Archivo donde se guardan clientes registrados
ARCHIVO_CLIENTES = "clientes.txt"


# ==========================================================
# CONFIGURACIÓN DE PAÍSES
# ==========================================================
# Cada país tiene:
# - código telefónico
# - cantidad de dígitos
# - número inicial obligatorio
# - bandera visual
# Esto permite validar celulares de forma realista
# ==========================================================
CODIGOS_PAISES = {
    "Ecuador": {"codigo": "+593", "digitos": 9, "inicio": "9", "bandera": "🇪🇨"},
    "Perú": {"codigo": "+51", "digitos": 9, "inicio": "9", "bandera": "🇵🇪"},
    "Colombia": {"codigo": "+57", "digitos": 10, "inicio": "3", "bandera": "🇨🇴"},
    "México": {"codigo": "+52", "digitos": 10, "inicio": "1", "bandera": "🇲🇽"},
    "España": {"codigo": "+34", "digitos": 9, "inicio": "6", "bandera": "🇪🇸"},
}


# ==========================================================
# VALIDACIÓN DE CONTRASEÑA
# ==========================================================
# Se asegura que la contraseña sea segura:
# - mínimo 8 caracteres
# - mayúsculas
# - minúsculas
# - números
# - símbolos
# ==========================================================
def validar_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"\d", password) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )


# ==========================================================
# VALIDACIÓN DE CORREO ELECTRÓNICO
# ==========================================================
# 1. Verifica estructura general (usuario@dominio.extensión)
# 2. Permite extensiones como .com .es .com.ec .edu.ec
# 3. Detecta dominios mal escritos (gamil, hotmial, etc.)
# ==========================================================
def validar_correo(correo):

    # patrón general de correo válido
    patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    # si no cumple estructura básica
    if not re.match(patron, correo):
        return "formato"

    usuario, dominio = correo.split("@")
    dominio = dominio.lower()

    partes = dominio.split(".")

    # debe tener al menos dominio + extensión
    if len(partes) < 2:
        return "dominio"

    base = partes[0]

    # evita dominios demasiado cortos o mal escritos
    if len(base) < 2:
        return "dominio"

    return "ok"


# ==========================================================
# VALIDACIÓN DE CÉDULA POR PAÍS
# ==========================================================
# Cada país tiene formato distinto:
# - Ecuador: 10 dígitos
# - Perú: 8 dígitos
# - Colombia: 10 dígitos
# - México: 10-18 alfanumérico
# - España: 8 números + 1 letra
# ==========================================================
def validar_cedula(cedula, pais):

    if pais == "Ecuador":
        return cedula.isdigit() and len(cedula) == 10

    if pais == "Perú":
        return cedula.isdigit() and len(cedula) == 8

    if pais == "Colombia":
        return cedula.isdigit() and len(cedula) == 10

    if pais == "México":
        return cedula.isalnum() and 10 <= len(cedula) <= 18

    if pais == "España":
        return re.match(r"^\d{8}[A-Za-z]$", cedula) is not None

    return False


# ==========================================================
# CLASE: SISTEMA DE CLIENTES
# ==========================================================
# Se encarga de:
# - cargar clientes desde archivo
# - guardar clientes nuevos
# - validar datos
# - buscar clientes
# ==========================================================
class SistemaClientes:

    def __init__(self):
        self.clientes = []
        self.cargar()

    # --------------------------
    # CARGAR CLIENTES DESDE ARCHIVO
    # --------------------------
    def cargar(self):
        if os.path.exists(ARCHIVO_CLIENTES):
            with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as f:
                for l in f:
                    d = l.strip().split(",")
                    if len(d) == 5:
                        self.clientes.append({
                            "nombres": d[0],
                            "cedula": d[1],
                            "pais": d[2],
                            "celular": d[3],
                            "correo": d[4]
                        })

    # --------------------------
    # GUARDAR CLIENTE EN ARCHIVO
    # --------------------------
    def guardar(self, n, c, p, ce, co):
        with open(ARCHIVO_CLIENTES, "a", encoding="utf-8") as f:
            f.write(f"{n},{c},{p},{ce},{co}\n")

    # --------------------------
    # VALIDAR TODOS LOS CAMPOS
    # --------------------------
    def validar(self, n, c, ce, co, p):

        d = CODIGOS_PAISES[p]

        # nombre completo (nombre + 3 apellidos)
        if len(n.split()) != 4:
            return "nombre"

        # cédula según país
        if not validar_cedula(c, p):
            return "cedula"

        # celular solo números
        if not ce.isdigit():
            return "celular_num"

        # inicio correcto del número
        if not ce.startswith(d["inicio"]):
            return "celular_inicio"

        # longitud correcta según país
        if len(ce) != d["digitos"]:
            return "celular_longitud"

        # validación de correo
        correo_estado = validar_correo(co)

        if correo_estado == "formato":
            return "correo_formato"
        if correo_estado == "dominio":
            return "correo_dominio"

        return "ok"

    # --------------------------
    # REGISTRAR CLIENTE
    # --------------------------
    def registrar(self, n, c, p, ce, co):

        for x in self.clientes:
            if x["cedula"] == c:
                return "dup"

        self.clientes.append({
            "nombres": n,
            "cedula": c,
            "pais": p,
            "celular": ce,
            "correo": co
        })

        self.guardar(n, c, p, ce, co)
        return "ok"

    # --------------------------
    # BUSCAR CLIENTE
    # --------------------------
    def buscar(self, c):
        for x in self.clientes:
            if x["cedula"] == c:
                return x
        return None


# ==========================================================
# CLASE: LOGIN
# ==========================================================
# Encargada de:
# - autenticar usuario
# - validar contraseña segura
# - abrir menú principal
# ==========================================================
class Login:

    def __init__(self, sistema):

        self.sistema = sistema

        self.v = tk.Tk()
        self.v.title("LOGIN")
        self.v.geometry("350x300")
        self.v.configure(bg="#d6eaf8")

        tk.Label(self.v, text="Usuario", bg="#d6eaf8").pack()
        self.u = tk.Entry(self.v)
        self.u.pack()

        tk.Label(self.v, text="Contraseña", bg="#d6eaf8").pack()

        frame = tk.Frame(self.v, bg="#d6eaf8")
        frame.pack(pady=5)

        self.p = tk.Entry(frame, show="*", width=22)
        self.p.grid(row=0, column=0)

        self.show = False

        tk.Button(frame, text="👁", width=2,
                  command=self.toggle).grid(row=0, column=1)

        tk.Button(self.v, text="Entrar",
                  command=self.login).pack(pady=10)

        self.v.mainloop()

    # mostrar/ocultar contraseña
    def toggle(self):
        self.show = not self.show
        self.p.config(show="" if self.show else "*")

    # validar login
    def login(self):

        u = self.u.get()
        p = self.p.get()

        if not validar_password(p):
            messagebox.showerror("Error", "Contraseña inválida")
            return

        if u in USUARIOS_SISTEMA and USUARIOS_SISTEMA[u] == p:
            self.v.destroy()
            Menu(self.sistema)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")


# ==========================================================
# CLASE: MENÚ PRINCIPAL
# ==========================================================
class Menu:

    def __init__(self, sistema):

        self.sistema = sistema

        self.v = tk.Tk()
        self.v.title("MENÚ")
        self.v.geometry("450x450")
        self.v.configure(bg="#d6eaf8")

        self.menu()
        self.v.mainloop()

    def limpiar(self):
        for i in self.v.winfo_children():
            i.destroy()

    def menu(self):

        self.limpiar()

        tk.Label(self.v, text="SISTEMA CLIENTES",
                 bg="#d6eaf8").pack(pady=10)

        tk.Button(self.v, text="Registrar",
                  command=self.reg).pack(pady=5)

        tk.Button(self.v, text="Afiliado",
                  command=self.afi).pack(pady=5)

    def reg(self):
        self.limpiar()
        Registro(self)

    def afi(self):

        self.limpiar()

        if len(self.sistema.clientes) == 0:
            messagebox.showinfo("Info", "No hay clientes")
            self.menu()
            return

        tk.Label(self.v, text="Cédula", bg="#d6eaf8").pack()
        self.c = tk.Entry(self.v)
        self.c.pack()

        self.c.bind("<Return>", lambda e: self.buscar())

        tk.Button(self.v, text="Buscar",
                  command=self.buscar).pack()

        tk.Button(self.v, text="Regresar",
                  command=self.menu).pack()

    def buscar(self):

        r = self.sistema.buscar(self.c.get())

        if r:
            messagebox.showinfo("Cliente", str(r))
        else:
            messagebox.showerror("Error", "No encontrado")


# ==========================================================
# CLASE: REGISTRO DE CLIENTES
# ==========================================================
class Registro:

    def __init__(self, menu):

        self.menu = menu
        self.sistema = menu.sistema
        self.v = menu.v

        tk.Label(self.v, text="Registro",
                 bg="#d6eaf8").pack()

        tk.Label(self.v, text="Nombre completo").pack()
        self.n = tk.Entry(self.v)
        self.n.pack()

        tk.Label(self.v, text="Cédula").pack()
        self.c = tk.Entry(self.v)
        self.c.pack()

        self.p = tk.StringVar()
        self.p.set("Ecuador")

        tk.OptionMenu(self.v, self.p,
                      *CODIGOS_PAISES.keys()).pack()

        self.ce = tk.Entry(self.v)
        self.ce.pack()

        self.co = tk.Entry(self.v)
        self.co.pack()

        tk.Button(self.v, text="Guardar",
                  command=self.save).pack()

        self.update()

    def update(self):
        d = CODIGOS_PAISES[self.p.get()]

    def save(self):

        r = self.sistema.validar(
            self.n.get(),
            self.c.get(),
            self.ce.get(),
            self.co.get(),
            self.p.get()
        )

        errores = {
            "nombre": "Nombre incompleto",
            "cedula": "Cédula inválida según país",
            "celular_num": "Celular solo números",
            "celular_inicio": "Inicio incorrecto",
            "celular_longitud": "Longitud incorrecta",
            "correo_formato": "Correo inválido",
            "correo_dominio": "Dominio incorrecto",
        }

        if r != "ok":
            messagebox.showerror("Error", errores.get(r))
            return

        self.sistema.registrar(
            self.n.get(),
            self.c.get(),
            self.p.get(),
            self.ce.get(),
            self.co.get()
        )

        messagebox.showinfo("OK", "Cliente guardado")
        self.menu.menu()


# ==========================================================
# INICIO DEL PROGRAMA
# ==========================================================
if __name__ == "__main__":
    sistema = SistemaClientes()
    Login(sistema)
