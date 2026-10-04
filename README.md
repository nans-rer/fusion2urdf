# URDF Exporter para Fusion 360

Este es un **fork** del repositorio original: https://github.com/syuntoku14/fusion2urdf

## **Cambios realizados**

* **Compatibilidad con Python 3.12**: Se reemplazó el módulo obsoleto `distutils.dir_util` por `shutil` para las operaciones con directorios, asegurando la compatibilidad con **Python 3.12**, utilizado por Fusion 360.
* **Manejo de errores**: Se mejoró el manejo de errores para evitar `FileExistsError` al copiar directorios que ya existen.
* **Operaciones con directorios**: Toda la copia de directorios ahora se realiza utilizando `shutil.copytree`.

## **Notas**

* El script está actualizado para utilizarse con **Python 3.12**, ya que Fusion 360 dejó de admitir `distutils` en versiones superiores a Python 3.10.

---

## ¡Actualizado!

### 2021/01/09: Corrección del cálculo de xyz

* Si observas que tus componentes se desplazan alrededor del centro del mapa en RViz, prueba esta actualización.
* Para obtener más información, consulta:
  https://forums.autodesk.com/t5/fusion-360-api-and-scripts/difference-of-geometryororiginone-and-geometryororiginonetwo/m-p/9837767

### 2020/11/10: Correcciones del README

* Se corrigió el comando de instalación para MacOS en el README.
* Se unificó el formato de fecha en el README a `yyyy/dd/mm`.
* Se movió la sección de instalación hacia arriba para mejorar la experiencia del usuario y facilitar su localización.

### 2020/01/04: Múltiples actualizaciones

* Ya no es necesario ejecutar un script de Bash para convertir los archivos STL.
* Se realizaron algunas mejoras en la generación de joints y transmisiones.
* Se define una etiqueta de material de ejemplo en lugar de definir un material en cada link.
* `fusion2urdf` ahora genera un paquete ROS `{robot_name}_description` independiente y autocontenido.
* Ahora se inicia mediante:
  `roslaunch {robot_name}_description display.launch`
* Se cambió la salida de `fusion2urdf` de URDF a Xacro para proporcionar mayor flexibilidad.
* Los materiales, las transmisiones y los elementos de Gazebo se separaron en archivos independientes.

### 2018/20/10: Corrección de funciones

* Se corrigieron las funciones encargadas de generar los archivos `launch`.

### 2018/25/09: Soporte para tipos de joints

* Se añadieron los tipos de joint **"Rigid"** y **"Slider"**.
* Se añadió soporte para los límites de los joints de tipo **"Revolute"** y **"Slider"**.

### 2018/19/09: Correcciones

* Se corrigieron errores relacionados con el centro de masa y la inercia.

---

# Instalación

Ejecuta el siguiente comando en tu terminal.

### Windows (PowerShell)

```powershell
cd <path to fusion2urdf>
Copy-Item ".\URDF_Exporter\" -Destination "${env:APPDATA}\Autodesk\Autodesk Fusion 360\API\Scripts\" -Recurse
```

### macOS (Bash o Zsh)

```bash
cd <path to fusion2urdf>
cp -r ./URDF_Exporter "$HOME/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/"
```

---

# ¿Qué es este script?

Este es un script para Fusion 360 que permite exportar directamente un modelo de Fusion 360 a URDF.

El script exporta:

* Un archivo `.urdf` del modelo.
* Archivos `.launch` y `.yaml` para simular el robot en Gazebo.
* Archivos `.stl` del modelo.

## Ejemplo

El siguiente modelo de prueba no queda orientado verticalmente porque el eje Z no está orientado hacia arriba en Fusion 360 de forma predeterminada.

Si quieres que el robot quede correctamente orientado, asegúrate de que el eje Z esté orientado hacia arriba en tu modelo de Fusion 360.

### Modelo original

[Imagen del modelo industrial]

### Simulación en Gazebo del `.urdf` y `.launch` exportados

* Centro de masa.
* Colisiones.
* Inercia.

---

# Antes de utilizar este script

Antes de utilizar este script, asegúrate de que todos los **"links" estén definidos como componentes**.

