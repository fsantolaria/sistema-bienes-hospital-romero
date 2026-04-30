# ✅ Carpeta QA – Sistema de Bienes Patrimoniales (Hospital Melchor Romero)

Este archivo documenta todo el trabajo realizado desde el área de **Quality Assurance (QA)** dentro del proyecto. Aquí se explica la estructura de carpetas, el objetivo del área, las actividades realizadas, resultados y responsables.

---

## 📂 Estructura de la carpeta QA

sistema-bienes-hospital-romero/
├── QA_Documentos/ → Informes QA (Word, PDF, etc.)
├── QA_Evidencias/ → Capturas de pantalla, gráficos y pruebas realizadas
├── README_QA.md → Este archivo (índice y documentación del área QA)

---

## 🎯 Objetivo del área QA

Garantizar que el sistema funcione sin errores críticos, cumpla con los requerimientos funcionales establecidos por los analistas, y ofrezca una experiencia correcta para el usuario final.

---

## ✅ Actividades realizadas por QA

- Análisis de los casos de uso (Alta, Baja, Modificación, Login, etc.)
- Diseño de **casos de prueba positivos y negativos**
- Ejecución de pruebas manuales en entorno local
- Registro de **resultados y evidencias** (capturas, errores, mensajes del sistema)
- Reporte de errores a Backend o Frontend según corresponda
- Repruebas después de las correcciones
- Elaboración del **Informe QA** (Word) y generación de gráficos técnicos

---

## 📊 Resultados generales

| Estado del Caso de Prueba | Cantidad |
|---------------------------|----------|
| Casos ejecutados          | 13       |
| Aprobados                 | 8        |
| Fallo parcial             | 4        |
| No aprobados              | 1        |

📁 Gráfico generado:  
`QA_Evidencias/grafico_casos_prueba.png`

---

## 📌 Criterios de Aceptación (generales)

- El sistema debe permitir acceso solo con credenciales válidas.  
- Los campos obligatorios deben estar completos y con el formato correcto.  
- Si se ingresan datos incorrectos (ej: letras en precio), el sistema debe mostrar un mensaje de error.  
- No debe permitir guardar un bien sin completar los datos obligatorios.  
- La baja de un bien debe solicitar **motivo y confirmación** antes de registrarse.  
- Los cambios realizados en una modificación deben reflejarse correctamente.  
- Los usuarios solo pueden acceder a las funciones que correspondan a su rol (Administrador u Operador).

---

## 👥 Equipo de QA

| Nombre               | Rol |
|----------------------|-----|
| Milagros Mantilla    | QA  |
| Beatriz Romero       | QA  |

---

Este archivo tiene como objetivo documentar y facilitar la comprensión del trabajo realizado desde QA, para docentes, compañeros o cualquier integrante del proyecto.

