import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
import os
import webbrowser

# Crear carpeta para guardar imágenes
output_dir = "imagenes_reportes"
os.makedirs(output_dir, exist_ok=True)

# Función para guardar gráficos
def guardar_grafico(fig, nombre):
    path = os.path.join(output_dir, f"{nombre}.png")
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    return path

# URLs de los archivos CSV
urls = {
    'Tienda 1': "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_1%20.csv",
    'Tienda 2': "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_2.csv",
    'Tienda 3': "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_3.csv",
    'Tienda 4': "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_4.csv"
}

# Cargar los archivos CSV en una lista de tuplas: (nombre, DataFrame)
tiendas = [(nombre, pd.read_csv(url)) for nombre, url in urls.items()]

# Ingresos
ingresos = [{'Tienda': nombre, 'Ingreso': df.get('Precio', pd.Series()).sum()} for nombre, df in tiendas]
df_ingresos = pd.DataFrame(ingresos).sort_values(by='Ingreso', ascending=False)

# Calificaciones
calificaciones = [{'Tienda': nombre, 'Calificación Promedio': df.get('Calificación', pd.Series()).mean()} for nombre, df in tiendas]
df_calificaciones = pd.DataFrame(calificaciones).sort_values(by='Calificación Promedio', ascending=False)

# Costo de Envío
costos_envio = [{'Tienda': nombre, 'Costo de Envío Promedio': df.get('Costo de envío', pd.Series()).mean()} for nombre, df in tiendas]
df_envios = pd.DataFrame(costos_envio).sort_values(by='Costo de Envío Promedio')

# ------------------------
# CANTIDAD DE PRODUCTOS VENDIDOS POR CATEGORÍA
# ------------------------
categorias_por_tienda = []
for nombre, df in tiendas:
    if 'Categoría del Producto' in df.columns:
        agrupado = df.groupby('Categoría del Producto').size().reset_index(name='Cantidad')
        agrupado['Tienda'] = nombre
        categorias_por_tienda.append(agrupado)
    else:
        print(f"[ADVERTENCIA] {nombre} no tiene la columna 'Categoría del Producto'")
df_categorias = pd.concat(categorias_por_tienda, ignore_index=True)
df_categorias = df_categorias.sort_values(by=['Tienda', 'Categoría del Producto'])

# ------------------------
# ANÁLISIS GEOGRÁFICO DE VENTAS
# ------------------------
df_geo = pd.concat([df.assign(Tienda=nombre) for nombre, df in tiendas], ignore_index=True)
df_geo = df_geo.dropna(subset=['lat', 'lon', 'Precio'])
df_geo['lat'] = df_geo['lat'].astype(float)
df_geo['lon'] = df_geo['lon'].astype(float)

# ------------------------
# Ventas totales y calificación promedio por tienda
# ------------------------
resumen_kpis = []
for nombre, df in tiendas:
    ventas = df['Precio'].sum()
    calif = df['Calificación'].mean()
    resumen_kpis.append({"Tienda": nombre, "Ventas Totales": ventas, "Calificación Promedio": round(calif, 2)})

df_kpis = pd.DataFrame(resumen_kpis).sort_values(by='Ventas Totales', ascending=False)

# Mostrar resumen de KPIs
print("\nResumen de KPIs por tienda:")
print(df_kpis)


# ------------------------
# GRÁFICOS ESTÁTICOS
# ------------------------
# 1. Ingresos - gráfico de líneas
fig1, ax1 = plt.subplots()
ax1.plot(df_ingresos['Tienda'], df_ingresos['Ingreso'], marker='o', linestyle='-', color='teal')
ax1.set_title("Ingreso Total por Tienda")
ax1.set_ylabel("Ingreso")
img_ingresos = guardar_grafico(fig1, "ingresos")

# 2. Calificaciones - gráfico de áreas
fig2, ax2 = plt.subplots()
ax2.fill_between(df_calificaciones['Tienda'], df_calificaciones['Calificación Promedio'], color='orange', alpha=0.6)
ax2.plot(df_calificaciones['Tienda'], df_calificaciones['Calificación Promedio'], marker='o', color='orange')
ax2.set_title("Calificación Promedio por Tienda")
ax2.set_ylabel("Calificación")
img_calificaciones = guardar_grafico(fig2, "calificaciones")

# 3. Costos de envío - gráfico horizontal
fig3, ax3 = plt.subplots()
ax3.barh(df_envios['Tienda'], df_envios['Costo de Envío Promedio'], color='purple')
ax3.set_title("Costo de Envío Promedio por Tienda")
ax3.set_xlabel("Costo (USD)")
img_envio = guardar_grafico(fig3, "envio")

# 4. Productos por categoría - gráfico de pastel por tienda
fig4, ax4 = plt.subplots()
categoria_sample = df_categorias[df_categorias['Tienda'] == df_categorias['Tienda'].unique()[0]]
ax4.pie(categoria_sample['Cantidad'], labels=categoria_sample['Categoría del Producto'], autopct='%1.1f%%', startangle=90)
ax4.set_title(f"Distribución por Categoría - {categoria_sample['Tienda'].values[0]}")
img_categorias = guardar_grafico(fig4, "categorias")

