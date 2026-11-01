import os, numpy as np, pandas as pd, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from read_zximu import load
OUT = 'out'; FIG = f'{OUT}/figures'; os.makedirs(FIG, exist_ok=True)
INK, GR = '#1d232b', '#8a8f98'
AXC = {'x': '#1f5fbf', 'y': '#d9622b', 'z': '#2e9e6a'}
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10.5, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True, 'grid.color': '#e7eaee', 'axes.edgecolor': '#c9ced6'})
def save(fig, name): fig.savefig(f'{FIG}/{name}.png', dpi=170, bbox_inches='tight'); fig.savefig(f'{FIG}/{name}.svg', bbox_inches='tight'); plt.close(fig)
PRIM = '20261026_143229_00000#0'
PRIOR = {'gyro': 0.002, 'accel': 0.02}
UNIT = {'gyro': 'rad/s', 'accel': 'm/s²'}
A = pd.read_csv(f'{OUT}/a8_allan.csv'); S = pd.read_csv(f'{OUT}/a8_static_segments.csv').set_index('segment')
dur = S.loc[PRIM, 'duration_s']
for sensor in ['gyro', 'accel']:
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for k in 'xyz':
        d = A[(A.segment == PRIM) & (A.sensor == sensor) & (A.axis == k)].dropna()
        ax.loglog(d.tau_s, d.adev, color=AXC[k], lw=1.8, label=f'{k} axis — N = {S.loc[PRIM, f"{sensor}_{k}_N_fit"]:.5f}')
    t = np.logspace(-2.5, 2.2, 10)
    ax.loglog(t, PRIOR[sensor] / np.sqrt(t), color=INK, ls='--', lw=1, label=f'Calibration-file prior, {PRIOR[sensor]} (white noise only)')
    ax.set_xlabel('Averaging time τ (s)'); ax.set_ylabel(f'Allan deviation ({UNIT[sensor]})')
    ax.set_title(f'{"Gyroscope" if sensor == "gyro" else "Accelerometer"}: one {dur:.0f} s static recording', loc='left', fontsize=11)
    ax.legend(frameon=False, fontsize=8.5, loc='lower left'); save(fig, f'fn14_allan_{sensor}')
# gyro spectrum: why per-sample std misleads on z
r, _ = load('/home/claude/calib2/raw/20261026_143229_00000.imu') if os.path.exists('/home/claude/calib2/raw/20261026_143229_00000.imu') else (None, None)
if r is not None:
    g = r[r['k1'] == 2]; tg = g['ts'].astype(np.int64); fs = 1e6 / np.median(np.diff(tg))
    i0 = int((S.loc[PRIM, 'start_s']) * fs); n = int(dur * fs); seg = np.c_[g['x'], g['y'], g['z']][i0:i0 + n].astype(float)
    fig, ax = plt.subplots(figsize=(7, 3.8)); w = 4096
    rows = []
    for j, k in enumerate('xyz'):
        x = seg[:, j] - seg[:, j].mean(); m = len(x) // w
        P = (np.abs(np.fft.rfft(x[:m * w].reshape(m, w) * np.hanning(w), axis=1)) ** 2).mean(0) * 2 / (fs * (np.hanning(w) ** 2).sum())
        f = np.fft.rfftfreq(w, 1 / fs); ax.semilogy(f[1:], np.sqrt(P[1:]), color=AXC[k], lw=1, label=f'{k} axis')
        rows += [dict(axis=k, f_hz=a, asd=b) for a, b in zip(f[1:], np.sqrt(P[1:]))]
    pd.DataFrame(rows).to_csv(f'{OUT}/a8_gyro_asd.csv', index=False, float_format='%.6g')
    ax.set_xlabel('Frequency (Hz)'); ax.set_ylabel('Amplitude spectral density (rad/s/√Hz)')
    ax.set_title('Gyroscope noise is not flat: z rises toward the Nyquist frequency', loc='left', fontsize=11); ax.legend(frameon=False, fontsize=9)
    save(fig, 'fn14_gyro_spectrum')
# gyro bias per static segment
fig, ax = plt.subplots(figsize=(7, 3.8)); segs = list(S.index); x = np.arange(len(segs)); w = 0.26
for o, k in zip([-w, 0, w], 'xyz'):
    v = np.degrees(S[f'gyro_{k}_mean'].values); ax.bar(x + o, v, w, color=AXC[k], label=f'{k} axis')
ax.axhline(0, color=INK, lw=0.8); ax.set_axisbelow(True); ax.grid(axis='x', visible=False)
lab = [f'{s.split("_")[1][:2]}:{s.split("_")[1][2:4]} seg {s[-1]}\n{S.loc[s, "duration_s"]:.0f} s' for s in segs]
ax.set_xticks(x); ax.set_xticklabels(lab, fontsize=8.5); ax.set_ylabel('Mean gyro output at rest (°/s)')
ax.set_title('Gyroscope bias at rest, five static segments on one day', loc='left', fontsize=11); ax.legend(frameon=False, fontsize=9, ncol=3)
save(fig, 'fn14_gyro_bias')
print('ok')
