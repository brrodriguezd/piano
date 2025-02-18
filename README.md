# Piano Digital en Python

## Descripción
Este proyecto es un piano digital interactivo implementado en Python utilizando `pygame` para la interfaz gráfica y `numpy` junto con `sounddevice` para la síntesis y reproducción de sonido. También incluye funcionalidad para grabar y reproducir notas, y utiliza `scipy` para guardar archivos `.wav`.

## Instalación
### 1. Clonar el repositorio
```bash
git clone https://github.com/brrodriguezd/piano.git
cd piano
```

### 2. Instalar dependencias
Asegúrate de tener Python 3 instalado. Luego, instala las bibliotecas necesarias:
```bash
pip install -r requirements.txt
```

## Uso
### 1. Ejecutar el piano digital
Para lanzar el piano interactivo, ejecuta:
```bash
python piano.py
```
Se abrirá una ventana donde puedes tocar las notas usando el teclado o haciendo clic con el mouse.

## Funcionalidades
### `notas.py`
- Genera señales sinusoidales para notas musicales.
- Guarda los sonidos en archivos `.wav` usando `scipy`.
- Permite la reproducción de sonidos generados.
- Permite reproducir la secuencia de notas grabadas.

### `piano.py`
- Implementa un piano digital con teclas blancas y negras.
- Reproduce sonidos de notas cuando se presionan teclas o clics en la interfaz.
- Graba las notas tocadas en `notes.txt` con marcas de tiempo relativas.
- **Tecla `ESPACIO`**: Inicia y detiene la grabación de notas en `notes.txt`.

## Controles
- **Teclas blancas:** Se tocan con las teclas `A` a `L`.
- **Teclas negras:** Se tocan con las teclas `W` a `P`.
- **Clic del mouse:** También permite tocar las teclas.
- **Espacio (`SPACEBAR`)**: Inicia y detiene la grabación de notas.

## Notas registradas y reproducción
Las notas tocadas se guardan en `notes.txt` con su tiempo relativo. Para reproducir la grabación:
```bash
python notas.py
```
Esto leerá `notes.txt` y reproducirá la secuencia en tiempo real.

## Créditos
Proyecto desarrollado como una demostración de síntesis de audio en Python para la asignatura teoría de la información

