"""A8 — IMU noise and bias from static segments (ZXIMU v6).

Static detection: 1 s windows, max per-axis gyro std < 0.06 rad/s; segments >= 60 s kept
(edges trimmed 2 s). For each segment: per-axis mean (bias), white-noise density from
Allan deviation at tau=1 s, Allan curve (overlapping), quantisation of gyro values,
bias drift (10 s block means), accel-norm.
Run: PYTHONPATH=. python3 a8_imu_static.py OUT_DIR IMU_FILE [IMU_FILE ...]
"""
import sys, os
import numpy as np, pandas as pd
from read_zximu import load

OUT = sys.argv[1]; FILES = sys.argv[2:]; os.makedirs(OUT, exist_ok=True)
AX = 'xyz'

def oadev(x, fs, taus):
    """Overlapping Allan deviation of rate samples x (sampling fs)."""
    th = np.cumsum(np.r_[0, x]) / fs; N = len(th); out = []
    for tau in taus:
        m = int(round(tau * fs))
        if m < 1 or 2 * m >= N: out.append(np.nan); continue
        d = th[2 * m:] - 2 * th[m:-m] + th[:-2 * m]
        out.append(np.sqrt(np.sum(d ** 2) / (2 * (m / fs) ** 2 * (N - 2 * m))))
    return np.array(out)

def segments(G, fs, thr=0.06, min_s=60, trim=2):
    w = int(round(fs)); n = len(G) // w
    st = G[:n * w].reshape(n, w, 3).std(1).max(1) < thr
    segs, i = [], 0
    while i < n:
        if st[i]:
            j = i
            while j < n and st[j]: j += 1
            if j - i >= min_s: segs.append(((i + trim) * w, (j - trim) * w))
            i = j
        else: i += 1
    return segs

seg_rows, allan_rows, drift_rows = [], [], []
for p in FILES:
    r, _ = load(p); name = os.path.basename(p)[:-4]
    g = r[r['k1'] == 2]; a = r[r['k1'] == 4]
    tg = g['ts'].astype(np.int64); ta = a['ts'].astype(np.int64)
    fs_g = 1e6 / np.median(np.diff(tg)); fs_a = 1e6 / np.median(np.diff(ta))
    G = np.c_[g['x'], g['y'], g['z']].astype(np.float64); A = np.c_[a['x'], a['y'], a['z']].astype(np.float64)
    for si, (i0, i1) in enumerate(segments(G, fs_g)):
        t0, t1 = tg[i0], tg[i1 - 1]
        ja = (ta >= t0) & (ta <= t1)
        segid = f'{name}#{si}'
        Gs, As = G[i0:i1], A[ja]
        dur = (t1 - t0) / 1e6
        row = dict(segment=segid, file=name, start_s=(t0 - tg[0]) / 1e6, duration_s=dur, gyro_rate_hz=fs_g, accel_rate_hz=fs_a,
                   gyro_samples=len(Gs), accel_samples=len(As), accel_norm_mean=np.linalg.norm(As.mean(0)))
        taus = np.unique(np.round(np.logspace(np.log10(2 / fs_g), np.log10(dur / 4), 40), 4))
        for sname, X, fs in (('gyro', Gs, fs_g), ('accel', As, fs_a)):
            for k in range(3):
                x = X[:, k]
                ad = oadev(x, fs, taus)
                for tau, v in zip(taus, ad): allan_rows.append(dict(segment=segid, sensor=sname, axis=AX[k], tau_s=tau, adev=v))
                n1 = oadev(x, fs, [1.0])[0]  # white-noise density ~ adev(1 s) for slope -1/2
                i_min = np.nanargmin(ad)
                row[f'{sname}_{AX[k]}_mean'] = x.mean(); row[f'{sname}_{AX[k]}_std'] = x.std()
                row[f'{sname}_{AX[k]}_adev_1s'] = n1
                row[f'{sname}_{AX[k]}_noise_density_from_sample_std'] = x.std() / np.sqrt(fs)  # Kalibr convention sigma_d = sigma_c*sqrt(fs)
                tt = np.array([0.05, 0.1, 0.2, 0.5, 1.0]); row[f'{sname}_{AX[k]}_N_fit'] = np.median(oadev(x, fs, tt) * np.sqrt(tt))
                row[f'{sname}_{AX[k]}_lag1_autocorr'] = np.corrcoef(x[:-1], x[1:])[0, 1]
                F = np.abs(np.fft.rfft(x - x.mean())) ** 2; fr = np.fft.rfftfreq(len(x), 1 / fs)
                row[f'{sname}_{AX[k]}_psd_ratio_150hz_to_1_20hz'] = F[fr >= 150].mean() / F[(fr >= 1) & (fr < 20)].mean()
                row[f'{sname}_{AX[k]}_adev_min'] = ad[i_min]; row[f'{sname}_{AX[k]}_tau_at_min_s'] = taus[i_min]
                row[f'{sname}_{AX[k]}_unique_values'] = len(np.unique(x))
                # 10 s block means: bias drift
                b = int(10 * fs); nb = len(x) // b
                bm = x[:nb * b].reshape(nb, b).mean(1)
                row[f'{sname}_{AX[k]}_drift_10s_range'] = bm.max() - bm.min()
                for bi, v in enumerate(bm): drift_rows.append(dict(segment=segid, sensor=sname, axis=AX[k], t_s=row['start_s'] + 10 * bi + 5, mean=v))
        # gyro quantisation step
        d = np.diff(np.unique(np.round(Gs[:, 0], 9))); row['gyro_lsb_rad_s'] = np.median(d[d > 1e-9])
        da = np.diff(np.unique(np.round(As[:, 0], 9))); row['accel_lsb_m_s2'] = np.median(da[da > 1e-9])
        seg_rows.append(row)
        print(segid, f'{dur:.0f}s', 'gyro adev1s', [f"{row[f'gyro_{c}_adev_1s']:.5f}" for c in AX], 'acc adev1s', [f"{row[f'accel_{c}_adev_1s']:.5f}" for c in AX], 'norm %.3f' % row['accel_norm_mean'])

S = pd.DataFrame(seg_rows); S.to_csv(f'{OUT}/a8_static_segments.csv', index=False, float_format='%.6g')
pd.DataFrame(allan_rows).to_csv(f'{OUT}/a8_allan.csv', index=False, float_format='%.6g')
pd.DataFrame(drift_rows).to_csv(f'{OUT}/a8_bias_drift_10s.csv', index=False, float_format='%.6g')
