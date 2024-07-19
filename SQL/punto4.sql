CREATE TABLE MULTIPLES_PRODUCTOS as
with cte as (
	select
		row_number() over (partition by num_documento ) conteo
		,tipo_id_producto 
		,*
	from public.obligaciones_cliente_result
	where num_documento = '1032032677'
), cte_summary as (
	select num_documento ,  COUNT(distinct id_producto ) cantidad_productos
	from public.obligaciones_cliente_result
	where num_documento = '1032032677'
	group by 1
), CTE_FINAL as (
select 
	cte.num_documento
	,cs.cantidad_productos
	,sum(cte.valor_final ) total_valor_final
from cte 
left join cte_summary CS
on cte.num_documento = cs.num_documento
group by 1,2
)
select * from CTE_FINAL where cantidad_productos >= 2

