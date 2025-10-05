Comando para correr el servidor con cmd:
(si no anda el entorno creenlo python -m venv .entorno)
cd entorno
cd scripts
activate
cd..
cd..
cd web
pip install -r requirements.txt
python manage.py runserver

La base de sql ya esta conectada pero hay que modificar los models para que anden bien poruqe estan configurados para la base de django que no nos va a servir creo. Segun la IA tenemos que usar las dos bases de datos, la de django solo para que entren los administrador y lo que seria el carrusel del inicio, la de sql se usa para todo lo demas.

Para que funcione la base de datos en el settings cambien solo el nombre del host por el que tienen uds en su compu y tendria que andar, tambien tienen que instalar el ODBC 17 xq el 18 anda pa tras.

Antes de migrar preguntenle al chat porque hay un comando raro para que solo se migre a la base de datos de django proque sino se crean nuevas tablas en sql y eso no sirve. FIJENSE LO QUE MIGRAN NO SEAN PELOTUDOS

Faltaria arreglar lo del catalogo porque el model esta mal hecho y no deja subir los productos al sql.

El login SUPUESTAMENTE deberia andar 


