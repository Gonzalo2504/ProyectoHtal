# Paso a paso para ejecutar el proyecto

1. Clonar el repositorio en tu máquina local utilizando el comando `git clone https://github.com/Gonzalo2504/ProyectoHtal.git` en la terminal.

2. Entrar en la carpeta del proyecto con el comando `cd ProyectoHtal`.

3. Crear un archivo `config.py` en el directorio raíz con las siguientes variables necesarias para la sesión de la base de datos y del token:

    DATABASE_URL = "mysql+mysqlconnector://<usuario>:<contrasena>@localhost:3306/<base_de_datos>"
    SECRET_KEY = "<clave_secreta>"
    ALGORITHM = "HS256"
    TOKEN_EXPIRE = 6

4. Crear un entorno virtual para el proyecto usando el siguiente comando:

    ```bash
      python3.10 -m venv myvenv
      ```

5. Activar el entorno virtual:

    - En Windows:

      ```bash
      .\myvenv\Scripts\activate
      ```

    - En macOS y Linux:

      ```bash
      source myvenv/bin/activate
      ```

6. Instalar las dependencias del proyecto con el siguiente comando:

    ```bash
    pip install -r app/requirements.txt

    ```

7. Para inicializar la base de datos se debe ejecutar el siguiente comando:

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
       Abre el archivo `alembic.ini` y configura la cadena de conexión a tu base de datos.
       ```ini
       sqlalchemy.url = mysql+mysqlconnector://<usuario>:<contraseña>@localhost:3306/<nombre_de_la_base_de_datos>
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

    Con estos pasos, tu base de datos debería estar actualizada con la primera migración. Si encuentras algún problema, revisa los logs de Alembic para obtener más detalles.

8. Una vez creada la primera migración y verificando que se crearon las tablas, ejecuta el servidor con el siguiente comando:

   ```bash
   uvicorn app.main:app --reload
   ```
9. Una vez ejecutado el paso 8 y con el servidor inicializado, sigue estos pasos para crear el primer administrador:

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

10. Acceder a la documentación de la API:

    Una vez que el servidor esté en ejecución, puedes acceder a la documentación de la API en:
    ```
    http://localhost:8000/docs
    ```

    Esta documentación es generada automáticamente por FastAPI y te permite interactuar con los endpoints de la API directamente desde el navegador. Puedes probar solicitudes, ver los modelos de datos y explorar todas las rutas disponibles.
