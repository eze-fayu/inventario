#! /usr/bin/python3
#! -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime, date, timedelta
import crea_bd 

# inicio la aplicacion
app = Flask(__name__)

#  conexion con la base de datos sqlite
if not os.path.exists('bd/Stock.db'):
        crea_bd.creabase
        
conexion = sqlite3.connect('bd/Stock.db', check_same_thread=False)
cursor = conexion.cursor()

# guardo datos de los mensajes y la sesion
app.secret_key = 'mysecretkey'

# main page
@app.route('/')
def index():
    mes = datetime.now().strftime("%Y%m")
    mes_ant = (date.today().replace(day=1) - timedelta(days=1)).strftime("%Y%m")
    
    listar_stock = '''select articulos.codigo, articulos.nombre, articulos.unidad_medida, sum(movimientos.cantidad)
                    from articulos
                    INNER JOIN movimientos  on articulos.codigo = movimientos.codigo and articulos.unidad_medida = movimientos.unidad_medida
                    group by articulos.codigo
                    '''
    cursor.execute(listar_stock)
    stock_actual = cursor.fetchall()
    
    listar_stock2 = '''select articulos.codigo, articulos.nombre, articulos.unidad_medida, materiaprima.cantidad, max(materiaprima.fecha_movimientos)
                    from articulos
                    INNER JOIN materiaprima  on articulos.codigo = materiaprima.codigo and articulos.unidad_medida = materiaprima.unidad_medida
                    group by articulos.codigo
                    '''
    cursor.execute(listar_stock2)
    mp_actual = cursor.fetchall()    
    
    transporte_actual = '''select sum(transporte.cantidad)
                       from transporte
                       where transporte.fecha_movimientos like ?
                    '''
    cursor.execute(transporte_actual,(mes+"%",))
    transporte_actual_resultado = cursor.fetchall()
    
    transporte_pasado = '''select sum(transporte.cantidad)
                       from transporte
                       where transporte.fecha_movimientos like ?
                    '''
    cursor.execute(transporte_pasado,(mes_ant+"%",))
    transporte_pasado_resultado = cursor.fetchall()    
    
    rueda_actual = '''select sum(larueda.cantidad)
                       from larueda
                       where larueda.fecha_movimientos like ?
                    '''
    cursor.execute(rueda_actual,(mes+"%",))
    rueda_actual_resultado = cursor.fetchall()
    
    rueda_pasado = '''select sum(larueda.cantidad)
                       from larueda
                       where larueda.fecha_movimientos like ?
                    '''
    cursor.execute(rueda_pasado,(mes_ant+"%",))
    rueda_pasado_resultado = cursor.fetchall()
    
    return render_template('index.html', cantidades=stock_actual, materiasprimas=mp_actual, mes=mes, mes_ant=mes_ant, \
        rueda_actual_resultado=rueda_actual_resultado[0][0], rueda_pasado_resultado=rueda_pasado_resultado[0][0], \
        transporte_pasado_resultado=transporte_pasado_resultado[0][0], transporte_actual_resultado=transporte_actual_resultado[0][0])

#  pagina de carga de nuevos articulos
@app.route('/alta', methods=['POST'])
def alta():
    if request.method == 'POST':
        # obtengo los datos cargados en el formulario y los mando a variables
        mp = ''
        articulo_cod = request.form['articulo_cod']
        articulo_um = request.form['articulo_um']
        articulo_nombre = request.form['articulo_nombre']
        materiaprima = request.form['matprim']
        print("valor de materia prima: ",materiaprima)
        if materiaprima == "1":
            mp = "True"
        else:
            mp = "False"
        print("valor de mp :",mp)
        # controlo si esta vacio lo saco, si esta completo lo guardo
        if articulo_cod == '' or articulo_um == '' or articulo_nombre == '':
            flash("Artículo Incompleto")
            return redirect(url_for('index'))
        else:
            # primero controlo que no existe, si es asi 
            consulta = '''select articulos.codigo, articulos.nombre, articulos.unidad_medida
            from articulos
            WHERE articulos.codigo = ? and articulos.unidad_medida = ?
            '''
            cursor.execute(consulta, (articulo_cod, articulo_um))
            resultado = cursor.fetchall()
            # return resultado

            if len(resultado) == 0:
                #  mando los datos a la base de datos articulo
                cursor.execute("insert INTO ARTICULOS values (?,?,?,?)",(articulo_cod,articulo_um,articulo_nombre.upper(),mp))
                # los guardo
                conexion.commit()
                #  mensaje de que se guardo con exito
                if materiaprima == "1":
                    fecha = datetime.now().strftime("%Y%m%d%H%M%S")
                    #  mando los datos a la base de datos materiaprima
                    cursor.execute("insert INTO materiaprima(codigo, unidad_medida, cantidad, fecha_movimientos) values (?,?,0,?)",(articulo_cod,articulo_um,fecha))
                    # los guardo
                    conexion.commit()

                #  mensaje de que se guardo con exito
                flash("Artículo Agregado con Éxito")
                return redirect(url_for('index'))
            else:
                flash("Artículo Existente")
                return redirect(url_for('index'))

