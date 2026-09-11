import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

# Ensure reproducibility
np.random.seed(42)

def generate_line_codes(bits, spb=64, V=1.0):
    """
    Generate 6 standard line codes from a binary sequence without using any communications toolbox.
    
    Parameters:
        bits (np.ndarray): 1D array of binary digits (0 and 1).
        spb (int): Samples per bit duration (Tb).
        V (float): Peak voltage level.
        
    Returns:
        dict: Line code name -> 1D numpy array of waveform samples.
    """
    N = len(bits)
    half_s = spb // 2
    
    # 1. Unipolar NRZ (Non-Return-to-Zero)
    unipolar_nrz = np.repeat(bits * V, spb)
    
    # 2. Polar NRZ (NRZ-L)
    polar_nrz = np.repeat(np.where(bits == 1, V, -V), spb)
    
    # 3. Unipolar RZ (Return-to-Zero)
    u_rz_2d = np.zeros((N, spb), dtype=np.float64)
    u_rz_2d[:, :half_s] = (bits * V)[:, None]
    unipolar_rz = u_rz_2d.flatten()
    
    # 4. Polar RZ
    p_rz_2d = np.zeros((N, spb), dtype=np.float64)
    p_rz_2d[:, :half_s] = np.where(bits == 1, V, -V)[:, None]
    polar_rz = p_rz_2d.flatten()
    
    # 5. Bipolar AMI (Alternate Mark Inversion, NRZ)
    ami_symbols = np.zeros(N, dtype=np.float64)
    mark_indices = np.where(bits == 1)[0]
    if len(mark_indices) > 0:
        ami_symbols[mark_indices] = V * ((-1.0) ** np.arange(len(mark_indices)))
    bipolar_ami = np.repeat(ami_symbols, spb)
    
    # 6. Manchester (Split-phase / Biphase-L, IEEE 802.3)
    man_2d = np.zeros((N, spb), dtype=np.float64)
    man_2d[:, :half_s] = np.where(bits == 1, V, -V)[:, None]
    man_2d[:, half_s:] = np.where(bits == 1, -V, V)[:, None]
    manchester = man_2d.flatten()
    
    return {
        "Unipolar NRZ": unipolar_nrz,
        "Polar NRZ": polar_nrz,
        "Unipolar RZ": unipolar_rz,
        "Polar RZ": polar_rz,
        "Bipolar AMI": bipolar_ami,
        "Manchester": manchester
    }

def sinc(x):
    return np.sinc(x) # np.sinc(x) = sin(pi*x)/(pi*x)

def theoretical_onesided_psd(f_norm, V=1.0):
    """
    Theoretical continuous one-sided normalized PSD G(f) / (V^2 * Tb) as a function of f/Rb.
    For f > 0, G(f) = 2 * S_two_sided(f).
    """
    fn = np.maximum(f_norm, 1e-12)
    
    # One-sided continuous PSDs (factor of 2 included for f > 0)
    # 1. Unipolar NRZ (continuous part)
    psd_u_nrz = 2.0 * (0.25 * (sinc(fn) ** 2))
    
    # 2. Polar NRZ
    psd_p_nrz = 2.0 * (1.0 * (sinc(fn) ** 2))
    
    # 3. Unipolar RZ (continuous part)
    psd_u_rz = 2.0 * (0.0625 * (sinc(fn / 2.0) ** 2))
    
    # 4. Polar RZ
    psd_p_rz = 2.0 * (0.25 * (sinc(fn / 2.0) ** 2))
    
    # 5. Bipolar AMI
    psd_ami = 2.0 * (1.0 * (sinc(fn) ** 2) * (np.sin(np.pi * fn) ** 2))
    
    # 6. Manchester
    psd_man = 2.0 * (1.0 * (sinc(fn / 2.0) ** 2) * (np.sin(np.pi * fn / 2.0) ** 2))
    
    return {
        "Unipolar NRZ": psd_u_nrz,
        "Polar NRZ": psd_p_nrz,
        "Unipolar RZ": psd_u_rz,
        "Polar RZ": psd_p_rz,
        "Bipolar AMI": psd_ami,
        "Manchester": psd_man
    }

