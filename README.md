# URDF Exporter para Fusion 360

Este proyecto es un **fork** del repositorio original: [syuntoku14/fusion2urdf](https://github.com/syuntoku14/fusion2urdf). Incluye soporte para versiones recientes de Fusion 360, scripts para la preparación de modelos hacia **MuJoCo** y directrices detalladas de diseño.

## ¿Qué hace este script?

Permite exportar modelos mecánicos directamente desde Autodesk Fusion 360 generando:

* Un archivo `.urdf` del modelo cinemático.

* Mallas `.stl` correspondientes a cada link.

* Archivos `.launch` y `.yaml` para simulación en Gazebo / ROS.

## Reglas de diseño y preparación en Fusion 360

### 1. Jerarquía de componentes

* **Cada link debe ser un componente independiente que contenga únicamente cuerpos (`bodies`).**

* **NO se admiten componentes anidados ni subensambles.** Si se diseña un link agrupando piezas (por ejemplo, estructura + servomotores), se debe combinar los cuerpos o consolidarlos en un único componente sin subcomponentes internos antes de ensamblar.


### 2. Nomenclatura

* La link base del robot debe llamarse **`base_link`**.

* Los links sucesivos deben nombrarse secuencialmente: **`link1`**, **`link2`**, ..., **`linkN`**.

### 3. Definición de uniones

* **Tipos admitidos:** Únicamente **Rígida (Rigid)**, **Revolución (Revolute)** y **Corredera (Slider)**.

* **Regla Padre-Hijo:**

  * `Component1` = **Link hijo** (`link[n+1]`)

  * `Component2` = **Link padre** (`link[n]`)

* **Sin acentos ni caracteres especiales:** El exportador no procesa tildes. Dado que Fusion en español suele nombrar las uniones como *"Revolución"*, se puede:

  * Cambiar el idioma de Fusion 360 a inglés, o bien

  * Renombrar manualmente cada unión en el navegador para quitar la tilde (ej. `Revolucion 1`).

### 4. Orientación y bloqueos

* **Eje Z hacia arriba:** Se debe verificar que el modelo esté correctamente orientado con el eje Z vertical (se puede añadir una restricción de alineación entre la base y el plano XY).

* **Sin componentes bloqueados:** Se debe verificar que ningún componente esté fijado o bloqueado al momento de exportar.

* **Copia de seguridad:** Se recomienda crear un guardado o duplicado del diseño antes de lanzar el proceso.

A modo de ejemplo, el siguiente ensamble está listo para ser exportado, cumpliendo con todos los requisitos nombrados anteriormente.

<img width="512" height="462" alt="robot_ejemplo" src="https://github.com/user-attachments/assets/4a116798-e1a8-4eb1-959e-90ec795673b5" />

## Instalación

Clona este repositorio o descarga su contenido:

```
git clone https://github.com/nans-rer/fusion2urdf.git

```

Copia la carpeta `URDF_Exporter` al directorio de scripts de Fusion 360 según tu sistema operativo:

### Windows (PowerShell)

```
cd <ruta_hacia_fusion2urdf>
Copy-Item ".\URDF_Exporter\" -Destination "${env:APPDATA}\Autodesk\Autodesk Fusion 360\API\Scripts\" -Recurse

```

### macOS (Terminal)

```
cd <ruta_hacia_fusion2urdf>
cp -r ./URDF_Exporter "$HOME/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/"

```

## Flujo de Exportación

1. En Fusion 360, abre el modelo preparado.

2. Dirígete a la barra superior: **Utilidades** $\rightarrow$ **Complementos** $\rightarrow$ **Secuencias de comandos y complementos** (o presiona `Shift + S`).

3. En la pestaña *Secuencias de comandos*, localiza **URDF_Exporter** y haz clic en **Ejecutar**.

4. Selecciona la carpeta destino donde se generará la carpeta con terminación `_description`.


<img width="600" alt="complementos" src="https://github.com/user-attachments/assets/fc1f1b98-00d2-41ec-9c29-14c0c147308c" />
<img width="600" alt="complementos2" src="https://github.com/user-attachments/assets/52ca8915-8bf5-4724-96e2-c47e22c8820c" />

## Simulación en MuJoCo

Para procesar el URDF resultante y visualizarlo en el entorno de simulación de MuJoCo:

### 1. Preparar el entorno virtual

En la raíz de este proyecto se encuentra un convertidor de URDF a MuJoCo. Se debe abrir la carpeta una terminal (se puede usar VSCode) y abrir la carpeta del convertidor. Una vez dentro se ejecuta el siguiente codigo:

```
# 1.- Crear entorno virtual con Python 3.12+
python -m venv venv

# 2.- Activar entorno (Windows)
.\venv\Scripts\activate
# En Linux/macOS usar: source venv/bin/activate

# 3.- Instalar dependencias
python -m pip install -r requirements.txt

```

### 2. Procesar y cargar el modelo

1. Copia la carpeta generada por el exportador URDF (ej. `robot_description`) dentro de la raíz de este proyecto.

2. Convierte el URDF a formato MuJoCo XML:

   ```
   python preparar_urdf_mujoco.py
   ```

3. Al finalizar, la consola mostrará la ruta del archivo `.xml` generado.

4. Carga la escena interactiva ejecutando:

   ```
   python cargar_escena.py ruta/hacia/el/archivo_generado.xml
   
   ```

## Cita

```
@misc{toshinori2020fusion2urdf,
    author = {Toshinori Kitamura},
    title = {Fusion2URDF},
    year = {2020},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/syuntoku14/fusion2urdf}}
}

```
