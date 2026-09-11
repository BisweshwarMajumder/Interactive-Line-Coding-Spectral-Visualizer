import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

np.random.seed(42)

def generate_line_codes(bits, spb=32, V=1.0):
    N = len(bits)
    half_s = spb // 2
    
    # 1. Unipolar NRZ
    u_nrz = np.repeat(bits * V, spb)
    # 2. Polar NRZ
    p_nrz = np.repeat(np.where(bits == 1, V, -V), spb)
    # 3. Unipolar RZ
    u_rz_2d = np.zeros((N, spb))
    u_rz_2d[:, :half_s] = (bits * V)[:, None]
    u_rz = u_rz_2d.flatten()
    # 4. Polar RZ
    p_rz_2d = np.zeros((N, spb))
    p_rz_2d[:, :half_s] = np.where(bits == 1, V, -V)[:, None]
    p_rz = p_rz_2d.flatten()
    # 5. Bipolar AMI
    ami_symbols = np.zeros(N)
    mark_indices = np.where(bits == 1)[0]
    if len(mark_indices) > 0:
        ami_symbols[mark_indices] = V * ((-1.0) ** np.arange(len(mark_indices)))
    b_ami = np.repeat(ami_symbols, spb)
    # 6. Manchester
    man_2d = np.zeros((N, spb))
    man_2d[:, :half_s] = np.where(bits == 1, V, -V)[:, None]
    man_2d[:, half_s:] = np.where(bits == 1, -V, V)[:, None]
    man = man_2d.flatten()
    
    return {
        "Unipolar NRZ": u_nrz,
        "Polar NRZ": p_nrz,
        "Unipolar RZ": u_rz,
        "Polar RZ": p_rz,
        "Bipolar AMI": b_ami,
        "Manchester": man
    }

# Parameters for animation
N_total_bits = 40
spb = 32
bits = np.random.randint(0, 2, size=N_total_bits)
signals = generate_line_codes(bits, spb=spb)

fig, axes = plt.subplots(6, 1, figsize=(11, 8), sharex=True)
fig.suptitle("Moving / Streaming Line Codes (Real-Time Oscilloscope View)", fontsize=13, fontweight='bold')

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
lines = []

for ax, (name, sig), col in zip(axes, signals.items(), colors):
    line, = ax.plot([], [], color=col, linewidth=2, label=name)
    lines.append(line)
    ax.set_ylabel("V", fontsize=8, fontweight='bold')
    ax.set_ylim(-1.5, 1.5)
    ax.set_yticks([-1.0, 0, 1.0])
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc="upper right", fontsize=8)

axes[-1].set_xlabel("Time (Bit Periods)", fontsize=10, fontweight='bold')
window_bits = 8
axes[-1].set_xlim(0, window_bits)

num_frames = 60
t_total = len(signals["Unipolar NRZ"])

def update(frame):
    # Shift window across bits
    shift = (frame / num_frames) * (N_total_bits - window_bits - 2) * spb
    start_idx = int(shift)
    end_idx = start_idx + window_bits * spb
    t_win = np.linspace(0, window_bits, window_bits * spb, endpoint=False)
    
    for line, (name, sig) in zip(lines, signals.items()):
        line.set_data(t_win, sig[start_idx:end_idx])
        
    return lines

ani = animation.FuncAnimation(fig, update, frames=num_frames, interval=50, blit=True)
plt.tight_layout()

ani.save("c:/Users/majum/Music/moving_line_codes.gif", writer='pillow', fps=20)
print("Saved moving_line_codes.gif")
