# Usa una imagen base de Python
FROM python:3.10

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app
# Instala las dependencias desde el archivo requirements.txt
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
# Copia los archivos del proyecto al contenedor
COPY . .
# Exponer el puerto si tu aplicación lo requiere (ejemplo con Flask en puerto 5000)
EXPOSE 34200
# Crear el directorio que vamos a monitorear
RUN mkdir /Videos
# Comando para ejecutar tu aplicación (ajusta según tu archivo Python principal)
CMD ["python", "main.py"]
