"""
==============================================================================
DISEÑO Y APLICACIÓN DE FILTROS DIGITALES: PASA BAJOS, PASA ALTOS Y PASA BANDA
==============================================================================
Este script implementa filtros digitales FIR (Finite Impulse Response) e
IIR (Infinite Impulse Response, método Butterworth) para procesar señales
de prueba compuestas por ruido blanco y componentes senoidales de distintas
frecuencias.

Estructura del código:
    1. Definición de la señal de entrada
    2. Diseño del filtro
    3. Aplicación del filtro a la señal

Librerías utilizadas: numpy, scipy.signal, matplotlib
==============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Semilla para reproducibilidad del ruido blanco
np.random.seed(42)


# ==============================================================================
# 1. DEFINICIÓN DE LA SEÑAL DE ENTRADA
# ==============================================================================
# Se define una señal compuesta por tres componentes de frecuencia distinta
# (baja, media y alta) más ruido blanco gaussiano. Esta señal servirá como
# entrada común para probar los tres tipos de filtro (pasa bajos, pasa altos
# y pasa banda).

fs = 1000.0          # Frecuencia de muestreo [Hz]
T = 1.0              # Duración de la señal [s]
N = int(fs * T)      # Número de muestras
t = np.linspace(0, T, N, endpoint=False)   # Vector de tiempo

# Frecuencias de las componentes senoidales que forman la señal compuesta
f_baja = 5      # Hz  -> componente de baja frecuencia
f_media = 50    # Hz  -> componente de frecuencia media (banda de interés)
f_alta = 200    # Hz  -> componente de alta frecuencia

# Señal compuesta: suma de tres senoidales de distinta frecuencia y amplitud
senal_compuesta = (1.0 * np.sin(2 * np.pi * f_baja * t) +
                    0.8 * np.sin(2 * np.pi * f_media * t) +
                    0.5 * np.sin(2 * np.pi * f_alta * t))

# Ruido blanco gaussiano (media 0, desviación estándar 0.4)
ruido_blanco = 0.4 * np.random.randn(N)

# Señal de prueba final: señal compuesta + ruido blanco
senal_entrada = senal_compuesta + ruido_blanco


def graficar_senal_tiempo_frecuencia(t, senal, fs, titulo, color='tab:blue'):
    """
    Grafica una señal en el dominio del tiempo y su espectro de amplitud
    (dominio de la frecuencia, obtenido mediante FFT).
    """
    fig, (ax_t, ax_f) = plt.subplots(1, 2, figsize=(12, 3.5))

    # --- Dominio del tiempo ---
    ax_t.plot(t, senal, color=color, linewidth=0.8)
    ax_t.set_title(f'{titulo} - Dominio del tiempo')
    ax_t.set_xlabel('Tiempo [s]')
    ax_t.set_ylabel('Amplitud')
    ax_t.grid(True, alpha=0.3)

    # --- Dominio de la frecuencia (FFT) ---
    n = len(senal)
    fft_vals = np.fft.rfft(senal)
    fft_freqs = np.fft.rfftfreq(n, d=1 / fs)
    fft_mag = np.abs(fft_vals) / n

    ax_f.plot(fft_freqs, fft_mag, color=color, linewidth=0.9)
    ax_f.set_title(f'{titulo} - Espectro de frecuencia')
    ax_f.set_xlabel('Frecuencia [Hz]')
    ax_f.set_ylabel('Magnitud')
    ax_f.set_xlim(0, fs / 2)
    ax_f.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig


# --- Paso 2 del punto 1: graficar la señal ANTES de aplicar cualquier filtro ---
fig_entrada = graficar_senal_tiempo_frecuencia(
    t, senal_entrada, fs,
    'Señal de entrada (compuesta + ruido blanco)',
    color='tab:blue'
)
fig_entrada.savefig('senal_entrada.png', dpi=130)
plt.close(fig_entrada)


# ==============================================================================
# 2. DISEÑO DEL FILTRO
# ==============================================================================
# Se diseñan dos familias de filtros para cada tipo (pasa bajos, pasa altos
# y pasa banda):
#
#   a) FIR (Finite Impulse Response) mediante el método de ventana
#      (scipy.signal.firwin), usando ventana de Hamming.
#   b) IIR (Infinite Impulse Response) mediante el método Butterworth
#      (scipy.signal.butter), que ofrece respuesta plana en la banda pasante.

nyq = fs / 2.0        # Frecuencia de Nyquist
orden_fir = 101        # Número de taps (orden) del filtro FIR -> debe ser impar
                       # para filtros pasa altos/banda tipo I con ganancia 0 en Nyquist
orden_iir = 4          # Orden del filtro IIR Butterworth

# Frecuencias de corte para cada tipo de filtro (en Hz)
fc_pasa_bajos = 20     # Deja pasar solo la componente de 5 Hz
fc_pasa_altos = 100    # Deja pasar solo la componente de 200 Hz
fc_banda = [30, 80]    # Deja pasar la banda alrededor de 50 Hz

# ------------------------------------------------------------------------
# 2.1 Filtros FIR - método de ventana (Hamming)
# ------------------------------------------------------------------------
fir_pasa_bajos = signal.firwin(orden_fir, fc_pasa_bajos, fs=fs,
                                pass_zero='lowpass', window='hamming')

fir_pasa_altos = signal.firwin(orden_fir, fc_pasa_altos, fs=fs,
                                pass_zero='highpass', window='hamming')

fir_banda = signal.firwin(orden_fir, fc_banda, fs=fs,
                           pass_zero='bandpass', window='hamming')

# ------------------------------------------------------------------------
# 2.2 Filtros IIR - método Butterworth
# ------------------------------------------------------------------------
# Se usa la representación en Second-Order Sections (sos), numéricamente
# más estable que la forma (b, a) clásica, especialmente en órdenes altos.
iir_pasa_bajos = signal.butter(orden_iir, fc_pasa_bajos, btype='lowpass',
                                fs=fs, output='sos')

iir_pasa_altos = signal.butter(orden_iir, fc_pasa_altos, btype='highpass',
                                fs=fs, output='sos')

iir_banda = signal.butter(orden_iir, fc_banda, btype='bandpass',
                           fs=fs, output='sos')


def graficar_respuesta_frecuencia(filtros, fs, titulo):
    """
    Grafica la respuesta en frecuencia (magnitud en dB) de una lista de
    filtros diseñados, para verificar visualmente el diseño antes de
    aplicarlos a la señal.
    filtros: lista de tuplas (nombre, tipo, coeficientes)
             tipo = 'fir' -> coeficientes = b (numerador)
             tipo = 'iir' -> coeficientes = sos
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    for nombre, tipo, coef in filtros:
        if tipo == 'fir':
            w, h = signal.freqz(coef, worN=2048, fs=fs)
        else:  # iir (sos)
            w, h = signal.sosfreqz(coef, worN=2048, fs=fs)
        ax.plot(w, 20 * np.log10(np.abs(h) + 1e-12), label=nombre)

    ax.set_title(titulo)
    ax.set_xlabel('Frecuencia [Hz]')
    ax.set_ylabel('Magnitud [dB]')
    ax.set_ylim(-80, 5)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    return fig


