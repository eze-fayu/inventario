# !/usr/bin/python3
# -*- coding: utf-8 -*-

#python3 -m pip install pyodbc openpyxl pandas

#sudo apt-get install unixodbc-dev libsqliteodbc unixodbc


import sqlite3

#  conexion con la base de datos sqlite
conexion = sqlite3.connect('Stock.db', check_same_thread=False)
cursor = conexion.cursor()

def controlarticulos():
    script = '''select articulos.codigo, articulos.nombre, articulos.unidad_medida
    from articulos
    WHERE articulos.codigo = ? and articulos.unidad_medida = ?
    '''
    cursor.execute(script, (704, 2))
    resultado = cursor.fetchall()
    print(resultado)
    if len(resultado) == 0:
        print('no existe')
    else:
        print('existe')
        
# controlarticulos()

script_entrada='''insert INTO movimientos(codigo, unidad_medida, cantidad, fecha_movimientos) 
values (?,?,?,?)
 '''
                
cursor.execute(script_entrada,(704,2,123,"2021/06/03"))
conexion.commit()