# pagina de alta de stock
# time.strftime("%Y%m%d%H%M%S") 
@app.route('/entrada', methods=['POST'])
def entrada():
    if request.method == 'POST':
        fecha = datetime.now().strftime("%Y%m%d%H%M%S")
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
        fecha = datetime.now().strftime("%Y%m%d%H%M%S")
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


@app.route('/modificar/<codigo>')
def datos_modificar(codigo):
    # HAGO LA OCNSULTA en la base de datos por el valor que tengo al hacer click en modificar
    fecha = datetime.now().strftime("%Y%m%d%H%M%S")
    mod_mp = '''select articulos.codigo, articulos.nombre, materiaprima.cantidad, materiaprima.unidad_medida
                    from articulos
                    INNER JOIN materiaprima  on articulos.codigo = materiaprima.codigo and articulos.unidad_medida = materiaprima.unidad_medida
                    where materiaprima.codigo = ?
                    '''
    # ejecuto la ocnsulta
    cursor.execute(mod_mp, (codigo,))  #LOS CORCHETES ES PARA QUE TOME LITERAL EL VALOR DE LA VARIABLE PORQUE CON LA TUPLA TOMA 3 (154 COMO 1,5 Y 4) sino (codigo y ,) para q haga tupla
    # guardo los datos en la variable
    mp_modificar = cursor.fetchall()
    print(mp_modificar[0])
    return render_template('modificar.html', mp_edit = mp_modificar[0])    

@app.route('/actualiza/<codigo>', methods=['POST'])
def modificar(codigo):
    if request.method == 'POST':
        fecha = datetime.now().strftime("%Y%m%d%H%M%S")
        # obtengo los datos cargados en el formulario y los mando a variables
        articulo_cod = request.form['articulo_cod']
        articulo_um = request.form['articulo_um']
        cantidad = request.form['cantidad']
        
        print("valores a ingresar",articulo_cod, articulo_um, cantidad, fecha)
        # primero controlo que no existe, si es asi 
        
        # consulta por actualizacion. pase a insertar nuevos datos
        # consulta = '''update materiaprima
        #                 set cantidad = ?,
        #                 fecha_movimientos = ?
        #             where codigo = ?
        # '''
        consulta = '''insert INTO materiaprima(codigo, unidad_medida, cantidad, fecha_movimientos) values (?,?,?,?) 
        '''
        
        
        cursor.execute(consulta, (articulo_cod,articulo_um,cantidad,fecha))
        # cursor.execute(consulta, (cantidad, fecha, codigo))
        # los guardo
        conexion.commit()
        #  mensaje de que se guardo con exito
        flash("Entrada Modificada con Éxito")
        return redirect(url_for('index'))


################################################################
# la rueda
@app.route('/larueda', methods=['POST'])
def larueda():
    if request.method == 'POST':
        fecha = datetime.now().strftime("%Y%m%d%H%M%S")
        cantidad = request.form['cantidad_cajas']
        if len(cantidad) != 0:
            #  mando los datos a la base de datos
            cursor.execute("insert INTO larueda(cantidad, fecha_movimientos) values (?,?)",(cantidad,fecha))
            # los guardo
            conexion.commit()
            #  mensaje de que se guardo con exito
        
            flash("Entrada Agregada con Éxito")
            return redirect(url_for('index'))


#############################################################
# costanzo
@app.route('/transporte', methods=['POST'])
def transporte():
    if request.method == 'POST':
        fecha = datetime.now().strftime("%Y%m%d%H%M%S")
        # obtengo los datos cargados en el formulario y los mando a variables
        cantidad = request.form['cantidad_viajes']
        if len(cantidad) != 0:
            #  mando los datos a la base de datos
            cursor.execute("insert INTO transporte(cantidad, fecha_movimientos) values (?,?)",(cantidad,fecha))
            # los guardo
            conexion.commit()
            #  mensaje de que se guardo con exito
            flash("Entrada Agregada con Éxito")
            return redirect(url_for('index'))


# @app.roure('/borrar')
# def eliminar():
#     continue

# ejecucion de la aplicacion
if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 5555, debug = True)