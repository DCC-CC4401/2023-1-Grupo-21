# 2023-1-Grupo-21
# Budget Pal
BudgetPal es un proyecto de página web creado con Django, que permite a los usuarios:

`-` Crear, modificar y borrar ingresos/egresos.  
`-` Ver su saldo disponible.  
`-` Asignar categorías a sus ingresos/egresos.  
`-` Listar sus ingresos/egresos por categoría.  
`-` Listar sus ingresos/egresos por rango de fechas.

## Requisitos previos e Instalación
Lo primero es clonar el repositorio. Esto se puede hacer copiando el url del repositorio , y aplicando el comando git clone url , en la terminal.
Se recomienda crear un ambiente virtual a la hora de utilizar este proyecto. A continuación, se mostrará como hacerlo en Windows. Para crear el ambiente, navegar por consola hasta la carpeta en que quieras crearlo y escribir:

``` python -m venv myvenv```

Una vez creado, debemos activarlo, para esto basta ingresar en la consola:


``` myvenv\Scripts\activate```

Luego, se debe descargar e instalar los módulos especificados en el archivo requirements.txt. Esto se puede realizar sencillamente con el comando:


```pip install -r requirements.txt```

En el proceso, se instalará automaticamente Django. 
Finalmente, basta aplicar la primer capa de migraciones, esto se realiza con los comandos:


```python manage.py makemigrations```  
```python manage.py migrate```


## Estructura del proyecto
De momento, las principales apps del proyecto son login y movimientos.  Esta sección se irá actualizando a medida que avanze el proyecto.

## Uso
Para ejecutar el programa, es necesario inicializar el comando:


```python manage.py runserver```

Luego, visitar el url: http://localhost:8000/login/ y visitar la sección de Crear un usuario o directamente visitar el url : http://localhost:8000/login/register/ . Una vez creado el usuario, verá distintas opciones como ingresar un nuevo movimiento, revisar el saldo actual o filtrar/modificar/borrar movimientos ya existentes.

## Contacto
El link del repositorio actual es : https://github.com/DCC-CC4401/2023-1-Grupo-21.  
Los usuarios de GitHub de los contributores:  
`-` sven4  
`-` Vonetto  
`-` overexpOG  
`-` CarlaHayler  
`-` camilaF2022