fig_resp = graficar_respuesta_frecuencia(
    [('FIR pasa bajos (Hamming)', 'fir', fir_pasa_bajos),
     ('IIR pasa bajos (Butterworth)', 'iir', iir_pasa_bajos),
     ('FIR pasa altos (Hamming)', 'fir', fir_pasa_altos),
     ('IIR pasa altos (Butterworth)', 'iir', iir_pasa_altos),
     ('FIR pasa banda (Hamming)', 'fir', fir_banda),
     ('IIR pasa banda (Butterworth)', 'iir', iir_banda)],
    fs, 'Respuesta en frecuencia de los filtros diseñados'
)
fig_resp.savefig('respuesta_filtros.png', dpi=130)
plt.close(fig_resp)


# ==============================================================================
# 3. APLICACIÓN DEL FILTRO A LA SEÑAL
# ==============================================================================
# Se aplica cada filtro a la señal de entrada:
#   - FIR: se usa filtfilt (filtrado de fase cero) con los coeficientes b
#          del FIR y a=1, ya que un FIR no tiene realimentación.
#   - IIR: se usa sosfiltfilt, versión de filtfilt optimizada para la
#          representación en secciones de segundo orden (sos), evitando
#          desfase y mejorando la estabilidad numérica.

# --- Pasa bajos ---
salida_fir_pb = signal.filtfilt(fir_pasa_bajos, [1.0], senal_entrada)
salida_iir_pb = signal.sosfiltfilt(iir_pasa_bajos, senal_entrada)

