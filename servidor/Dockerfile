# Usamos una imagen oficial de Node.js ligera
FROM node:18-bullseye-slim

# Definimos el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

# Instalamos CoffeeScript globalmente, tal como lo exige tu servidor
RUN npm install -g coffeescript

# Copiamos todos los archivos de tu servidor al contenedor
COPY . .

# Instalamos las dependencias internas del proyecto
RUN npm install

# Exponemos el puerto de RTMP (1935) y el de HTTP/RTSP (80)
EXPOSE 1935
EXPOSE 80

# El comando maestro que encenderá el servidor automáticamente
CMD ["coffee", "server.coffee"]
