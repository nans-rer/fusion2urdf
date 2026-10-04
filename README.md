# URDF Exporter para Fusion 360

Este es un **fork** del repositorio original: https://github.com/syuntoku14/fusion2urdf

## **Cambios realizados**

* **Compatibilidad con Fusion 2705.1.25** Se arreglaron problemas de exportación relacionados con cambios realizados a la generación de nombres en Fusion.

## **Notas**

* El script está actualizado para utilizarse con **Python 3.12** y superiores.

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

Es necesario que el robot quede correctamente orientado, asegúrate de que el eje Z esté orientado hacia arriba en tu modelo de Fusion 360.

### Modelo original

<img src="https://github.com/syuntoku14/fusion2urdf/blob/images/industrial_robot.png" alt="industrial_robot" title="industrial_robot" width="300" height="300">

### Simulación en Gazebo del `.urdf` y `.launch` exportados

* Centro de masa.
  
  <img src="https://github.com/syuntoku14/fusion2urdf/blob/images/center_of_mass.png" alt="center_of_mass" title="center_of_mass" width="300" height="300">

* Colisiones.
  
  <img src="https://github.com/syuntoku14/fusion2urdf/blob/images/collision.png" alt="collision" title="collision" width="300" height="300">

* Inercia.
  
  <img src="https://github.com/syuntoku14/fusion2urdf/blob/images/inertia.png" alt="inertia" title="inertia" width="300" height="300">

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
<img src="https://github.com/syuntoku14/fusion2urdf/blob/images/spot_mini.PNG" alt="spot_mini" title="spot_mini" width="300" height="300">

También asegúrate de que los componentes de tu modelo contengan **únicamente cuerpos (`bodies`)**.

Los **componentes anidados (`Nested components`) no son compatibles**.

### Esto funciona:

<img src="https://github.com/syuntoku14/fusion2urdf/blob/images/only_bodies.PNG" alt="only_bodies" title="only_bodies" width="300" height="300">

### Esto no funciona: Pues `"face (3):1"` contiene otros componentes, no funcionará.

<img src="https://github.com/syuntoku14/fusion2urdf/blob/images/nest_components.PNG" alt="nest_components" title="nest_components" width="300" height="300">

**Cada componente debe contener únicamente cuerpos.**

En algunas ocasiones, este script puede generar un URDF anormal sin mostrar ningún mensaje de error.

En ese caso, probablemente exista un problema con los joints. Vuelve a definir los joints y ejecuta nuevamente el script.

Además, ten en cuenta que actualmente este script solo admite los siguientes tipos de joint: “Rígida”, “Revolución” y “Corredera”. 


---

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