# --- Pasa altos ---
salida_fir_pa = signal.filtfilt(fir_pasa_altos, [1.0], senal_entrada)
salida_iir_pa = signal.sosfiltfilt(iir_pasa_altos, senal_entrada)

# --- Pasa banda ---
salida_fir_bp = signal.filtfilt(fir_banda, [1.0], senal_entrada)
salida_iir_bp = signal.sosfiltfilt(iir_banda, senal_entrada)


def comparar_antes_despues(t, senal_original, salida_fir, salida_iir, fs, titulo):
    """
    Genera una figura comparativa de 3 filas (original, FIR, IIR) mostrando
    tiempo y espectro para cada una, facilitando el análisis del efecto del
    filtrado.
    """
    fig, axes = plt.subplots(3, 2, figsize=(12, 9))
    señales = [
        ('Original (sin filtrar)', senal_original, 'tab:blue'),
        ('Filtrada - FIR (ventana Hamming)', salida_fir, 'tab:green'),
        ('Filtrada - IIR (Butterworth)', salida_iir, 'tab:red'),
    ]

    n = len(senal_original)
    fft_freqs = np.fft.rfftfreq(n, d=1 / fs)

    for i, (nombre, s, color) in enumerate(señales):
        axes[i, 0].plot(t, s, color=color, linewidth=0.8)
        axes[i, 0].set_title(f'{nombre} - Tiempo')
        axes[i, 0].set_xlabel('Tiempo [s]')
        axes[i, 0].set_ylabel('Amplitud')
        axes[i, 0].grid(True, alpha=0.3)

        fft_mag = np.abs(np.fft.rfft(s)) / n
        axes[i, 1].plot(fft_freqs, fft_mag, color=color, linewidth=0.9)
        axes[i, 1].set_title(f'{nombre} - Espectro')
        axes[i, 1].set_xlabel('Frecuencia [Hz]')
        axes[i, 1].set_ylabel('Magnitud')
        axes[i, 1].set_xlim(0, fs / 2)
        axes[i, 1].grid(True, alpha=0.3)

    fig.suptitle(titulo, fontsize=13, fontweight='bold')
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    return fig


fig_pb = comparar_antes_despues(t, senal_entrada, salida_fir_pb, salida_iir_pb, fs,
                                 f'Filtro PASA BAJOS (fc = {fc_pasa_bajos} Hz)')
fig_pb.savefig('comparacion_pasa_bajos.png', dpi=130)
plt.close(fig_pb)

fig_pa = comparar_antes_despues(t, senal_entrada, salida_fir_pa, salida_iir_pa, fs,
                                 f'Filtro PASA ALTOS (fc = {fc_pasa_altos} Hz)')
fig_pa.savefig('comparacion_pasa_altos.png', dpi=130)
plt.close(fig_pa)

fig_bp = comparar_antes_despues(t, senal_entrada, salida_fir_bp, salida_iir_bp, fs,
                                 f'Filtro PASA BANDA (fc = {fc_banda} Hz)')
fig_bp.savefig('comparacion_pasa_banda.png', dpi=130)
plt.close(fig_bp)


print("Proceso completado. Se generaron las siguientes imágenes:")
print(" - senal_entrada.png          (señal antes del filtrado)")
print(" - respuesta_filtros.png      (respuesta en frecuencia de los diseños)")
print(" - comparacion_pasa_bajos.png (antes/después, FIR e IIR)")
print(" - comparacion_pasa_altos.png (antes/después, FIR e IIR)")
print(" - comparacion_pasa_banda.png (antes/después, FIR e IIR)")
