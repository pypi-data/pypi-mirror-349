# Librería TCQi

---

Esta librería tiene como propósito facilitar la modificación de archivos TCQi,
descomprimiendo y guardando las tablas en formato Excel y/o DataFrame, y la consiguiente
compresión y guardado en formato TCQi, al finalizar.

---

## Estructura

Para utilizar esta librería, se debe crear en el directorio del proyecto, una carpeta "Data":

```
proyecto-tcqi/
├─ Data/
│   └─ archivo.tcqi
└─ main.py
```

## Utilización

Para instalar la librería, se utiliza el paquete recopilado mediante el comando 'pip':

```
!pip install tcqi
```

A continuación, se debe importar en el archivo Python que lo requiera:

```
from tcqi import TCQi
```

Y para finalizar, se debe inicializar un objeto TCQi, para poder llamar las funciones
que contiene la librería:

```
tcqi = TCQi()
```

Ejemplo:

```
from tcqi import TCQi

# Inicializar el objeto TCQi
tcqi = TCQi()
# Localizar archivo tcqi a modificar
file = 'filename.tcqi'
# Ejecutar una función de la librería con formato 'tcqi.funcion_x()'
table_files = tcqi.read_and_split_TCQi_file(
    tcqi.unpack_file('.//Data//' + file)
)
```
