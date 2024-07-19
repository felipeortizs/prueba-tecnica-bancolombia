import pandas as pd

# Ruta del archivo XLSX
ruta_archivo= r"C:\Users\jufeorti\Documents\Automatizaciones\Ecosistemas\Datos\Obligaciones_clientes.xlsx"
ruta_archivo2= r"C:\Users\jufeorti\Documents\Automatizaciones\Ecosistemas\Datos\tasas_productos.xlsx"

# Ruta de los archivos de salida
#ruta_salida_merged = r"C:\Users\jufeorti\Documents\Automatizaciones\Ecosistemas\Resultados\obligaciones_con_tasas.xlsx"
#ruta_salida_final = r"C:\Users\jufeorti\Documents\Automatizaciones\Ecosistemas\Resultados\clientes_con_multiples_productos.xlsx"


# Cargar los archivos XLSX de ruta especifica
obligaciones_clientes = pd.read_excel(ruta_archivo, engine='openpyxl', sheet_name='Obligaciones_clientes')
tasas_productos = pd.read_excel(ruta_archivo2, engine='openpyxl', sheet_name='Tasas')

# Función para extraer el nombre del producto
def extraer_nombre_producto(id_producto):
    if ' - ' in id_producto:
        partes = id_producto.split(' - ')
        if len(partes) > 1:
            producto = partes[1]
            if '-' in producto:
                return producto.split('-')[1].split()[0].lower()
            return producto.split()[0].lower()
    return id_producto.split(' - ')[0].lower()

# Aplicar la función al campo id_producto
obligaciones_clientes['producto'] = obligaciones_clientes['id_producto'].apply(extraer_nombre_producto)

# Filtrar las tasas según cod_segm_tasa, cod_subsegm_tasa y cal_interna_tasa
def filtrar_tasas(row, tasas):
    filtro = (
        (tasas['cod_segmento'] == row['cod_segm_tasa']) &
        (tasas['cod_subsegmento'] == row['cod_subsegm_tasa']) &
        (tasas['calificacion_riesgos'] == row['cal_interna_tasa'])
    )
    return tasas[filtro]

# Función para obtener la tasa basada en el nombre del producto
def obtener_tasa(row, tasas):
    tasas_filtradas = filtrar_tasas(row, tasas)
    producto = row['producto']
    tasa_columna = f'tasa_{producto}'
    if tasa_columna in tasas_filtradas.columns:
        return tasas_filtradas[tasa_columna].values[0]
    return None

# Aplicar la función para obtener la tasa correspondiente
obligaciones_clientes['tasa'] = obligaciones_clientes.apply(lambda row: obtener_tasa(row, tasas_productos), axis=1)

# Función para calcular la tasa efectiva
def calcular_tasa_efectiva(t, periodicidad):
    n = 12 / periodicidad  # Aquí convertimos la periodicidad textual a su valor numérico correspondiente
    te = (((1 + t)**(1/n) - 1) * n) / n
    return te

# Diccionario de periodicidad a valor numérico
periodicidad_dict = {
    'MENSUAL': 1,
    'BIMESTRAL': 2,
    'TRIMESTRAL': 3,
    'SEMESTRAL': 6,
    'ANUAL': 12
}

# Convertir periodicidad a valor numérico
obligaciones_clientes['periodicidad_numerica'] = obligaciones_clientes['periodicidad'].map(periodicidad_dict)

# Calcular la tasa efectiva
obligaciones_clientes['tasa_efectiva'] = obligaciones_clientes.apply(
    lambda row: calcular_tasa_efectiva(row['tasa'], row['periodicidad_numerica']), axis=1
)

# Calcular el valor final
obligaciones_clientes['valor_final'] = obligaciones_clientes['tasa_efectiva'] * obligaciones_clientes['valor_inicial']

# Sumar el valor_final por cliente
suma_valor_final_por_cliente = obligaciones_clientes.groupby('num_documento').agg({
    'valor_final': 'sum',
    'id_producto': 'nunique'
}).reset_index()

# Filtrar clientes con al menos 2 productos distintos
clientes_con_multiples_productos = suma_valor_final_por_cliente[suma_valor_final_por_cliente['id_producto'] >= 2]


# Filtrar el DataFrame original para solo incluir estos clientes
obligaciones_clientes = obligaciones_clientes[obligaciones_clientes['num_documento'].isin(clientes_con_multiples_productos['num_documento'])]

#Ahora generamos el EXCEL en ruta especifica
clientes_con_multiples_productos.to_excel(r'C:\Users\jufeorti\Documents\Automatizaciones\Ecosistemas\Datos\clientes_con_multiples_productos.xlsx', index=False, engine='openpyxl')

#Ahora generamos el EXCEL en ruta especifica
obligaciones_clientes.to_excel(r'C:\Users\jufeorti\Documents\Automatizaciones\Ecosistemas\Datos\oblig_clientes.xlsx', index=False, engine='openpyxl')