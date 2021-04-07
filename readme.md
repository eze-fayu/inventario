## Aplicacion de inventario

Realizada con python y flask. Lista para crear un contenedor con docker.  
Se conecta al puerto 5555.  
Necesita de la Base de datos que se vincula al docker como:  
```
-v ruta/a/la/base/de/datos/Stock.db:/inventario/db/Stock.db
```

Mapear el puerto
```
-p 5555:5555
```