def main():
    Rb = 1000.0         # Bit rate = 1000 bps
    Tb = 1.0 / Rb       # Bit duration = 1 ms
    spb = 64            # Samples per bit
    Fs = Rb * spb       # Sampling frequency = 64 kHz
    V = 1.0             # Peak voltage
    
    # -------------------------------------------------------------
    # 1. TIME DOMAIN PLOT
    # -------------------------------------------------------------
    demo_bits = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1])
    N_demo = len(demo_bits)
    demo_signals = generate_line_codes(demo_bits, spb=spb, V=V)
    t_demo = np.arange(N_demo * spb) / Fs
    bit_str = ", ".join(map(str, demo_bits))
    
    fig, axes = plt.subplots(6, 1, figsize=(13, 11), sharex=True)
    fig.suptitle(f"Time-Domain Waveforms for Bit Sequence: [{bit_str}]", 
                 fontsize=14, fontweight='bold', y=0.99)
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    for ax, (name, sig), col in zip(axes, demo_signals.items(), colors):
        ax.step(t_demo / Tb, sig, color=col, linewidth=2, where='post', label=name)
        ax.set_ylabel("Amplitude (V)", fontsize=9, fontweight='bold')
        ax.set_ylim(-1.6, 1.6)
        ax.set_yticks([-1.0, 0.0, 1.0])
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(loc="upper right", fontsize=9, framealpha=0.9)
        
        for b_idx, b_val in enumerate(demo_bits):
            ax.axvline(b_idx, color='gray', linestyle=':', alpha=0.4)
            if ax == axes[0]:
                ax.text(b_idx + 0.5, 1.25, str(b_val), fontsize=10, ha='center', va='center', 
                        fontweight='bold', color='navy')
        ax.axvline(N_demo, color='gray', linestyle=':', alpha=0.4)
        
    axes[-1].set_xlabel("Normalized Time ($t / T_b$)", fontsize=11, fontweight='bold')
    axes[-1].set_xlim(0, N_demo)
    plt.tight_layout()
    plt.savefig("c:/Users/majum/Music/line_codes_time_domain.png", dpi=300)
    plt.close()
    
    # -------------------------------------------------------------
    # 2. WELCH PSD ESTIMATION (OVERLAY)
    # -------------------------------------------------------------
    N_bits_psd = 65536
    random_bits = np.random.randint(0, 2, size=N_bits_psd)
    psd_signals = generate_line_codes(random_bits, spb=spb, V=V)
    
    nperseg = 4096
    noverlap = 2048
    
    fig, (ax_linear, ax_db) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle("Estimated Normalized Power Spectral Density (PSD) using Welch's Method", 
                 fontsize=14, fontweight='bold')
    
    for (name, sig), col in zip(psd_signals.items(), colors):
        f, psd = welch(sig, fs=Fs, window='hann', nperseg=nperseg, noverlap=noverlap, 
                       scaling='density', return_onesided=True)
        f_norm = f / Rb
        mask = (f_norm >= 0) & (f_norm <= 3.5)
        psd_normalized = psd / (V**2 * Tb)
        
        ax_linear.plot(f_norm[mask], psd_normalized[mask], label=name, color=col, linewidth=1.8)
        psd_db = 10 * np.log10(np.maximum(psd_normalized[mask], 1e-6))
        ax_db.plot(f_norm[mask], psd_db, label=name, color=col, linewidth=1.8)
        
    ax_linear.set_title("PSD on Linear Scale ($G(f) / [V^2 T_b]$)", fontsize=12, fontweight='bold')
    ax_linear.set_xlabel("Normalized Frequency ($f / R_b$)", fontsize=11, fontweight='bold')
    ax_linear.set_ylabel("Normalized One-Sided PSD", fontsize=11, fontweight='bold')
    ax_linear.set_xlim(0, 3.5)
    ax_linear.set_ylim(0, 2.3)
    ax_linear.grid(True, linestyle='--', alpha=0.6)
    ax_linear.legend(loc='upper right', fontsize=9.5)
    
    ax_db.set_title("PSD on Logarithmic Scale (dB)", fontsize=12, fontweight='bold')
    ax_db.set_xlabel("Normalized Frequency ($f / R_b$)", fontsize=11, fontweight='bold')
    ax_db.set_ylabel("Normalized PSD (dB)", fontsize=11, fontweight='bold')
    ax_db.set_xlim(0, 3.5)
    ax_db.set_ylim(-35, 10)
    ax_db.grid(True, which='both', linestyle='--', alpha=0.6)
    ax_db.legend(loc='upper right', fontsize=9.5)
    
    plt.tight_layout()
    plt.savefig("c:/Users/majum/Music/line_codes_psd_welch.png", dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 3. INDIVIDUAL COMPARISON: WELCH ESTIMATE VS THEORETICAL PSD
    # -------------------------------------------------------------
    fig, axes = plt.subplots(2, 3, figsize=(16, 9.5))
    fig.suptitle("Welch's Estimated PSD vs Theoretical Spectral Shape for Each Line Code", 
                 fontsize=14, fontweight='bold')
    axes = axes.flatten()
    
    f_theory = np.linspace(0.001, 3.0, 1000)
    theo_dict = theoretical_onesided_psd(f_theory, V=V)
    
    for i, ((name, sig), col) in enumerate(zip(psd_signals.items(), colors)):
        ax = axes[i]
        f, psd = welch(sig, fs=Fs, window='hann', nperseg=nperseg, noverlap=noverlap, 
                       scaling='density', return_onesided=True)
        f_norm = f / Rb
        mask = (f_norm >= 0) & (f_norm <= 3.0)
        psd_norm = psd / (V**2 * Tb)
        
        ax.plot(f_norm[mask], psd_norm[mask], color=col, linewidth=2.0, label='Welch Estimate')
        ax.plot(f_theory, theo_dict[name], color='black', linestyle='--', linewidth=1.5, label='Theory (Continuous)')
        ax.set_title(name, fontsize=11, fontweight='bold')
        ax.set_xlabel("Normalized Frequency ($f / R_b$)", fontsize=9.5)
        ax.set_ylabel("One-Sided PSD ($G(f)/V^2 T_b$)", fontsize=9.5)
        ax.set_xlim(0, 3.0)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='upper right', fontsize=8.5)
        
    plt.tight_layout()
    plt.savefig("c:/Users/majum/Music/line_codes_psd_individual.png", dpi=300)
    plt.close()
    
    print("All plots re-generated successfully with exact 1-sided PSD matching!")

if __name__ == "__main__":
    main()
