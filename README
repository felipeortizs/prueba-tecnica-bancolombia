# Prueba Técnica: ETL, Manipulación de Datos y API con Python

## Introducción

Esta documentación detalla el proceso y los pasos seguidos para realizar una prueba técnica que consta de tres partes: ETL (Extracción, Transformación y Carga), manipulación de datos con Python y Pandas, y la creación de una API con Python para exponer la información procesada.

## Parte 1: ETL

### Descripción

En esta primera parte, se recibió un correo con dos archivos Excel: `obligaciones_clientes.xlsx` y `tasas_productos.xlsx`. Estos archivos se importaron a una base de datos local llamada `banco` utilizando el motor de base de datos PostgreSQL. 

### Requisitos

- PostgreSQL
- Python 3.11.9
- Pandas
- Openpyxl

### Proceso

1. **Importación de los Archivos Excel a la Base de Datos**
   - Archivos recibidos: `obligaciones_clientes.xlsx` y `tasas_productos.xlsx`.
   - Conexión a la base de datos: `postgresql://postgres:admin@localhost:5432/banco`.
   - Importación de los archivos a las tablas correspondientes en la base de datos.

2. **Transformaciones de Datos**
   - En la tabla `obligaciones_clientes`:
     - Se encontraron 6 registros con el campo `plazo` en `None` y se cambiaron por vacío.
     - Se corrigieron caracteres UTF-8 en el campo `id_producto` de 'Tarjeta de CrÃ©dito' a 'Tarjeta de Crédito'.
   - Creación de las tablas `OBLIGACIONES_CLIENTE_RESULT` y `MULTIPLES_PRODUCTOS` para su uso posterior en el API.

## Parte 2: Manipulación de Datos con Python y Pandas

### Descripción

Se realizó la manipulación y análisis de datos provenientes de los archivos `obligaciones_clientes.xlsx` y `tasas_productos.xlsx` utilizando Python y la librería Pandas.

### Proceso

1. **Carga de Datos**
   - Se cargaron los datos de los archivos `obligaciones_clientes.xlsx` y `tasas_productos.xlsx` utilizando Pandas.

2. **Extracción del Nombre del Producto**
   - Se implementó una función para extraer el nombre del producto del campo `id_producto`.

3. **Filtrado de Tasas**
   - Se creó una función para filtrar las tasas en el archivo `tasas_productos` basándose en los valores de `cod_segm_tasa`, `cod_subsegm_tasa` y `cal_interna_tasa`.

4. **Obtención de la Tasa Correspondiente**
   - Se desarrolló una función para obtener la tasa correspondiente al producto basándose en el nombre del producto extraído.

5. **Cálculo de la Tasa Efectiva**
   - Se implementó una función para calcular la tasa efectiva utilizando una fórmula específica.

6. **Cálculo del Valor Final**
   - Se calculó el `valor_final` multiplicando la `tasa_efectiva` por el `valor_inicial` de cada obligación.

7. **Suma del Valor Final por Cliente**
   - Se agruparon las obligaciones por cliente y se sumaron los valores finales para cada cliente.

8. **Conteo de Productos Distintos por Cliente**
   - Se contó la cantidad de productos distintos por cliente.

9. **Filtrado de Clientes con al Menos 2 Productos**
   - Se filtraron los clientes que tienen al menos 2 productos distintos.

10. **Guardado del Resultado Final**
    - Se guardaron los resultados en archivos Excel: `clientes_con_multiples_productos.xlsx` y `oblig_clientes.xlsx`.

## Parte 3: Creación de una API con Python

### Descripción

Se necesita disponibilizar un API con dos endpoints que permitan, a través de un número de documento, consultar los registros solicitados.

### Requisitos

- Python 3.x
- FastAPI
- Uvicorn

### Endpoints

1. **Consultar Productos, Tasas Efectivas y Valor Final por Cliente**
   - Endpoint: `/punto3/{documento}`
   - Devuelve varios registros dependiendo del cliente consultado.
   
2. **Consultar Valor Total por Cliente**
   - Endpoint: `/punto4/{documento}`
   - Devuelve un único registro por cliente.

### Proceso

1. **Activar el Ambiente Virtual**
   - Sistema operativo: Windows 11
   - Comando: `myenv\Scripts\activate`

2. **Ejecutar el API**
   - Comando: `uvicorn main:app --reload`

3. **Pruebas de Endpoints**
   - Para consultar productos, tasas efectivas y valor final:
     - `http://127.0.0.1:8000/punto3/1299605389`
     - `http://127.0.0.1:8000/punto3/1032032677`
   - Para consultar el valor total:
     - `http://127.0.0.1:8000/punto4/1299605389`
     - `http://127.0.0.1:8000/punto4/1032032677`

## Dependencias

Asegúrate de tener todas las dependencias necesarias instaladas. Puedes instalarlas utilizando el archivo `requirements.txt`.

### Crear el archivo `requirements.txt`

Para generar el archivo `requirements.txt` con todas las dependencias instaladas en tu ambiente virtual, utiliza el siguiente comando:

```sh
pip freeze > requirements.txt