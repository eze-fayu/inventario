# !/usr/bin/python3
# -*- coding: utf-8 -*-

#python3 -m pip install pyodbc openpyxl pandas

#sudo apt-get install unixodbc-dev libsqliteodbc unixodbc


import pyodbc
import pandas as pd
import os
import datetime
import uno # get the uno component context from the PyUNO runtime

cnxn = pyodbc.connect("Driver={libsqlite3odbc.so};"
                              "Server=localhost;"
                               "Database=wemeback.db;"
                               "trusted_connection=yes;")

#fecha = input("ingrese la fecha a buscar en formato AAAA-MM-DD:\n")
fecha = "2020/08/01"
#si esta formateada 2222/22/22
if len(fecha) == 10 and fecha[4] == "/" and fecha[7] == "/":
    fecha = fecha[:4] + "-" + fecha[5:7] + "-" + fecha[8:]
#si esta formateada 22222222
elif len(fecha) == 8:
    fecha = fecha[:4] + "-" + fecha[4:6] + "-" + fecha[6:]
#si esta vacia
elif len(fecha) == 0:
    fecha = datetime.date.today() + datetime.timedelta(days=1)
#si esta formateada 2222-22-22
elif len(fecha) == 10 and fecha[4] == "-" and fecha[7] == "-":
    pass
else:
    print("Formato de fecha no válida")
    exit()

#print(fecha)

script = '''SELECT sigaremi.codprov, sigaremi.nro_suc, sigaremi.tipodoc, sigaremi.suc_ent, sigaremi.nro_rem, sigaremi.fecha, sigaremi.art_cod, sigaremi.art_um, sigaremi.art_cant, sigaremi.art_desc, sigaclie.nom_fant, sigaremi.pre_uni, sigaremi.codisco 
FROM sigaremi 
INNER JOIN sigaclie ON sigaremi.codprov = sigaclie.codigo AND sigaremi.nro_suc = sigaclie.sucursal 
WHERE sigaremi.tipodoc = "RC" AND sigaremi.fecha = ? AND sigaclie.nom_fant != "LATIN CHEMICAL SUPPLIERS S.A. "'''

df = pd.read_sql(script, cnxn, params=(fecha,))

writer = pd.ExcelWriter('prod.xlsx')
df.to_excel(writer, sheet_name ='pedidos')
writer.save()

'''
def call_basic_macro():
    document = XSCRIPTCONTEXT.getDocument()
    frame = document.getCurrentController().getFrame()
    ctx = XSCRIPTCONTEXT.getComponentContext()
    dispatcher = ctx.ServiceManager.createInstanceWithContext(
        'com.sun.star.frame.DispatchHelper', ctx)
    url = document.getURL()
    macro_call = ('macro:///Standard.Module1.Macro1("%s")' % url)
    dispatcher.executeDispatch(frame, macro_call, "", 0, ())

g_exported_scripts=call_basic_macro,
'''
'''
desktop = XSCRIPTCONTEXT.getDesktop()
file_url = uno.systemPathToFileUrl("Logistica.ods")
doc = desktop.loadComponentFromURL(file_url, "_blank", 0, ())
oScriptProvider = doc.getScriptProvider()
oScript = oScriptProvider.getScript(
    "vnd.sun.star.script:Standard.PROCUCCION.Main?"
    "language=Basic&location=document")
oScript.invoke((), (), ())
'''

#ejecutamacro = 'soffice "vnd.sun.star.script:Logistica.ods.Standard.PRODUCCION.Main?language=Basic&location=application" "Logistica.ods"'

ejecutamacro = 'soffice "macro://Logistica.ods/Standard.PRODUCCION.Main" "Logistica.ods"'

os.system(ejecutamacro)

#--headless --invisible

'''
localContext = uno.getComponentContext()# create the UnoUrlResolver
resolver = localContext.ServiceManager.createInstanceWithContext(
				"com.sun.star.bridge.UnoUrlResolver", localContext )# connect to the running office
ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
smgr = ctx.ServiceManager# get the central desktop object
desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)# access the current writer document
model = desktop.getCurrentComponent()
'''

soffice --norestore "-accept=socket,host=localhost,port=2002;urp;"
localContext = uno.getComponentContext()
if os.path.exists("Logistica.ods"):
    xl=localContext.Dispatch("Calc.Application")
    xl.Workbooks.Open(Filename="/home/ezequiel/Nextcloud/Trabajo/Logistica.ods", ReadOnly=1)
    xl.Application.Run("Logistica.ods!Standar.PRODUCCION:Main")
##    xl.Application.Save() # if you want to save then uncomment this line and change delete the ", ReadOnly=1" part from the open function.
##    xl.Application.Quit() # Comment this out if your excel script closes
    del xl