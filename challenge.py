import pandas as pd
import matplotlib.pyplot as plt

# URLs de los archivos CSV
urls = {
    'Tienda 1': "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_1%20.csv",
    'Tienda 2': "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_2.csv",
    'Tienda 3': "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_3.csv",
    'Tienda 4': "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_4.csv"
}

# Cargar los archivos CSV en una lista de tuplas: (nombre, DataFrame)
tiendas = [(nombre, pd.read_csv(url)) for nombre, url in urls.items()]

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
