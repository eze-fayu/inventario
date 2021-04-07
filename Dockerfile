FROM welersonb/python3.8-alpine

WORKDIR /inventario

COPY . /inventario

EXPOSE 5555

RUN python3 -m pip --no-cache-dir install -r requirements.txt

CMD [ "python3", "inventario.py" ]



# comando para ejecutarlo
# docker run -v /media/trabajo/Trabajo/Administracion/Stock.db:/inventario/bd/Stock.db -p 5555:5555 inventario
