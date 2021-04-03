#!/usr/bin/python3
# -*- coding: utf-o -*-

"""
# AGREGAR ARTICULO
insert INTO  ARTICULO values (704,02,800)

# AGREGAR ENTRADA
insert INTO  ENTRADA(CODIGO,unidad_medida,CANTIDAD) values (704,02,800)

# AGREGAR SALIDA
insert INTO  SALIDA(CODIGO,unidad_medida,CANTIDAD) values (704,02,40)

# TOTAL ENTRADAS
select articulos.codigo, articulos.nombre, articulos.unidad_medida, sum(entrada.cantidad)
from articulos
INNER JOIN entrada  on articulos.codigo = entrada.codigo and articulos.unidad_medida = entrada.unidad_medida
# para filtrar x articulo
WHERE articulos.codigo = 704
# para agrupar x articulos
group by articulos.codigo


# TOTAL SALIDAS
select articulos.codigo, articulos.nombre, articulos.unidad_medida, sum(salida.cantidad)
from articulos
INNER JOIN salida  on articulos.codigo = salida.codigo and articulos.unidad_medida = salida.unidad_medida
"""
