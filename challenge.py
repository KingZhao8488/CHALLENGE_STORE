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

print("\n🔹 Calificación promedio por tienda:")
print(df_calificaciones)
