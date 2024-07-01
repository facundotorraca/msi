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

1. **Genera el certificado raiz**:

```sh
chmod +x ./scripts/genroot.sh
.scripts/generate_ca.sh -c "<Nombre del CA>" -d 3650 -k 2048
```

Los parámetros son:
* `-c`: Nombre Común (CN) del certificado.
* `-d`: Número de días para los que el certificado es válido.
* `-k`: Tamaño de la clave RSA en bits.

Este comando guardará los certificados y su correspondiente clave privada en `certs/`:
* `certs/root-ca.pem`
* `certs/root-ca.key`

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
         "subject_name": "example.com",
         "is_ca": false,
         "path_length": null
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