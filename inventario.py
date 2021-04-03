#! /usr/bin/python3
#! -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

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
    return render_template('index.html')

#  pagina de carga de nuevos articulos
@app.route('/alta', methods=['POST'])
def alta():
    if request.method == 'POST':
        # obtengo los datos cargados en el formulario y los mando a variables
        articulo_cod = request.form['articulo_cod']
        articulo_um = request.form['articulo_um']
        articulo_nombre = request.form['articulo_nombre']
        #  mando los datos a la base de datos
        cursor.execute("insert INTO  ARTICULOS values (?,?,?)",(articulo_cod,articulo_um,articulo_nombre.upper()))
        # los guardo
        conexion.commit()
        #  mensaje de que se guardo con exito
        flash("Artículo Agregado con Éxito")
    return redirect(url_for('index'))

# pagina de alta de stock
@app.route('/entrada')
def entrada():
    return 'pagina de entrada'

#  pagina de salida de stock
@app.route('/salida')
def salida():
    return 'pagina de salida'



# ejecucion de la aplicacion
if __name__ == '__main__':
    app.run(port = 5000, debug = True)