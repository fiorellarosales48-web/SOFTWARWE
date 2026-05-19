# SOFTWARE - Sistema de Gestión de Clientes

Este proyecto es una aplicación desarrollada en Python utilizando **Programación Orientada a Objetos (POO)** y una interfaz gráfica con **Tkinter**.

---

## 📌 Descripción

El sistema permite la gestión completa de clientes mediante un inicio de sesión seguro y funcionalidades de registro, validación y búsqueda.

A lo largo del desarrollo, el sistema fue mejorado para incluir validaciones más realistas, estructura modular y manejo avanzado de datos.

---

## ⚙️ Funcionalidades

### 🔐 Sistema de login seguro
- Inicio de sesión con usuarios predefinidos
- Validación de contraseñas seguras
- Botón para mostrar/ocultar contraseña

### 👤 Registro de clientes
- Validación completa de datos personales
- Registro con:
  - Nombres completos
  - Cédula
  - Celular
  - Correo electrónico
- Evita registros duplicados

### 🌍 Validaciones avanzadas por país
- Cédula validada según país:
  - Ecuador 🇪🇨
  - Perú 🇵🇪
  - Colombia 🇨🇴
  - México 🇲🇽
  - España 🇪🇸

- Celular validado por:
  - longitud variable por país
  - prefijo obligatorio

### 📧 Validación de correo mejorada
- Validación de formato real
- Detección de errores comunes (ej: dominios mal escritos como “gamil”)
- Soporte para dominios reales:
  - gmail.com
  - hotmail.com
  - outlook.com
  - yahoo.com
  - dominios educativos y corporativos (.edu.ec, .com.ec, .es, etc.)

### 💾 Persistencia de datos
- Almacenamiento en archivo `.txt`
- Carga automática de clientes al iniciar el sistema

### 🔎 Búsqueda de clientes
- Búsqueda por número de cédula
- Visualización de datos del cliente

---

## 🧠 Mejoras implementadas en el sistema

- ✔ Validaciones más estrictas y realistas
- ✔ Validación de cédula por país
- ✔ Validación de celular según reglas internacionales
- ✔ Validación de correo más completa y flexible
- ✔ Mensajes de error específicos y detallados
- ✔ Separación modular del código (POO)
- ✔ Mejor experiencia de usuario en interfaz Tkinter

---

## 🛠 Tecnologías utilizadas

- Python 🐍
- Tkinter (interfaz gráfica)
- Expresiones regulares (re)
- Manejo de archivos (.txt)
- Programación Orientada a Objetos (POO)

---

## 📂 Estructura del proyecto

- Login del sistema
- Menú principal
- Registro de clientes
- Consulta de clientes afiliados

---

## 👨‍💻 Autor

Proyecto desarrollado como parte de la asignatura de **Ingeniería de Software**.

---

## 📌 Nota

Este sistema evolucionó desde una versión básica a una versión más avanzada con:
- validaciones por país
- control de errores detallado
- mejor estructura de código
- mayor realismo en datos ingresados
