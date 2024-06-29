# Instancia EC2 con Docker y BWAPP usando Terraform

Esta guía proporciona instrucciones paso a paso sobre cómo usar Terraform 
para crear una instancia EC2 en AWS, instalar Docker y ejecutar la aplicación BWAPP.
La instancia se creará con un par de claves especificado para el acceso seguro por SSH.

> :warning: **imporante**: Este setup tiene un costo sobre la cuenta de Amazon, que si bien es minimo, no es totalemnte gratis. Esto se debe a que Amazon pasó a cobrar por las IPs publicas de sus servicios gratuitos (0.005 USD por hora). Recuerda ejecutrar el paso #4 para realizar la limpieza y evitar sorpresas!

## Requisitos previos

1. **Cuenta de AWS**: Debes tener una cuenta de [AWS](https://aws.amazon.com/).
2. **Cuenta en Cloudflare**: Debes tener una cuenta en [Cloudflare](www.cloudflare.com)
3. **Un dominio**: Puedes comprar un _.xyz_ por $1 USD en [Namecheap](www.namecheap.com)
3. **AWS CLI**: Instalar y configurar AWS CLI con los permisos necesarios.
4. **Terraform**: Instalar Terraform en tu máquina local.

## Setup

### 1. Configurar AWS CLI

Primero, configura AWS CLI con tus credenciales. 
Esto creará un perfil que Terraform puede usar.

```sh
aws configure --profile <mi-perfil-terraform>
```

Se te pedirá que ingreses tu AWS Access Key ID, AWS Secret Access Key, 
nombre de la región por defecto y formato de salida por defecto.


### 2. Establecer la Variable de Entorno

Establece la variable de entorno AWS_PROFILE para usar el perfil que configuraste.

```sh
export AWS_PROFILE=<mi-perfil-terraform>
```

### 3. Linkear dominio a Cloudflare

Puedes seguir esta [guia](https://developers.cloudflare.com/fundamentals/setup/manage-domains/add-site/) para linkear tu dominio a _Cloudflare_.

Si segusite las recomendaciones de esta guia y adquiriste el dominio por _Namecheap_, puedes seguir esta [guia](https://www.namecheap.com/support/knowledgebase/article.aspx/9607/2210/how-to-set-up-dns-records-for-your-domain-in-a-cloudflare-account) de como vincular los servidores DNS

### 4. Crear infraestructura

#### 4.1 Inicializar Terraform

Inicializa la configuración de Terraform. Esto descargará los plugins necesarios del proveedor

```sh
terraform init
```

#### 4.2 Plan de la configuracion

Genera y revisa el plan de ejecución para la infraestructura. Esto te mostrará lo que Terraform va a crear o cambiar.

```sh
terraform plan
```

#### 4.3 Aplicar la configuracion

Aplica la configuración de Terraform para crear los recursos.

```sh
terraform apply
```

#### 4.4 Output

Luego de la ejecución, terraform dará los siguientes resultados:

```sh
* cloudflare_record = "<Nombre del dominio>"
* ec2_public_ip     = "<IP Publica del servicio>"
* ec2_public_dns    = "<DNS Publico para acceder>"
* ec2_instance_id   = "<ID de la instancia en EC2>"
```

**_NOTE:_**  En la proxima sección explicaremos en detalle como usar el public DNS para acceder a la aplicación BWapp.

Podras consultarlo tambien con:

```sh
terraform output <variable>
```

### 5. Inicializar la aplicación BWapp

Una vez instalado todo, podrás acceder a tu servicio por HTTPs como:

`www.<dominio>.com`

Primero debes instalar la base de datos, para eso:
1. Ingresa a `www.<dominio>.com/install.php`
2. Hace click en instalar 

Una vez instalado, puedes ir a la pagina y loaggearte con las credenciales defualt:

* **username**: _bee_
* **password**: _bug_

Ya puedes disfrutar de todas las vulnerabilidades :smile:

### 6. Limpieza

> :warning: **imporante**: Ejecuta este paso, ya que las IPs publicas de amazon tienen un costo. Si no se ejecuta este paso, 

Para destruir la infraestructura creada por Terraform, ejecuta:

```sh
terraform destroy
```

Confirma la acción cuando se te solicite escribiendo "yes".


