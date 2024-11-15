
# 🚀 Paso a paso para levantar el proyecto

1. **Cloná el repo en tu compu**: Bajate el proyecto con el comando 
    
    ```bash 
    git clone https://github.com/Gonzalo2504/ProyectoHtal.git
    ```

2. **Metete en la carpeta del proyecto**: 

    ```bash 
    cd ProyectoHtal
    ```

3. **Configurá la base de datos y el token**: Creá un archivo config.py en el root del proyecto y meté las siguientes variables:

    ```python
    DATABASE_URL = "mysql+mysqlconnector://<usuario>:<contrasena>@localhost:3306/<base_de_datos>"
    SECRET_KEY = "<clave_secreta>"
    ALGORITHM = "HS256"
    TOKEN_EXPIRE = 6
    ```

4. **Armá un entorno virtual**:

    ```bash
    python3.10 -m venv myvenv
    ```

5. **Activá el entorno virtual**:

    - En Windows:

      ```bash
      .\myvenv\Scripts\activate
      ```

    - En macOS y Linux:

      ```bash
      source myvenv/bin/activate
      ```

6. **Instalá las dependencias del proyecto con este comando**:

    ```bash
    pip install -r app/requirements.txt
    ```

7. **Para inicializar la base de datos se debe ejecutar el siguiente comando**:

    ## Ejecución de la Primera Migración con Alembic

    1. **Instalar Alembic**:
       Asegúrate de tener Alembic instalado en tu entorno virtual.
       ```bash
       pip install alembic
       ```

    2. **Inicializar Alembic**:
       Inicializa el entorno de Alembic en tu proyecto.
       ```bash
       alembic init alembic
       ```

    3. **Configurar Alembic**:
       Abrí el archivo `alembic.ini` y configura la cadena de conexión a tu base de datos.
       
       ```ini
       sqlalchemy.url = mysql+mysqlconnector://<usuario>:<contraseña>@localhost:3306/<nombre_de_la_base_de_datos>
       ```

       En la carpeta /migrations `env.py`:

       ```
       from app.models.models import Base
       target_metadata = Base.metadata
       ```

    4. **Generar una Migración**:
       Genera una nueva migración basada en los cambios en tus modelos.
       ```bash
       alembic revision --autogenerate -m "crear tabla roles"
       ```

    5. **Aplicar la Migración**:
       Aplica las migraciones a tu base de datos.
       ```bash
       alembic upgrade head
       ```

    ¡Listo! Con esto la base de datos debería estar creada. Si hay algún problema, fijate en los logs de Alembic.

8. **Corré el servidor**:

   ```bash
   uvicorn app.main:app --reload
   ```

9. **Crear el primer administrador**:

   1. **Editar la ruta de creación de administradores**:
      Abre el archivo `administrador_routes.py` que se encuentra en la carpeta `routes` y quita temporalmente el `Depends` que verifica el rol de usuario en la función `create_administrador`. 

      Cambia de esto:
      ```python
      @router.post("/administradores/", response_model=Administrador)
      def create_administrador(administrador: AdministradorCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
          return crud_administradores.create_administrador(db=db, administrador=administrador)
      ```

      A esto:
      ```python
      @router.post("/administradores/", response_model=Administrador)
      def create_administrador(administrador: AdministradorCreate, db: Session = Depends(get_db)):
          return crud_administradores.create_administrador(db=db, administrador=administrador)
      ```

   2. **Crear el primer administrador**:
      Usa una herramienta como `Postman` o `curl` para enviar una solicitud `POST` a la ruta `/administradores/` con los datos necesarios para crear un nuevo administrador.

      Ejemplo de comando `curl`:
      ```bash
      curl -X POST "http://localhost:8000/administradores/" -H "Content-Type: application/json" -d '{
          "nombre": "Admin",
          "apellido": "Principal",
          "dni": 12345678,
          "email": "admin@example.com",
          "telefono": "1234567890",
          "usuario": "adminuser",
          "contrasena": "adminpass",
          "rol_id": 1
      }'
      ```

   3. **Revertir los cambios en `administrador_routes.py`**:
      Después de crear el primer administrador, vuelve a colocar el código original en `administrador_routes.py` para reactivar la verificación del rol de usuario:

      ```python
      @router.post("/administradores/", response_model=Administrador)
      def create_administrador(administrador: AdministradorCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
          return crud_administradores.create_administrador(db=db, administrador=administrador)
      ```

   4. **Probar las primeras consultas a la API**:
      Con el primer administrador creado, puedes proceder a probar las primeras consultas a la API para asegurarte de que todo funcione correctamente.

10. **Acceder a la documentación de la API**:

    Una vez que el servidor esté en ejecución, puedes acceder a la documentación de la API en:
    ```
    http://localhost:8000/docs
    ```

    Esta documentación es generada automáticamente por FastAPI y te permite interactuar con los endpoints de la API directamente desde el navegador. Puedes probar solicitudes, ver los modelos de datos y explorar todas las rutas disponibles.

11. Después de crear el administrador, se pueden crear pacientes, médicos y enfermeros:

    - Los `rol_id` son:
      - `1` para administradores
      - `2` para médicos
      - `3` para enfermeros

    - Para crear estos usuarios, primero debes hacer login en la ruta `/login` utilizando el nombre de usuario y contraseña creados para cada usuario. Esto te proporcionará un token que podrás usar para hacer las solicitudes a las rutas protegidas.

    - Ejemplo de solicitud `POST` para hacer login:
      ```bash
      curl -X POST "http://localhost:8000/login/" -H "Content-Type: application/json" -d '{
          "usuario": "adminuser",
          "contrasena": "adminpass"
      }'
      ```

    - El login te devolverá un token JWT que debes incluir en el encabezado `Authorization` como `Bearer <token>` para las siguientes solicitudes.

    - Ejemplo de cómo usar el token para crear un médico:
      ```bash
      curl -X POST "http://localhost:8000/medicos/" -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{
          "nombre": "Doctor",
          "apellido": "Smith",
          "dni": 87654321,
          "especialidad": "Cardiología",
          "email": "doctor@example.com",
          "telefono": "0987654321",
          "usuario": "doctoresmith",
          "contrasena": "docpass"
      }'
      ```

    - Recuerda que la contraseña será hasheada en el backend antes de ser almacenada en la base de datos, asegurando así la seguridad de los datos del usuario.

    - **Verificación de roles**: En las rutas, asegurate de revisar qué acciones puede realizar cada usuario según su rol_id.

¡Listo! Con estos pasos vas a tener el proyecto corriendo y la API en funcionamiento. Si se traba algo, revisá los logs y las rutas para ver qué puede estar fallando. ¡Éxitos!