# 5. Gráfico de Dispersión Geográfica
fig_geo, ax_geo = plt.subplots(figsize=(10, 6))
scatter = ax_geo.scatter(df_geo['lon'], df_geo['lat'], c=df_geo['Precio'], cmap='plasma', alpha=0.6)
plt.colorbar(scatter, ax=ax_geo, label='Precio de Venta')
ax_geo.set_title("Distribución Geográfica de Ventas")
ax_geo.set_xlabel("Longitud")
ax_geo.set_ylabel("Latitud")
img_geo_scatter = guardar_grafico(fig_geo, "distribucion_geografica")

# Mapa interactivo con Folium
lat_center = df_geo['lat'].mean()
lon_center = df_geo['lon'].mean()
mapa = folium.Map(location=[lat_center, lon_center], zoom_start=6, tiles='CartoDB dark_matter')
heat_data = [[row['lat'], row['lon'], row['Precio']] for idx, row in df_geo.iterrows()]
HeatMap(heat_data, radius=10).add_to(mapa)
mapa_path = os.path.join(output_dir, "mapa_interactivo.html")
mapa.save(mapa_path)

# HTML export
html_path = "reporte_dashboard.html"
html_content = f"""
<!DOCTYPE html>
<html lang='es'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <meta author='Andres Guerrero'>
    <title>Dashboard - Análisis de Tiendas</title>
    <style>
    :root {{
        --floral-white: #fffcf2;
        --timberwolf: #ccc5b9;
        --black-olive: #403d39;
        --eerie-black: #252422;
        --flame: #eb5e28;
    }}
    body {{
        margin: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: var(--eerie-black);
        color: var(--floral-white);
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }}
    header {{
        background-color: var(--black-olive);
        padding: 1rem;
        border-bottom: 4px solid var(--flame);
        text-align: left;
    }}
    header h1 {{
        margin: 0;
        font-size: 2rem;
        color: var(--floral-white);
    }}
    .kpi-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
    }}
    .kpi-card {{
        background-color: #403d39;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
    }}
    .kpi-title {{
        color: #ccc5b9;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }}
    .kpi-value {{
        color: #eb5e28;
        font-size: 1.6rem;
        font-weight: bold;
    }}
    main {{
        padding: 1rem;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
    }}
    .card {{
        background-color: var(--black-olive);
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    }}
    .card h2 {{
        color: var(--flame);
        font-size: 1.2rem;
        margin-top: 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid var(--timberwolf);
        padding-bottom: 0.5rem;
    }}
    .card img {{
        width: 100%;
        border-radius: 5px;
        border: 2px solid var(--flame);
    }}
    .map-button {{
        display: block;
        margin-top: 1rem;
        background-color: var(--flame);
        color: white;
        padding: 0.5rem 1rem;
        text-align: center;
        border-radius: 5px;
        text-decoration: none;
    }}
    footer {{
        background-color: var(--black-olive);
        color: var(--timberwolf);
        text-align: center;
        padding: 1rem;
        margin-top: auto;
    }}
    </style>
</head>
<body>
    <header>
    <h1>Dashboard de Análisis de Tiendas</h1>
    </header>
    <main>
    <div class='kpi-container'>
"""

# Añadir tarjetas de KPIs
for _, row in df_kpis.iterrows():
    html_content += f"""
    <div class='kpi-card'>
        <div class='kpi-title'>{row['Tienda']}</div>
        <div class='kpi-value'>Ventas: ${row['Ventas Totales']:.2f}</div>
        <div class='kpi-value'>Calificación: {row['Calificación Promedio']}</div>
    </div>
    """

html_content += """
    </div>
    <div class='card'>
        <h2>Ingreso Total por Tienda</h2>
        <img src='{img_ingresos}' alt='Ingresos'>
    </div>
    <div class='card'>
        <h2>Calificación Promedio por Tienda</h2>
        <img src='{img_calificaciones}' alt='Calificaciones'>
    </div>
    <div class='card'>
        <h2>Costo de Envío Promedio por Tienda</h2>
        <img src='{img_envio}' alt='Costo de Envío'>
    </div>
    <div class='card'>
        <h2>Productos por Categoría</h2>
        <img src='{img_categorias}' alt='Categorías'>
    </div>
    <div class='card'>
        <h2>Distribución Geográfica</h2>
        <img src='{img_geo_scatter}' alt='Mapa Geográfico'>
        <a href='{mapa_path}' class='map-button' target='_blank'>Ver Mapa Interactivo</a>
    </div>
    </main>
    <footer>
    Creado por Andres Guerrero. Reporte generado automáticamente con Python - Abril 2025
    </footer>
</body>

</html>
"""

# Escribir HTML
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

# Abrir en navegador
webbrowser.open(f"file://{os.path.abspath(html_path)}")