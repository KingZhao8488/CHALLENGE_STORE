import pandas as pd
import matplotlib.pyplot as plt
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

# Cargar los archivos CSV
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
# INGRESOS POR TIENDA
# ------------------------

ingresos = []

for nombre, df in tiendas:
    if 'Precio' in df.columns:
        ingreso = df['Precio'].sum(min_count=1)  # min_count=1 para evitar 0 si todos son NaN
    else:
        ingreso = None
        print(f"[ADVERTENCIA] {nombre} no tiene la columna 'Precio'")
    ingresos.append({'Tienda': nombre, 'Ingreso': ingreso})

df_ingresos = pd.DataFrame(ingresos).sort_values(by='Ingreso', ascending=False)
print(" Ingresos por Tienda:")
print(df_ingresos)

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

print("\n Cantidad de productos vendidos por categoría:")
print(df_categorias)

# ------------------------
# CALIFICACIÓN PROMEDIO POR TIENDA
# ------------------------

calificaciones = []

for nombre, df in tiendas:
    if 'Calificación' in df.columns:
        promedio = df['Calificación'].mean()
    else:
        promedio = None
        print(f"[ADVERTENCIA] {nombre} no tiene la columna 'Calificación'")
    calificaciones.append({'Tienda': nombre, 'Calificación Promedio': promedio})

df_calificaciones = pd.DataFrame(calificaciones).sort_values(by='Calificación Promedio', ascending=False)

print("\n Calificación promedio por tienda:")
print(df_calificaciones)

# ------------------------
# PRODUCTOS MÁS Y MENOS VENDIDOS POR TIENDA
# ------------------------

print("\n Productos más y menos vendidos por tienda:")

for nombre, df in tiendas:
    print(f"\n {nombre}")
    
    if 'Producto' not in df.columns:
        print("   [ADVERTENCIA] No se encuentra la columna 'Producto'")
        continue

    conteo_productos = df['Producto'].value_counts()

    # Obtener el producto más vendido (pueden ser varios)
    max_ventas = conteo_productos.max()
    productos_mas_vendidos = conteo_productos[conteo_productos == max_ventas]

    # Obtener el producto menos vendido (pueden ser varios)
    min_ventas = conteo_productos.min()
    productos_menos_vendidos = conteo_productos[conteo_productos == min_ventas]

    print("Producto(s) más vendido(s):")
    for producto, cantidad in productos_mas_vendidos.items():
        print(f"      - {producto}: {cantidad} ventas")

    print("Producto(s) menos vendido(s):")
    for producto, cantidad in productos_menos_vendidos.items():
        print(f"      - {producto}: {cantidad} venta(s)")

# ------------------------
# COSTO DE ENVÍO PROMEDIO POR TIENDA
# ------------------------

costos_envio = []

for nombre, df in tiendas:
    if 'Costo de envío' in df.columns:
        promedio_envio = df['Costo de envío'].mean()
    else:
        promedio_envio = None
        print(f"[ADVERTENCIA] {nombre} no tiene la columna 'Costo de envío'")
    costos_envio.append({'Tienda': nombre, 'Costo de Envío Promedio': promedio_envio})

df_envios = pd.DataFrame(costos_envio).sort_values(by='Costo de Envío Promedio', ascending=True)

print("\n Costo de envío promedio por tienda:")
print(df_envios)


# ------------------------
# GRÁFICO 1: Ingreso total por tienda
# ------------------------
fig1, ax1 = plt.subplots()
ax1.bar(df_ingresos['Tienda'], df_ingresos['Ingreso'], color='teal')
ax1.set_title("Ingreso Total por Tienda")
ax1.set_ylabel("Ingreso")
img_ingresos = guardar_grafico(fig1, "ingresos")

# ------------------------
# GRÁFICO 2: Calificación promedio por tienda
# ------------------------
fig2, ax2 = plt.subplots()
ax2.bar(df_calificaciones['Tienda'], df_calificaciones['Calificación Promedio'], color='orange')
ax2.set_title("Calificación Promedio por Tienda")
ax2.set_ylabel("Calificación")
img_calificaciones = guardar_grafico(fig2, "calificaciones")

# ------------------------
# GRÁFICO 3: Costo de envío promedio por tienda
# ------------------------
fig3, ax3 = plt.subplots()
ax3.bar(df_envios['Tienda'], df_envios['Costo de Envío Promedio'], color='purple')
ax3.set_title("Costo de Envío Promedio por Tienda")
ax3.set_ylabel("Costo (USD)")
img_envio = guardar_grafico(fig3, "envio")

# ------------------------
# GRÁFICO 4: Productos vendidos por categoría y tienda
# ------------------------
fig4, ax4 = plt.subplots(figsize=(10, 6))
for tienda in df_categorias['Tienda'].unique():
    subset = df_categorias[df_categorias['Tienda'] == tienda]
    ax4.bar(subset['Categoría del Producto'], subset['Cantidad'], label=tienda)
ax4.set_title("Productos Vendidos por Categoría y Tienda")
ax4.set_ylabel("Cantidad")
ax4.set_xticklabels(subset['Categoría del Producto'], rotation=45, ha='right')
ax4.legend()
img_categorias = guardar_grafico(fig4, "categorias")

# ------------------------
# Crear archivo HTML con todos los gráficos
# ------------------------

# ------------------------
# Crear archivo HTML con diseño en modo oscuro y responsivo
# ------------------------

html_path = "reporte_tiendas.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write("""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Reporte de Tiendas</title>
    <style>
    :root {
        --floral-white: #fffcf2;
        --timberwolf: #ccc5b9;
        --black-olive: #403d39;
        --eerie-black: #252422;
        --flame: #eb5e28;
    }
    body {
        margin: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: var(--eerie-black);
        color: var(--floral-white);
        padding: 1rem;
        line-height: 1.6;
    }
    header {
        background-color: var(--black-olive);
        padding: 1rem;
        border-left: 5px solid var(--flame);
        margin-bottom: 2rem;
    }
    h1 {
        margin: 0;
        font-size: 2rem;
        color: var(--flame);
    }
    h2 {
        color: var(--flame);
        border-bottom: 2px solid var(--flame);
        padding-bottom: 0.3rem;
    }
    .seccion {
        background-color: var(--black-olive);
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        margin-bottom: 2rem;
    }
    img {
        max-width: 100%;
        height: auto;
        border: 2px solid var(--flame);
        border-radius: 8px;
        display: block;
        margin: 1rem auto;
    }
    footer {
        text-align: center;
        font-size: 0.9em;
        color: var(--timberwolf);
        margin-top: 40px;
        border-top: 1px solid var(--black-olive);
        padding-top: 10px;
    }
    </style>
</head>
<body>
    <header>
    <h1>Reporte de Análisis de Tiendas</h1>
    </header>
    <main>
""")

    for title, img in [
        ("Ingreso Total por Tienda", img_ingresos),
        ("Calificación Promedio por Tienda", img_calificaciones),
        ("Costo de Envío Promedio por Tienda", img_envio),
        ("Productos Vendidos por Categoría y Tienda", img_categorias),
    ]:
        f.write(f"""
    <section class="seccion">
        <h2>{title}</h2>
        <img src="{img}" alt="{title}">
    </section>
""")

    f.write(f"""
    </main>
    <footer>
    Andres Guerrero. Generado automáticamente con Python - {pd.Timestamp.today().strftime('%d/%m/%Y')}
    </footer>
</body>
</html>
""")

# Abrir en el navegador
webbrowser.open_new_tab(os.path.abspath(html_path))