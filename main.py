import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import os

# ==========================================
# 1. CLASE ENTIDAD (DONANTE)
# ==========================================
class Donante:
    def __init__(self, nombre, tipo_sangre, edad, contacto):
        self.nombre = nombre
        self.tipo_sangre = tipo_sangre
        self.edad = edad
        self.contacto = contacto
        self.fecha_donacion = datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "Nombre": self.nombre,
            "Tipo_Sangre": self.tipo_sangre,
            "Edad": self.edad,
            "Contacto": self.contacto,
            "Fecha_Donacion": self.fecha_donacion
        }

# ==========================================
# 2. CLASE GESTOR DE ARCHIVOS
# ==========================================
class GestorArchivos:
    def __init__(self, archivo="donantes_db.csv"):
        self.archivo = archivo
        self._inicializar_archivo()

    def _inicializar_archivo(self):
        if not os.path.exists(self.archivo):
            df = pd.DataFrame(columns=["Nombre", "Tipo_Sangre", "Edad", "Contacto", "Fecha_Donacion"])
            df.to_csv(self.archivo, index=False)

    def guardar_donante(self, donante):
        df = pd.DataFrame([donante.to_dict()])
        df.to_csv(self.archivo, mode='a', header=False, index=False)

    def obtener_datos(self):
        return pd.read_csv(self.archivo)

# ==========================================
# 3. CLASE INVENTARIO, BÚSQUEDAS Y REPORTES
# ==========================================
class Inventario:
    def __init__(self, gestor_archivos):
        self.gestor = gestor_archivos
        self.limite_seguridad = 3

    def buscar_avanzada(self, tipo=None, fecha=None):
        """Filtra el DataFrame según los criterios dados"""
        df = self.gestor.obtener_datos()
        if df.empty: return df
        
        if tipo:
            df = df[df['Tipo_Sangre'] == tipo]
        if fecha:
            df = df[df['Fecha_Donacion'].str.contains(fecha, na=False)]
        return df

    def verificar_alertas(self):
        df = self.gestor.obtener_datos()
        if df.empty: return []
        
        stock = df['Tipo_Sangre'].value_counts()
        alertas = []
        tipos_validos = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        
        for tipo in tipos_validos:
            cantidad = stock.get(tipo, 0)
            if cantidad < self.limite_seguridad:
                alertas.append(f"⚠️ {tipo}: Nivel crítico ({cantidad} unid.)")
        return alertas

    def obtener_donantes_frecuentes(self):
        """Retorna los nombres de las personas con más donaciones"""
        df = self.gestor.obtener_datos()
        if df.empty: return "Sin datos aún."
        frecuentes = df['Nombre'].value_counts().head(3) # Top 3
        texto = ""
        for nombre, cantidad in frecuentes.items():
            texto += f"• {nombre}: {cantidad} donación(es)\n"
        return texto

# ==========================================
# 4. CLASE ANÁLISIS ESTADÍSTICO
# ==========================================
class AnalisisEstadistico:
    def __init__(self, gestor_archivos):
        self.gestor = gestor_archivos

    def graficar_distribucion(self, frame):
        for widget in frame.winfo_children(): widget.destroy()
        df = self.gestor.obtener_datos()
        if df.empty: return

        conteo = df['Tipo_Sangre'].value_counts()
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(conteo, labels=conteo.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)
        ax.set_title("Inventario por Tipo")

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def graficar_tendencia(self, frame):
        for widget in frame.winfo_children(): widget.destroy()
        df = self.gestor.obtener_datos()
        if df.empty: return

        # Agrupar por fecha para ver tendencia
        tendencia = df.groupby('Fecha_Donacion').size()
        fig, ax = plt.subplots(figsize=(5, 4))
        tendencia.plot(kind='line', marker='o', ax=ax, color='#D32F2F')
        
        ax.set_title("Tendencia de Donaciones en el Tiempo")
        ax.set_ylabel("Cantidad de Donaciones")
        ax.set_xlabel("Fecha")
        ax.grid(True, linestyle='--', alpha=0.6)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# ==========================================
