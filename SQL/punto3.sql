CREATE TABLE OBLIGACIONES_CLIENTE_RESULT as
WITH OBLIGACIONES_CLIENTES AS (
    SELECT
        *,
        CASE
            WHEN trim(substring(id_producto FROM '.*-\s*(.*)$')) = 'Tarjeta de CrÃ©dito' THEN 'Tarjeta de Crédito'
            ELSE trim(substring(id_producto FROM '.*-\s*(.*)$'))
        END AS producto_final
    FROM public.obligaciones_clientes oc 
)
, TASAS_PRODUCTO AS (
    SELECT
        calificacion_riesgos,
        cod_subsegmento,
        cod_segmento,
        tasa_cartera,
        tasa_operacion_especifica,
        tasa_hipotecario,
        tasa_leasing,
        tasa_sufi,
        tasa_factoring,
        tasa_tarjeta
    FROM public.tasas_producto
)
, CTE_FINAL AS (
    SELECT
        oc.*,
        tp.tasa_cartera,
        tp.tasa_operacion_especifica,
        tp.tasa_hipotecario,
        tp.tasa_leasing,
        tp.tasa_sufi,
        tp.tasa_factoring,
        tp.tasa_tarjeta,
        CASE 
            WHEN oc.producto_final IN ('leasing', 'Leasing Cartera Total') THEN tp.tasa_leasing
            WHEN oc.producto_final = 'Sufi' THEN tp.tasa_sufi
            WHEN oc.producto_final = 'Hipotecario' THEN tp.tasa_hipotecario
            WHEN oc.producto_final IN ('Cartera Total', 'cartera') THEN tp.tasa_cartera
            WHEN oc.producto_final IN ('tarjeta', 'Tarjeta de Crédito') THEN tp.tasa_tarjeta
            WHEN oc.producto_final = 'factoring' THEN tp.tasa_factoring
            WHEN oc.producto_final = 'operacion_especifica' THEN tp.tasa_operacion_especifica
            ELSE 0
        END tasa_correspondiente_producto
    FROM OBLIGACIONES_CLIENTES oc
    LEFT JOIN tasas_producto tp 
        ON oc.cod_segm_tasa::varchar = tp.cod_segmento::varchar 
        AND oc.cod_subsegm_tasa::varchar  = tp.cod_subsegmento::varchar  
        AND oc.cal_interna_tasa::varchar  = tp.calificacion_riesgos::varchar
)
SELECT 
	num_documento,
	id_producto,
    cod_segm_tasa,
    cod_subsegm_tasa,
    cal_interna_tasa,
    tipo_id_producto,
    fecha_desembolso,
    valor_inicial,
    saldo_deuda,
    producto_final,
    tasa_correspondiente_producto,
    periodicidad,
    CASE 
        WHEN periodicidad = 'MENSUAL' THEN 12
        WHEN periodicidad = 'BIMENSUAL' THEN 6
        WHEN periodicidad = 'TRIMESTRAL' THEN 4
        WHEN periodicidad = 'SEMESTRAL' THEN 2
        WHEN periodicidad = 'ANUAL' THEN 1
        ELSE NULL
    END AS n,
    CASE 
        WHEN periodicidad IN ('MENSUAL', 'BIMENSUAL', 'TRIMESTRAL', 'SEMESTRAL', 'ANUAL') THEN
            (POWER((1 + tasa_correspondiente_producto / 100), (1.0 / CASE 
                WHEN periodicidad = 'MENSUAL' THEN 12
                WHEN periodicidad = 'BIMENSUAL' THEN 6
                WHEN periodicidad = 'TRIMESTRAL' THEN 4
                WHEN periodicidad = 'SEMESTRAL' THEN 2
                WHEN periodicidad = 'ANUAL' THEN 1
            END)) - 1) * CASE 
                WHEN periodicidad = 'MENSUAL' THEN 12
                WHEN periodicidad = 'BIMENSUAL' THEN 6
                WHEN periodicidad = 'TRIMESTRAL' THEN 4
                WHEN periodicidad = 'SEMESTRAL' THEN 2
                WHEN periodicidad = 'ANUAL' THEN 1
            END
        ELSE NULL
    END AS tasa_efectiva
    ,tasa_correspondiente_producto * CAST(REPLACE(valor_inicial, ',', '.') AS double precision) AS valor_final
FROM CTE_FINAL