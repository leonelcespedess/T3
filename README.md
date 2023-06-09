# Tarea 3: DCCard-Jitsu 🐧🥋


Un buen ```README.md``` puede marcar una gran diferencia en la facilidad con la que corregimos una tarea, y consecuentemente cómo funciona su programa, por lo en general, entre más ordenado y limpio sea éste, mejor será 

Para nuestra suerte, GitHub soporta el formato [MarkDown](https://es.wikipedia.org/wiki/Markdown), el cual permite utilizar una amplia variedad de estilos de texto, tanto para resaltar cosas importantes como para separar ideas o poner código de manera ordenada ([pueden ver casi todas las funcionalidades que incluye aquí](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet))

Un buen ```README.md``` no tiene por que ser muy extenso tampoco, hay que ser **concisos** (a menos que lo consideren necesario) pero **tampoco pueden** faltar cosas. Lo importante es que sea claro y limpio 

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

<Descripción de lo que hace y que **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item. Si quieres, también puedes agregarlos a los títulos:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores
#### Networking: 26 pts (19%)
##### ✅ Protocolo	
##### ✅ Correcto uso de sockets		
##### ✅ Conexión	
##### 🟠 Manejo de Clientes	
El ingresar un tercer cliente, mientras el resto esta ya en conexion, se le notificara que la sala esta llena, pero no podra realizar nada, se tiene que desocupar la sala, y luego volver a depurar el programa para que pueda ingresar este tercer cliente. Cabe recarcar que un tercer cliente no podra ingresar ni interaccionar con el programa, pero tampoco influye el comportamiento de este.
##### ✅ Desconexión Repentina
#### Arquitectura Cliente - Servidor: 31 pts (23%)			
##### ✅ Roles			
##### 🟠 Consistencia	
se mantiene coordinada la coneccion, pero no se utilizan locks.
##### ✅ Logs
Durante la realizacion de la tarea, use muchos prints que me fueron utiles, para entender que informacion me llegaba, como me llegaba, como la proceso, como la mando,etc. Decidi reintegrarlos ya que considero que ayudan a comprender mejor la situacion del programa. Ademas de los minimos.
#### Manejo de Bytes: 27 pts (20%)
##### ✅ Codificación			
##### ✅ Decodificación		
codificacion y decodificacion
En el enunciado dice lo siguiente: 4 largo_total | 4 numero_bloque | 32 bloque, por lo cual esto es lo que segui durante mi codigo, en vez de 4 largo_total | 4 numero_bloque | 28 bloque que se infiere de la pauta	
##### ✅ Encriptación		
##### ✅ Desencriptación	
##### ✅ Integración
#### Interfaz Gráfica: 27 pts (20%)	
##### 🟠 Ventana inicio		
Se advierte que la sala esta llena, pero unicamente eso y vuelve inservible la pestaña de cliente abierta.
##### ✅ Sala de Espera	
No se puede salir de la sala de espera, para ello hay que reinicar el programa de cliente.
##### ❌ Ventana de juego							
##### ❌ Ventana final
#### Reglas de DCCard-Jitsu: 17 pts (13%)
##### ❌ Inicio del juego			
##### ❌ Ronda				
##### ❌ Termino del juego
#### Archivos: 8 pts (6%)
##### ✅ Parámetros (JSON)	
Recalcar que la funcion que permite realizar esto fue extraida de la af3	
##### ❌ Cartas.py	
##### ✅ Cripto.py
#### Bonus: 8 décimas máximo
##### ❌ Cheatcodes	
##### ❌ Bienestar	
##### ❌ Chat

## Ejecución :computer:
Para ejecutar el servidor, se debe ejecutar el main.py correspondiente en su carpeta, es importante que este parametros.json para que pueda obtener el host y port, ademas de el resto de archivos.
De manera analoga para el cliente, se debe ejecutar su respectivo main.py, este utiliza qtdesigner por lo cal considerar los archivos .ui. Ademas, aun que se puso en el gitgnore que se deben ignorar los sprites, para poder lograr una visualizacion de su respectivo interfaz, se debe hacer una copia de la carpeta sprites (o almenos background ) en la carpeta de cliente.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```Pyqt5```: ```QApplication, Qobject, pyqtsygnal y los principales```
2. ```utils```: ```data_json()``` 
3. ...

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```cliente``` y "servidor" : se encargan de la comunicacion entre ellos y algunas funciones superficiales.
2. ```interfaz``` y "logica": se encarga de trabajar con informacion mas relevante, como en el caso de interfaz, actualizar el frontend.
3. ...

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Para que el cliente se visualice bien, debe tener dentro de la CARPETA cliente, la carpeta con los sprites, almenos que dentro de esta este la de background, ya que es necesario que esten estas presentes para poder abrir los interfaces creados en qtdesigner.
2. Notar que aunque el archivo de parametros se llamen igual y tengan el mismo contenido, estos son independientes entre si, y tienen lo mismo unicamente porque no llegue a alguna parte donde requiera algun otro parametro
3. ...

PD: Hago enfasis que en la parte de decodificacion y codificacion, me apegue a lo referenciado en el enunciado respecto a la distribucion de bloques.


-------



**EXTRA:** si van a explicar qué hace específicamente un método, no lo coloquen en el README mismo. Pueden hacerlo directamente comentando el método en su archivo. Por ejemplo:

```python
class Corrector:

    def __init__(self):
          pass

    # Este método coloca un 6 en las tareas que recibe
    def corregir(self, tarea):
        tarea.nota  = 6
        return tarea
```

Si quieren ser más formales, pueden usar alguna convención de documentación. Google tiene la suya, Python tiene otra y hay muchas más. La de Python es la [PEP287, conocida como reST](https://www.python.org/dev/peps/pep-0287/). Lo más básico es documentar así:

```python
def funcion(argumento):
    """
    Mi función hace X con el argumento
    """
    return argumento_modificado
```
Lo importante es que expliquen qué hace la función y que si saben que alguna parte puede quedar complicada de entender o tienen alguna función mágica usen los comentarios/documentación para que el ayudante entienda sus intenciones.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. Principalmente ayudantias y actividades formativas del presente y años anteriores, mi principal apoyo fue mi desarrollo de la af3, de donde copie y pegue codigo que realice, e incluso codigo base. Tambien utilice copie y pegue codigo de mi tarea 2, y sumativas.
2. La funcion data_json que se utilza para obtener parametros, la extraje expresamente de la af3 de este año.



## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/master/Tareas/Descuentos.md).
