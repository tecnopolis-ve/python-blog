## Microblog Python

#### Para ejecutar

Se recomienda utilizar PIPENV

Instalar PIP si no se tiene

```sudo apt-get install python-pip```

Instalar PIPENV

```pip install pipenv```

Instalar todas las dependencias (paquetes pip)

```pipenv install```

Para ejecutar el script

```pipenv run python main.py```

Registrar usuario

```curl -i -X POST -H "Content-Type: application/json" -d '{"username":"manuel","password":"000000"}' http://127.0.0.1:5000/api/users```

Autenticar

1. Contraseña válida (NOTA: copiar el TOKEN para poderlo usar en las otras consultas)

```curl -u manuel:000000 -i -X GET http://127.0.0.1:5000/api/token```

2. Contraseña incorrecta (demo)

```curl -u manuel:344545 -i -X GET http://127.0.0.1:5000/api/token```

3. Acceso a recurso

```curl -u TOKEN_AUTH:unused -i -X GET http://127.0.0.1:5000/api/check```

4. Crear nueva entrada en blog

```curl -u TOKEN_AUTH:unused -i -X POST -H "Content-Type: application/json" -d '{"title":"Hola!","body":"Hola Mundo! esto es un post en mi blog"}' http://127.0.0.1:5000/api/new-post```

5. Consultar entrada blog

```curl -u TOKEN_AUTH:unused -i -X GET http://127.0.0.1:5000/api/get-post/ID```

6. Editar entrada blog

```curl -u TOKEN_AUTH:unused -i -X POST -H "Content-Type: application/json" -d '{"title":"Hola!","body":"Hola Mundo! esto es un post en mi blog"}' http://127.0.0.1:5000/api/edit-post/ID```

7. Eliminar entrada blog

```curl -u TOKEN_AUTH:unused -i -X POST http://127.0.0.1:5000/api/delete-post/ID```

Si se indica un ID de post que no existe o no pertenece al usuario, se recibe un error.

