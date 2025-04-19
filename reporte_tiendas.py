
import matplotlib.pyplot as plt
import pandas as pd
import os
import webbrowser

# Crear carpeta para guardar imágenes
output_dir = "imagenes_reportes"
os.makedirs(output_dir, exist_ok=True)

# Simulación de datos (puedes reemplazar con tus propios DataFrames)
df_ingresos = pd.DataFrame({
    'Tienda': ['Tienda 1', 'Tienda 2', 'Tienda 3', 'Tienda 4'],
    'Ingreso': [15000, 22000, 18000, 20000]
})

df_calificaciones = pd.DataFrame({
    'Tienda': ['Tienda 1', 'Tienda 2', 'Tienda 3', 'Tienda 4'],
    'Calificación Promedio': [4.3, 3.8, 4.0, 4.5]
})

df_envio = pd.DataFrame({
    'Tienda': ['Tienda 1', 'Tienda 2', 'Tienda 3', 'Tienda 4'],
    'Costo Promedio Envío': [5.2, 6.1, 5.8, 4.9]
})

df_categorias = pd.DataFrame({
    'Tienda': ['Tienda 1'] * 3 + ['Tienda 2'] * 3,
    'Categoría del Producto': ['A', 'B', 'C', 'A', 'B', 'C'],
    'Cantidad': [100, 150, 90, 80, 200, 50]
})

# Función para guardar gráficos
def guardar_grafico(fig, nombre):
    path = os.path.join(output_dir, f"{nombre}.png")
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    return path

# Gráfico de ingresos
fig1, ax1 = plt.subplots()
ax1.bar(df_ingresos['Tienda'], df_ingresos['Ingreso'], color='teal')
ax1.set_title("Ingreso Total por Tienda")
ax1.set_ylabel("Ingreso")
img_ingresos = guardar_grafico(fig1, "ingresos")

# Gráfico de calificaciones
fig2, ax2 = plt.subplots()
ax2.bar(df_calificaciones['Tienda'], df_calificaciones['Calificación Promedio'], color='orange')
ax2.set_title("Calificación Promedio por Tienda")
ax2.set_ylabel("Calificación")
img_calificaciones = guardar_grafico(fig2, "calificaciones")

# Gráfico de envío
fig3, ax3 = plt.subplots()
ax3.bar(df_envio['Tienda'], df_envio['Costo Promedio Envío'], color='purple')
ax3.set_title("Costo de Envío Promedio por Tienda")
ax3.set_ylabel("Costo (USD)")
img_envio = guardar_grafico(fig3, "envio")

# Gráfico de productos por categoría
fig4, ax4 = plt.subplots(figsize=(8, 5))
for tienda in df_categorias['Tienda'].unique():
    sub_df = df_categorias[df_categorias['Tienda'] == tienda]
    ax4.bar(sub_df['Categoría del Producto'], sub_df['Cantidad'], label=tienda)
ax4.set_title("Productos Vendidos por Categoría y Tienda")
ax4.set_ylabel("Cantidad")
ax4.legend()
img_categorias = guardar_grafico(fig4, "categorias")

# Crear HTML
html_path = "reporte_tiendas.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write("<html><head><title>Reporte de Tiendas</title></head><body>")
    f.write("<h1>Reporte de Análisis de Tiendas</h1>")
    for title, img in [
        ("Ingreso Total por Tienda", img_ingresos),
        ("Calificación Promedio por Tienda", img_calificaciones),
        ("Costo de Envío Promedio por Tienda", img_envio),
        ("Productos Vendidos por Categoría y Tienda", img_categorias),
    ]:
        f.write(f"<h2>{title}</h2>")
        f.write(f'<img src="{img}" style="width:600px;"><br><br>')
    f.write("</body></html>")

# Abrir en el navegador
webbrowser.open_new_tab(html_path)