Debes definir los links creando los componentes correspondientes. Por ejemplo, el modelo de [SpotMini](https://grabcad.com/library/spotmini-robot-1) no es compatible a menos que definas el `base_link`.

Además, debes tener cuidado al definir los joints.

Los **links padre (`parent links`) deben configurarse como `Component2` al definir el joint, y no como `Component1`**.

Por ejemplo, si defines `base_link` como `Component1` al crear los joints, aparecerá un error como:

```text
KeyError: base_link__1
```

También asegúrate de que los componentes de tu modelo contengan **únicamente cuerpos (`bodies`)**.

Los **componentes anidados (`Nested components`) no son compatibles**.

### Esto funciona:

Un componente que contiene únicamente cuerpos.

### Esto no funciona:

Un componente que contiene otros componentes.

Por ejemplo, si el componente `"face (3):1"` contiene otros componentes, no funcionará.

**Cada componente debe contener únicamente cuerpos.**

En algunas ocasiones, este script puede generar un URDF anormal sin mostrar ningún mensaje de error.

En ese caso, probablemente exista un problema con los joints. Vuelve a definir los joints y ejecuta nuevamente el script.

Además, ten en cuenta que actualmente este script solo admite los siguientes tipos de joint:

* `Rigid`
* `Slider`
* `Revolute`

---

# Bucles cinemáticos complejos y joints esféricos

## ⚠️ NO utilices el editor de joints integrado de Fusion 360 para posicionar los joints

Por ejemplo, [@rohit-kumar-j](https://github.com/rohit-kumar-j) tenía que ensamblar un robot complejo con más de 50 joints, incluyendo algunos que formaban bucles dentro de la estructura, como un mecanismo de cuatro barras, también conocido como **bucle cinemático (`kinematic loop`)**.

Cuando Fusion 360 crea inicialmente los joints, es posible que estos no queden alineados exactamente donde deseas.

Por ejemplo, en la imagen original, la tapa del cilindro no coincide exactamente con la posición del pasador donde debe realizarse la unión. La flecha roja muestra la discrepancia en la posición inicial del joint realizada por Fusion 360.

Si arrastras manualmente las piezas y las alineas como corresponde, esto puede provocar problemas en cadena con las propiedades visuales y de colisión de determinados links.

A continuación se puede observar uno de los cilindros desalineado respecto de los demás.

El URDF mostrado en el ejemplo fue visualizado en PyBullet.

## Solución

**La solución consiste en dejar sin modificar los controles de los joints de Fusion 360 y crear los joints correspondientes a los joints del robot**, como se muestra en el ejemplo.

Un problema similar con otro conjunto de joints en el tobillo fue solucionado siguiendo este mismo procedimiento.

Para obtener más información, se puede consultar el video indicado en el repositorio original.

---

# Joints esféricos

Para los joints esféricos, es preferible mantenerlos como joints `Revolute` durante la exportación y posteriormente definirlos como joints esféricos en el URDF generado.

Esto depende de que el parser URDF del visualizador o motor de física utilizado sea compatible con joints esféricos.

Entre los motores mencionados se encuentran:

* Gazebo
* Webots
* PyBullet
* MuJoCo

En el ejemplo del tobillo existen cuatro joints esféricos. Solo dos de ellos fueron definidos como `Revolute` durante la exportación desde Fusion 360.

Los otros dos joints esféricos fueron creados posteriormente en PyBullet utilizando sus funciones integradas para crear bucles cinemáticos.

---

# En algunos casos, desactiva "Capture Design History" antes de exportar

Para planificar previamente la posición de los componentes cuando estés trabajando o ensamblando tu propio robot, se recomienda:

1. Utilizar nombres separados para los componentes.
2. Guardar los componentes individuales en una carpeta independiente.
3. Crear una copia de seguridad.
4. Romper el vínculo (`Break Link`) con el original.

Esta carpeta puede eliminarse posteriormente después de generar el URDF.

Consulta el [Issue #51](https://github.com/syuntoku14/fusion2urdf/issues/51) para obtener información sobre problemas relacionados con `copy-paste` frente a `copy-paste new`.

---

# Cómo utilizarlo

Como ejemplo, se exportará un archivo URDF a partir de este modelo de brazo robótico de Fusion 360:

https://grabcad.com/library/industrial-robot-10

El modelo fue creado por [Sanket Patil](https://grabcad.com/sanket.patil-16).

## Instalación desde la terminal

Ejecuta el [comando de instalación](#instalación) en tu terminal.

---

# Ejecutar en Fusion 360

En Fusion 360, haz clic en:

**ADD-INS → fusion2urdf**

> **Este script modificará tu modelo. Por lo tanto, antes de ejecutarlo, crea una copia de seguridad de tu modelo.**

Ejecuta el script y espera unos segundos (o unos minutos).

Después aparecerá una ventana para seleccionar una carpeta.

Selecciona dónde quieres guardar el URDF. En el ejemplo original se selecciona la carpeta:

```text
Desktop/test
```

Es posible que aparezca algún error al ejecutar el script. Corrígelo siguiendo las instrucciones indicadas.

En el ejemplo original, había un problema con el joint `"Rev 7"`. Probablemente podía solucionarse simplemente redefiniendo el joint.

---

# Definir el `base_link`

**Debes definir el componente base.**

Renombra el componente base como:

```text
base_link
```

En el ejemplo, `base_link` aparece inicialmente como grounded.

Haz clic derecho sobre él y selecciona:

**Unground**

Después de esto puedes ejecutar el script.

Selecciona la carpeta donde deseas guardar los archivos y espera unos segundos.

En el campo de componentes aparecerán muchos elementos llamados `"old_components"`. **Ignóralos.**

Si todo funciona correctamente, habrás exportado exitosamente el URDF.

También obtendrás los archivos `.stl` en la carpeta:

```text
Desktop/test/mm_stl
```

Estos archivos serán necesarios para el siguiente paso.

El archivo CAD original de Fusion 360 ya no es necesario para continuar con el proceso y puede eliminarse si ya tienes una copia de seguridad.

La carpeta:

```text
Desktop/test
```

será necesaria en el siguiente paso.

Debes trasladarla a tu entorno ROS.

---

# En tu entorno ROS

Coloca el directorio del paquete `_description` generado dentro de tu propio workspace de ROS.

En el ejemplo se utiliza:

```text
catkin_ws
```

Luego ejecuta `catkin_make`:

```bash
cd ~/catkin_ws/
catkin_make
source devel/setup.bash
```

Ahora podrás visualizar tu robot en RViz mediante:

```bash
roslaunch (whatever your robot_name is)_description display.launch
```

Por ejemplo, si el nombre del robot fuera `robot_ejemplo`:

```bash
roslaunch robot_ejemplo_description display.launch
```

Si quieres simular tu robot en Gazebo, ejecuta:

```bash
roslaunch (whatever your robot_name is)_description gazebo.launch
```

---

# ¡Disfruta de tu experiencia con Fusion 360 y ROS!

# Cita

```text
@misc{toshinori2020fusion2urdf,
    author = {Toshinori Kitamura},
    title = {Fusion2URDF},
    year = {2020},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/syuntoku14/fusion2urdf}}
}
```
