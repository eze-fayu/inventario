#! /usr/bin/python3
#! -*- coding: utf-8 -*-

import sqlite3

def creabase():
	conexion = sqlite3.connect('Stock.db')
	cursor = conexion.cursor()

	cursor.execute("""CREATE TABLE "articulos" (
		"codigo"	INTEGER NOT NULL UNIQUE,
		"unidad_medida"	INTEGER NOT NULL,
		"nombre"	TEXT NOT NULL,
		"matprim"	boolean,
		PRIMARY KEY("codigo","unidad_medida")
	);
	""" )
	conexion.commit()

	cursor.execute("""
	CREATE TABLE "materiaprima" (
		"codigo"	INTEGER NOT NULL DEFAULT 'references articulos(codigo)',
		"unidad_medida"	INTEGER NOT NULL DEFAULT 'references articulos(unidad_medida)',
		"cantidad"	INTEGER NOT NULL,
		"operacion"	INTEGER UNIQUE,
		"fecha_movimientos"	datetime,
		PRIMARY KEY("operacion")
	);
	""")
	conexion.commit()


	cursor.execute("""
	CREATE TABLE "movimientos" (
		"operacion"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		"codigo"	INTEGER NOT NULL DEFAULT 'references articulos(codigo)',
		"unidad_medida"	INTEGER NOT NULL DEFAULT 'references articulos(unidad_medida)',
		"cantidad"	INTEGER NOT NULL,
		"fecha_movimientos"	TEXT
	);
	""")
	conexion.commit()