# 5. CLASE INTERFAZ (CONTROLADOR GUI)
# ==========================================
class InterfazApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Banco de Sangre - Sistema de Gestión")
        self.geometry("900x650")
        
        self.gestor = GestorArchivos()
        self.inventario = Inventario(self.gestor)
        self.estadistica = AnalisisEstadistico(self.gestor)

        self._crear_widgets()

    def _crear_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.tab_registro = ttk.Frame(self.notebook)
        self.tab_datos = ttk.Frame(self.notebook)
        self.tab_graficos = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_registro, text="📝 Registro")
        self.notebook.add(self.tab_datos, text="🗃️ Búsqueda y Reportes")
        self.notebook.add(self.tab_graficos, text="📊 Análisis")

        self._construir_tab_registro()
        self._construir_tab_datos()
        self._construir_tab_graficos()

        self.notebook.bind("<<NotebookTabChanged>>", self._actualizar_interfaz)

    def _construir_tab_registro(self):
        frame_form = tk.Frame(self.tab_registro, pady=40)
        frame_form.pack()

        tk.Label(frame_form, text="Nombre Completo:", font=("Arial", 11)).grid(row=0, column=0, pady=10, sticky="e")
        self.ent_nombre = tk.Entry(frame_form, width=35, font=("Arial", 11))
        self.ent_nombre.grid(row=0, column=1, pady=10)

        tk.Label(frame_form, text="Tipo de Sangre:", font=("Arial", 11)).grid(row=1, column=0, pady=10, sticky="e")
        self.cb_tipo = ttk.Combobox(frame_form, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], state="readonly", width=33)
        self.cb_tipo.grid(row=1, column=1, pady=10)

        tk.Label(frame_form, text="Edad:", font=("Arial", 11)).grid(row=2, column=0, pady=10, sticky="e")
        self.ent_edad = tk.Entry(frame_form, width=35, font=("Arial", 11))
        self.ent_edad.grid(row=2, column=1, pady=10)

        tk.Label(frame_form, text="Contacto (Tel/Email):", font=("Arial", 11)).grid(row=3, column=0, pady=10, sticky="e")
        self.ent_contacto = tk.Entry(frame_form, width=35, font=("Arial", 11))
        self.ent_contacto.grid(row=3, column=1, pady=10)

        btn_guardar = tk.Button(frame_form, text="Guardar Registro", bg="#8B0000", fg="white", font=("Arial", 11, "bold"), command=self.registrar_donacion)
        btn_guardar.grid(row=4, columnspan=2, pady=30, ipadx=20, ipady=5)

    def registrar_donacion(self):
        nombre, tipo, edad, contacto = self.ent_nombre.get(), self.cb_tipo.get(), self.ent_edad.get(), self.ent_contacto.get()
        if not all([nombre, tipo, edad, contacto]):
            messagebox.showwarning("Error", "Llena todos los campos.")
            return

        nuevo_donante = Donante(nombre, tipo, edad, contacto)
        self.gestor.guardar_donante(nuevo_donante)
        messagebox.showinfo("Éxito", "Registrado correctamente.")
        
        self.ent_nombre.delete(0, tk.END)
        self.cb_tipo.set('')
        self.ent_edad.delete(0, tk.END)
        self.ent_contacto.delete(0, tk.END)

    def _construir_tab_datos(self):
        # Frame superior: Buscador
        frame_busqueda = tk.LabelFrame(self.tab_datos, text="Búsqueda Avanzada", padx=10, pady=10)
        frame_busqueda.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_busqueda, text="Tipo Sangre:").grid(row=0, column=0, padx=5)
        self.cb_busqueda_tipo = ttk.Combobox(frame_busqueda, values=["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], state="readonly", width=10)
        self.cb_busqueda_tipo.grid(row=0, column=1, padx=5)

        tk.Label(frame_busqueda, text="Fecha (YYYY-MM-DD):").grid(row=0, column=2, padx=5)
        self.ent_busqueda_fecha = tk.Entry(frame_busqueda, width=15)
        self.ent_busqueda_fecha.grid(row=0, column=3, padx=5)

        tk.Button(frame_busqueda, text="Buscar", command=self.ejecutar_busqueda, bg="#e0e0e0").grid(row=0, column=4, padx=10)
        tk.Button(frame_busqueda, text="Limpiar Filtros", command=lambda: self._cargar_tabla(self.gestor.obtener_datos())).grid(row=0, column=5)

        # Frame central: Tabla
        columnas = ("Nombre", "Tipo_Sangre", "Edad", "Contacto", "Fecha_Donacion")
        self.tree = ttk.Treeview(self.tab_datos, columns=columnas, show="headings", height=8)
        for col in columnas:
            self.tree.heading(col, text=col.replace("_", " "))
            self.tree.column(col, anchor="center")
        self.tree.pack(expand=True, fill='both', padx=20, pady=5)

        # Frame inferior: Reportes y Alertas
        frame_reportes = tk.Frame(self.tab_datos)
        frame_reportes.pack(fill="x", padx=20, pady=5)

        self.lbl_alertas = tk.Label(frame_reportes, fg="#D32F2F", font=("Arial", 10, "bold"), justify="left")
        self.lbl_alertas.pack(side="left", padx=10)

        self.lbl_frecuentes = tk.Label(frame_reportes, fg="#004D40", font=("Arial", 10, "bold"), justify="left")
        self.lbl_frecuentes.pack(side="right", padx=10)

    def ejecutar_busqueda(self):
        tipo = self.cb_busqueda_tipo.get()
        fecha = self.ent_busqueda_fecha.get()
        df_filtrado = self.inventario.buscar_avanzada(tipo, fecha)
        self._cargar_tabla(df_filtrado)

    def _cargar_tabla(self, df):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    def _construir_tab_graficos(self):
        # Dividir pestaña en dos columnas
        self.frame_pie = tk.Frame(self.tab_graficos)
        self.frame_pie.pack(side="left", expand=True, fill='both', padx=10, pady=10)

        self.frame_line = tk.Frame(self.tab_graficos)
        self.frame_line.pack(side="right", expand=True, fill='both', padx=10, pady=10)

    def _actualizar_interfaz(self, event):
        # Refrescar datos
        df = self.gestor.obtener_datos()
        self._cargar_tabla(df)

        # Actualizar Alertas
        alertas = self.inventario.verificar_alertas()
        if alertas:
            self.lbl_alertas.config(text="⚠️ ALERTAS DE STOCK:\n" + "\n".join(alertas))
        else:
            self.lbl_alertas.config(text="✅ Inventario Saludable.", fg="green")

        # Actualizar Frecuentes
        frecuentes = self.inventario.obtener_donantes_frecuentes()
        self.lbl_frecuentes.config(text="🏆 DONANTES MÁS FRECUENTES:\n" + frecuentes)

        # Actualizar Gráficos (Distribución y Tendencia)
        self.estadistica.graficar_distribucion(self.frame_pie)
        self.estadistica.graficar_tendencia(self.frame_line)

if __name__ == "__main__":
    app = InterfazApp()
    app.mainloop()