# PROYECTO-PROGRAMACION-AVANZADA
PROGRAMACION AVANZADA PROYECTO: APLICACIÓN DE REGISTRO PARA UN PROGRAMA DE DONACIÓN DE SANGRE

Sistema de Gestión para Banco de Sangre
Este es un proyecto individual desarrollado para la materia de Programación Orientada a Objetos (POO). Consiste en una aplicación de escritorio diseñada para optimizar, automatizar y digitalizar el control de inventario, registro de donantes y análisis estadístico en un banco de sangre, eliminando la necesidad de registros manuales tradicionales.

Características Principales
-Gestión y Registro de Donantes: Registro validado de información crítica (Nombre, Edad, Contacto y Grupo Sanguíneo). El sistema calcula la fecha de donación automáticamente.
-Búsqueda Avanzada: Filtros optimizados mediante la librería Pandas para realizar búsquedas cruzadas por tipo de sangre y fechas específicas.
-Sistema de Alertas Críticas: Monitorización activa del stock. La aplicación emite una alerta visual si las unidades de cualquier tipo de sangre caen por debajo del límite de seguridad ($< 3$ unidades).
-Reportes en Tiempo Real: Identificación automatizada de los donantes más frecuentes ("Top 3") para campañas de fidelización.
-Analítica Visual Integrada: Generación dinámica de gráficos de pastel (distribución del inventario) y de líneas (tendencia de donaciones en el tiempo) utilizando Matplotlib.

Tecnologías y Herramientas 
-UtilizadasLenguaje: Python 3.12+
-Paradigma: Programación Orientada a Objetos (POO)
-Interfaz Gráfica (GUI): Tkinter (ttk.Notebook para diseño modular por pestañas)
-Procesamiento de Datos: Pandas
-Visualización Estadística: Matplotlib
-Persistencia de Datos: Archivos de valores separados por comas (CSV) como base de datos local y portátil.
-IDE: Visual Studio (Última versión)

Arquitectura del Software (Clases)
El proyecto sigue una estructura modular acoplada mediante relaciones UML de asociación, composición y dependencia
-Donante: Clase entidad encargada de modelar el objeto del donante y sus atributos encapsulados.
-GestorArchivos: Clase encargada de la persistencia de datos (lectura y escritura del archivo CSV).
-Inventario: Clase de lógica de negocio dedicada a las búsquedas avanzadas, control de stock y cálculo de alertas.
-AnalisisEstadistico: Clase analítica que transforma los DataFrames de Pandas en componentes visuales de Matplotlib.
-InterfazApp: Clase controladora principal que hereda de Tkinter y orquesta la experiencia del usuario.
