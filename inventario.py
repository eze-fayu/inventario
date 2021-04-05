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
    listar_stock2 = '''select articulos.codigo, articulos.nombre, articulos.unidad_medida, materiaprima.cantidad
                    from articulos
                    INNER JOIN materiaprima  on articulos.codigo = materiaprima.codigo and articulos.unidad_medida = materiaprima.unidad_medida
                    '''
    cursor.execute(listar_stock2)
    mp_actual = cursor.fetchall()
    return render_template('index.html', cantidades=stock_actual, materiasprimas=mp_actual)

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
            # devulevo a la pagina indice
            return redirect(url_for('index'))
        else:
            #  mensaje de que no existe el articulo
            flash("Artículo Inexistente")
            # devulevo a la pagina indice
            return redirect(url_for('index'))


# ME QUEDE EN AGREGAR MODIFICACION Y ELIMINACION DE ARTICULOS
@app.route('/modificar/<codigo>')
def datos_modificar(codigo):
    # HAGO LA OCNSULTA en la base de datos por el valor que tengo al hacer click en modificar
    fecha = time.strftime("%c")
    mod_mp = '''select articulos.codigo, articulos.nombre, materiaprima.cantidad
                    from articulos
                    INNER JOIN materiaprima  on articulos.codigo = materiaprima.codigo and articulos.unidad_medida = materiaprima.unidad_medida
                    where materiaprima.codigo = ?
                    '''
    # ejecuto la ocnsulta
    cursor.execute(mod_mp, (codigo,))  #LOS CORCHETES ES PARA QUE TOME LITERAL EL VALOR DE LA VARIABLE PORQUE CON LA TUPLA TOMA 3 (154 COMO 1,5 Y 4) sino (codigo y ,) para q haga tupla
    # guardo los datos en la variable
    mp_modificar = cursor.fetchall()
    return render_template('modificar.html', mp_edit = mp_modificar[0])    

@app.route('/actualiza/<codigo>', methods=['POST'])
def modificar(codigo):
    if request.method == 'POST':
        fecha = time.strftime("%c")
        # obtengo los datos cargados en el formulario y los mando a variables
        # articulo_cod = request.form['articulo_cod']
        # articulo_um = request.form['articulo_um']
        cantidad = request.form['cantidad']
        # primero controlo que no existe, si es asi 
        consulta = '''update materiaprima
                        set cantidad = ?,
                        fecha_movimientos = ?
                    where codigo = ?
        '''
        cursor.execute(consulta, (cantidad, fecha, codigo))
        # los guardo
        conexion.commit()
        #  mensaje de que se guardo con exito
        flash("Entrada Modificada con Éxito")
        return redirect(url_for('index'))

# @app.roure('/borrar')
# def eliminar():
#     continue

# ejecucion de la aplicacion
if __name__ == '__main__':
    app.run(port = 5000, debug = True)