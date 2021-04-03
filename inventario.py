#! /usr/bin/python3
#! -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import time

# inicio la aplicacion
app = Flask(__name__)

#  conexion con la base de datos sqlite
conexion = sqlite3.connect('Stock.db', check_same_thread=False)
cursor = conexion.cursor()

# guardo datos de los mensajes y la sesion
app.secret_key = 'mysecretkey'

# main page
@app.route('/')
def index():
    listar_stock = '''select articulos.codigo, articulos.nombre, articulos.unidad_medida, sum(movimientos.cantidad)
                    from articulos
                    INNER JOIN movimientos  on articulos.codigo = movimientos.codigo and articulos.unidad_medida = movimientos.unidad_medida
                    group by articulos.codigo
                    '''
    cursor.execute(listar_stock)
    stock_actual = cursor.fetchall()
    return render_template('index.html', cantidades=stock_actual)

#  pagina de carga de nuevos articulos
@app.route('/alta', methods=['POST'])
def alta():
    if request.method == 'POST':
        # obtengo los datos cargados en el formulario y los mando a variables
        articulo_cod = request.form['articulo_cod']
        articulo_um = request.form['articulo_um']
        articulo_nombre = request.form['articulo_nombre']
        
        # primero controlo que no existe, si es asi 
        consulta = '''select articulos.codigo, articulos.nombre, articulos.unidad_medida
        from articulos
        WHERE articulos.codigo = ? and articulos.unidad_medida = ?
        '''
        cursor.execute(consulta, (articulo_cod, articulo_um))
        resultado = cursor.fetchall()
        # return resultado

        if len(resultado) == 0:
            #  mando los datos a la base de datos
            cursor.execute("insert INTO ARTICULOS values (?,?,?)",(articulo_cod,articulo_um,articulo_nombre.upper()))
            # los guardo
            conexion.commit()
            #  mensaje de que se guardo con exito
            flash("Artículo Agregado con Éxito")
            return redirect(url_for('index'))
        else:
            flash("Artículo Existente")
            return redirect(url_for('index'))

# pagina de alta de stock
# time.strftime("%c") 
@app.route('/entrada', methods=['POST'])
def entrada():
    if request.method == 'POST':
        fecha = time.strftime("%c")
        # obtengo los datos cargados en el formulario y los mando a variables
        articulo_cod = request.form['articulo_cod']
        articulo_um = request.form['articulo_um']
        cantidad = request.form['articulo_cantidad']
        # primero controlo que no existe, si es asi 
        consulta = '''select articulos.codigo, articulos.nombre, articulos.unidad_medida
        from articulos
        WHERE articulos.codigo = ? and articulos.unidad_medida = ?
        '''
        cursor.execute(consulta, (articulo_cod, articulo_um))
        resultado = cursor.fetchall()
        if len(resultado) != 0:
            #  mando los datos a la base de datos
            cursor.execute("insert INTO movimientos(codigo, unidad_medida, cantidad, fecha_movimientos) values (?,?,?,?)",(articulo_cod,articulo_um,cantidad,fecha))
            # los guardo
            conexion.commit()
            #  mensaje de que se guardo con exito
            flash("Entrada Agregada con Éxito")
            return redirect(url_for('index'))
        else:
            flash("Artículo Inexistente")
            return redirect(url_for('index'))

#  pagina de salida de stock
@app.route('/salida', methods=['POST'])
def salida():
    if request.method == 'POST':
        fecha = time.strftime("%c")
        # obtengo los datos cargados en el formulario y los mando a variables
        articulo_cod = request.form['articulo_cod']
        articulo_um = request.form['articulo_um']
        cantidad = request.form['articulo_cantidad']
        # primero controlo que no existe, si es asi 
        consulta = '''select articulos.codigo, articulos.nombre, articulos.unidad_medida
        from articulos
        WHERE articulos.codigo = ? and articulos.unidad_medida = ?
        '''
        cursor.execute(consulta, (articulo_cod, articulo_um))
        resultado = cursor.fetchall()
        if len(resultado) != 0:
            #  mando los datos a la base de datos
            cursor.execute("insert INTO movimientos(codigo, unidad_medida, cantidad, fecha_movimientos) values (?,?,?,?)",(articulo_cod,articulo_um,int(cantidad)*-1,fecha))
            # los guardo
            conexion.commit()
            #  mensaje de que se guardo con exito
            flash("Entrada Agregada con Éxito")
            return redirect(url_for('index'))
        else:
            flash("Artículo Inexistente")
            return redirect(url_for('index'))


# ME QUEDE EN AGREGAR MODIFICACION Y ELIMINACION DE ARTICULOS
@app.route('/modificar', methods=['POST'])
def modificar():
    

# ejecucion de la aplicacion
if __name__ == '__main__':
    app.run(port = 5000, debug = True)