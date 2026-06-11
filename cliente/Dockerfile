# Usamos Ubuntu como sistema base
FROM ubuntu:22.04

# Evitamos que la terminal nos haga preguntas durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Actualizamos el sistema e instalamos la dupla perfecta: FFmpeg (para transmitir) y VLC (para consumir)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    vlc \
    && rm -rf /var/lib/apt/lists/*

# Definimos el directorio de trabajo
WORKDIR /app

# Copiamos el video de prueba al contenedor
# (Asegúrate de tener un archivo llamado video.mp4 en la misma carpeta que este Dockerfile)
COPY video.mp4 .

# VLC no permite ejecutarse como root, así que creamos un usuario estándar
RUN useradd -m cliente_vlc
USER cliente_vlc

# Mantenemos el contenedor vivo en segundo plano para que puedas entrar a ejecutar tus comandos
CMD ["tail", "-f", "/dev/null"]
