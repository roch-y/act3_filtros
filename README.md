# Filtros Digitales en Python (FIR e IIR)
 
Script en Python para el diseño y aplicación de filtros digitales **pasa bajos**, **pasa altos** y **pasa banda**, comparando dos enfoques de diseño:
 
- **FIR** (Finite Impulse Response) mediante el método de ventana (Hamming).
- **IIR** (Infinite Impulse Response) mediante el método **Butterworth**.
## Contenido
 
- `filtros_digitales.py` — script principal.
- `senal_entrada.png` — señal de prueba antes del filtrado (tiempo y espectro).
- `respuesta_filtros.png` — respuesta en frecuencia de los 6 filtros diseñados.
- `comparacion_pasa_bajos.png` — señal original vs. filtrada (FIR e IIR).
- `comparacion_pasa_altos.png` — señal original vs. filtrada (FIR e IIR).
- `comparacion_pasa_banda.png` — señal original vs. filtrada (FIR e IIR).
## Descripción
 
El script genera una señal de prueba compuesta por tres componentes senoidales de distinta frecuencia (5 Hz, 50 Hz y 200 Hz) sumadas a ruido blanco gaussiano. Sobre esta señal se diseñan y aplican filtros digitales para aislar cada rango de frecuencia, comparando el resultado obtenido con FIR e IIR.
 
El código está organizado en tres bloques:
 
1. **Definición de la señal de entrada**: generación de la señal compuesta + ruido, y graficado en tiempo y frecuencia antes de filtrar.
2. **Diseño del filtro**: construcción de los filtros FIR (ventana Hamming) e IIR (Butterworth) para cada tipo (pasa bajos, pasa altos, pasa banda), y verificación de su respuesta en frecuencia.
3. **Aplicación del filtro a la señal**: filtrado de fase cero (`filtfilt` / `sosfiltfilt`) y comparación visual de la señal antes y después del filtrado.
## Requisitos
 
- Python 3.8+
- numpy
- scipy
- matplotlib
Instalación de dependencias:
 
```bash
pip install numpy scipy matplotlib
```
 
## Uso
 
```bash
python filtros_digitales.py
```
 
El script generará automáticamente las 5 imágenes `.png` mencionadas arriba en el mismo directorio.
 
## Parámetros configurables
 
Dentro del script se pueden ajustar fácilmente:
 
| Parámetro | Descripción |
|---|---|
| `fs` | Frecuencia de muestreo (Hz) |
| `f_baja`, `f_media`, `f_alta` | Frecuencias de las componentes de la señal de prueba |
| `fc_pasa_bajos`, `fc_pasa_altos`, `fc_banda` | Frecuencias de corte de cada filtro |
| `orden_fir` | Orden (número de taps) del filtro FIR |
| `orden_iir` | Orden del filtro IIR Butterworth |

## Herramientas de Apoyo 
1. Python. Sitio web: [https://www.python.org/](https://docs.python.org/3/)
2. Anthropic. (2026). Claude (Claude Sonnet 5) [Modelo de lenguaje de gran escala]. https://claude.ai
3. Rodríguez, C. (octubre, 20219). Módulo 1: Numpy - Curso de Python 3 Científico. IAA-CSIC. Enlace del documento: https://python.iaa.csic.es/sites/default/files/material/cientifico/numpy.pdf
4. Rodríguez, C. (octubre, 20219). Matplotlib. IAA-CSIC. Enlace del documento: https://python.iaa.csic.es/sites/default/files/material/cientifico/matplotlib.pdf
5. Rodríguez, C. (octubre, 20219). Curso Python 3 Científico: Scipy - Módulo 3. IAA-CSIC. Enlace del documento: https://python.iaa.csic.es/sites/default/files/material/cientifico/scipy.pdf  
6. Juan S. (Abril 23, 2020). IIR vs FIR: Entendiendo realmente sus diferencias. Sitio web: https://www.juansaudio.com/post/iir-vs-fir-entendiendo-realmente-sus-diferencias.
7. Olin Harris (octubre 10, 2024). Filtrado FIR vs IIR: ¿Qué enfoque es mejor para su aplicación?. SoundScapeHQ. Sitio web: https://soundscapehq.com/es/filtrado-de-abeto-vs-iir/
 
## Licencia
 
Uso libre para fines educativos.
