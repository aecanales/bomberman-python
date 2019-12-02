# Code with Fire - aecanales edition

:warning: **El código de esta tarea está en [inglés.](https://github.com/IIC2233/Syllabus-2017-2/issues/328#issuecomment-332159706)**

Para abrir el juego, debes abrir `main.py`. `highscores.csv` debe existir en la misma carpeta que `main.py`. Si deseas cambiar `mapa.txt`, está ubicado en `game/assets`.

## Consideraciones generales

### Comentarios

* Está implemtando *Kick the Bomb* y el modo multijugador.
* El código está muy inspirado en lo que es el motor de desarrollo de juegos [Unity.](https://unity3d.com/) Si los has usado, la estructura del código se te va a hacer muy intuitivo! 
* A veces las bombas se glitchean y dan saltos a espacios aleatorios despues de posicionarlos. Si esto empieza a ocurrir, **reinicia el juego**, va a seguir ocurriendo y el juego se va glitchear más y más.
* El power-up de supervelocidad hace que las colisiones se vayan a la b :grimacing:
* No alcanzé a terminar el cambio de look, pero los sprites que no son los dados vienen de [The Legend of Zelda:](https://www.spriters-resource.com/fullview/28736/) [A Link to the Past.](https://www.spriters-resource.com/fullview/7587/)

### Lo que no hice

* El jugadores parten en posiciones predefinidas, **no se pueden posicionar.**
* En el modo multijugador: el segundo jugador **no** tiene puntaje propio, y los enemigos sólo persiguen el primer jugador. 
* Se detecta cuando se alcanza el puntaje para el aumento de dificultad, pero la dificultada **no** aumenta en verdad.
* Existe el constante que repesenta el tamaño de la grilla, pero en verdad **no cambia el tamaño del mapa.**

## Desglose de mi libreria

* `main.py`: Continue el menú principal, el menú de highscores y la ventana principal del juego. (sí, hubiera sido bueno modularizar aquí pero no alcanzé :sweat_smile:)

### :file_folder: `game`

* `game.py`: Contiene el código que inicializa los objetos del nivel. Mi back-end usa el patrón de [object pooling](https://es.wikipedia.org/wiki/Object_pool_(patr%C3%B3n_de_dise%C3%B1o)) por lo que todos los objetos del juego son instanciados antes de comenzar.

#### :file_folder: `game/assets`

Contine los sprites y animaciones de los personajes y objetos del juego.

### :file_folder: `game/engine`

Contiene todo lo que es el código "base" para lo que es el juego.

* `back_end.py`: Contiene la clase `Engine`, quien maneja el [game loop](http://gameprogrammingpatterns.com/game-loop.html) principal (en su `run()`). 
* `collision_manager.py`: Maneja la deteción de collisiones entre las entidades del juego.
* `front_end.py`: Contiene la clase `Screen`, donde se dibuja todo lo que es el juego.
* `game_object.py`: **Contiene la clase `GameObject` del cual heredan todos los objetos en el juego**. Contiene varios componentes (ver un poco más abajo) y funciones para ser overrideadas por las clases que la heredan (cada uno esta propiamente documentado en el código). 
* `helper_functions.py`: Contiene funciones adicionales útiles para el juego. 
* `input_manager.py`: Maneja el input del usuario, distinguiendo entre *press*, *hold*, y *release*, para poder encapsular en una interfaz facil de utilizar después.

#### :file_folder: `game/engine/components`

["Components"](http://gameprogrammingpatterns.com/component.html) que se agregan a un `GameObject` para darle funcionalidad.

* `animator.py`: Componente que se encarga de cambiar el QPixmap del `GameObject` para crear animaciones.
* `box_collider.py`: Conjunto de funciones y propiedades que `collision_manager.py` usa para calcular si dos objetos están colisionando o no.
* `sprite_renderer.py`: Componente que da representación visual del objeto.
* `transform.py`: Guarda la posición y la escala del objeto.

### :file_folder: `game/game_logic`

Contiene lo que es el código propiamente específico de *Code with Fire*. Es mas o menos intuitivo que script está asociado a que parte del juego, por lo cual no los detallaré uno por uno.
