# ⚡ Digital Line Coding & Spectral Analysis Simulation Project

This project contains the complete implementation, interactive applications, spectral estimators, and visual diagrams for **6 standard digital line codes** generated from scratch (without toolbox encoders):

1. **Unipolar NRZ (Non-Return-to-Zero)**
2. **Polar NRZ (NRZ-L)**
3. **Unipolar RZ (Return-to-Zero)**
4. **Polar RZ**
5. **Bipolar AMI (Alternate Mark Inversion)**
6. **Manchester (Biphase-L, IEEE 802.3)**

---

## 📁 Project Directory Contents

### 🌐 1. Interactive Web Applications (Open in Any Browser)
* **`line_coding_interactive_suite.html`**: The flagship interactive application featuring:
  * 📺 **Moving Oscilloscope**: 60 FPS real-time streaming waveforms with play/pause, speed adjustments, and Tx clock alignment.
  * 📈 **Welch PSD Spectral Analyzer**: Live one-sided power spectral density calculation with Linear and Logarithmic (dB) scale overlays.
  * 📋 **Diagnostics & Comparison Matrix**: Live DC component $\mu_V$, AC power, transition density, and baseline wander indicators.
* **`moving_waveform_simulator.html`**: Dedicated multi-channel real-time oscilloscope simulator.
* **`line_code_visualizer.html`**: Instant static bit-sequence webform and waveform generator.

---

### 🐍 2. Python Simulation Scripts
* **`line_coding_analysis.py`**:
  * Vectorized NumPy generation of all 6 line codes.
  * Welch's PSD spectral estimation (`scipy.signal.welch` with Hann window and 50% overlap).
  * Analytical theoretical PSD overlay curves.
  * Generates high-resolution PNG plots.
* **`create_animated_waveform.py`**:
  * Matplotlib animation engine creating continuous moving waveform GIFs.

---

### 🖼️ 3. Generated Visualizations & Media
* **`line_codes_time_domain.png`**: High-resolution time-domain comparison for `[1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1]`.
* **`line_codes_psd_welch.png`**: Power Spectral Density comparison on both Linear and Logarithmic (dB) scales.
* **`line_codes_psd_individual.png`**: 6-panel verification overlaying empirical Welch PSD on top of theoretical spectra.
* **`moving_line_codes.gif`**: Animated moving waveform showing real-time digital transmission.

---

## 📊 Summary Comparison Table

| Line Code | Polarity / Levels | DC Component ($f=0$) | Null Bandwidth | Self-Clocking | Error Detection / Key Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Unipolar NRZ** | Unipolar ($0, +V$) | High ($+V/2$ mean, DC $\delta$) | $R_b$ | Poor (No transitions on 0/1 runs) | Simple digital logic, no AC coupling |
| **Polar NRZ** | Polar ($\pm V$) | Zero mean (Continuous peak @ DC) | $R_b$ | Poor (Fails on long runs) | Standard RS-232, vulnerable to baseline wander |
| **Unipolar RZ** | Unipolar ($0, +V$) | High ($+V/4$ mean) | $2 R_b$ | Good (Discrete clock spike @ $R_b$) | Simple clock recovery via bandpass filter |
| **Polar RZ** | Polar ($+V, 0, -V$) | Zero mean | $2 R_b$ | Good (Pulse in every bit) | Requires 3 voltage levels, $2\times$ bandwidth |
| **Bipolar AMI** | Pseudoternary ($+V, 0, -V$) | Strictly Zero DC ($G(0)=0$) | $R_b$ | Moderate (Sync on 1s only) | Single-bit error detection (AMI violation), T1/E1 |
| **Manchester** | Polar Split-Phase ($\pm V$) | Strictly Zero DC ($G(0)=0$) | $2 R_b$ | Excellent (Mid-bit transition every bit) | Standard in 10BASE-T Ethernet, no baseline wander |

---

## 🚀 How to Run the Python Scripts

Ensure dependencies are installed:
```bash
pip install numpy scipy matplotlib pillow
```

Run the main analysis:
```bash
python line_coding_analysis.py
```

Generate the animated moving GIF:
```bash
python create_animated_waveform.py
```
