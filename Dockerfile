FROM alpine:latest


RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

WORKDIR /inventario

COPY . /inventario

RUN pip3 --no-cache-dir install -r requirements.txt

CMD [ "python3", "inventario.py" ]