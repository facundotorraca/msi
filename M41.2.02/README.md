# Servicio de Autoridad Certificadora (CA)

Este proyecto permite establecer una Autoridad Certificadora básica utilizando OpenSSL
para generar el certificado raíz y FastAPI para gestionar operaciones de certificados 
como la generación, verificación y revocación de certificados.

## Requisitos Previos

- **OpenSSL**: Necesario para generar el certificado raíz.
- **Python 3.8 o superior**
- **Uvicorn**: Servidor para ejecutar aplicaciones FastAPI
- **Curl**: Optional to the test cases

## Instalación

1. **Instalar OpenSSL**:

En Ubuntu, puedes instalar OpenSSL con:
```bash
sudo apt-get install openssl
```

En otros sistemas operativos, instala OpenSSL desde la fuente o utilizando el gestor de paquetes apropiado.

2. **Instalar Python packages**:

```sh
pip install -r requirements.txt
```

## Configuracion

> **__NOTE__**: Para todos los comandos, estaremos usando paths relativos, asumiendo que esta en la carperta `/ca-server`

1. **Genera el certificado raiz**:

Puedes usar tus propios certificados raizes. En este caso, explicaremos como generar tu propio _self signed certificate_ para utilizar como raiz 

```sh
chmod +x ./scripts/genroot.sh
.scripts/generate_ca.sh -c "<Nombre del CA>" -d 3650 -k 2048
```

Los parámetros son:
* `-c`: Nombre Común (CN) del certificado.
* `-d`: Número de días para los que el certificado es válido.
* `-k`: Tamaño de la clave RSA en bits.

Este comando guardará los certificados y su correspondiente clave privada en `certs/`:
* `certs/root.pem`
* `certs/root.key`

2. **Configurar y Ejecutar el Servidor FastAPI**:

recomendado:

```sh
sh ./script/startca.sh
```

or con uvicorn

```sh
uvicorn main:app --reload
```

> *__NOTE__*: By default, the app will run on port **8000**. You will be able to access it locally on  `http://localhost:8000`

## Uso de CA

A continuación mostraremos ejemplos para los 3 endpoints:

* **generate**: Genera un nuevo certificado hijo del certificado root
* **verify**: Verifica que el certificado sea valido y emitido por le CA
* **revoke**: Agrega un certificado a la lista de revocados

> *__NOTE__ 1*: Vamos a asumir que la app esta corriendo en la URL default ``http://localhost:8000``

> *__NOTE__ 2*: La aplicación ademas cuenta con documentación en swagger, que podrá ser accedida por: `http://localhost:8000/docs`


### 1. Ejemplo de Generación de Certiticado:

Para generar un nuevo certificado mediante curl, ejecuta el siguiente comando:

```sh
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{
         "subject_name": "example.com"
     }'
```

### 2. Ejemplo de Verificación de Certificado:
Para verificar un certificado mediante curl, usa el siguiente comando, asegurándote de reemplazar el contenido del certificado correctamente:

```sh
curl -X POST "http://localhost:8000/verify" \
     -H "Content-Type: application/json" \
     -d '{
         "cert_pem": "-----BEGIN CERTIFICATE-----\\nMIID...\\n-----END CERTIFICATE-----"
     }'
```

### 3. Ejemplo de Revocación de Certificado:
Para revocar un certificado utilizando curl, utiliza el siguiente comando:

```sh
curl -X POST "http://localhost:8000/revoke" \
     -H "Content-Type: application/json" \
     -d '{
         "cert_pem": "-----BEGIN CERTIFICATE-----\\nMIID...\\n-----END CERTIFICATE-----"
     }'
```

## Servidor con TLS

Para probar uno de los certificados emitidos por nuestra CA, proveemos un servidor simple que corre en el puerto **443** utilizando el protocolo de **HTTPS**.
Este server puede ser levantado utilizando uno de los certificados generados.
Para eso sigue los siguientes pasos:

1. Genera un certificado con la CA utilizando el endpoint especificado mas arriba. Si bien puedes descargar los archivos, la CA guardará una copia local en
    * /ca-server/tmp/certs/**[_unixtimestamp_]**/cert.pem
    * /ca-server/tmp/certs/**[_unixtimestamp_]**/cert.key

2. Copia esos certificados en la carpeta /app-server/certs

3. corre la aplicacion con el comando `python main.py`

4. Listo, tu servidor esta corriendo en utilizando TLS :happy:

Puedes probar el servidor con el siguiente comando:

```sh
curl -X GET "https://localhost/ping" --insecure
```

El `--insecure` es necesario porque caso contrario recibiremos el siguiente error:

````
curl: (60) SSL certificate problem: unable to get local issuer certificate
More details here: https://curl.se/docs/sslcerts.html

curl failed to verify the legitimacy of the server and therefore could not
establish a secure connection to it. To learn more about this situation and
````

Esto se debe a que nosotros no somos un issuer verificado, por lo que nuestros certificados no tienen "validez" para asegurar que seamos una fuente
confiable
