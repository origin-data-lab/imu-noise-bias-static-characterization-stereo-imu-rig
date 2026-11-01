# Methodology
* Static: 1 s windows, max per-axis gyro std < 0.06 rad/s, runs ≥ 60 s, 2 s trimmed per edge.
* Overlapping Allan deviation on rate samples; taus log-spaced from 2/fs to duration/4.
* White noise N = median of adev(τ)·√τ for τ ∈ {0.05, 0.1, 0.2, 0.5, 1} s.
* Per-sample estimate (Kalibr convention σ_d = σ_c·√fs): σ_c = std/√fs — shown for contrast.
* Bias instability: raw Allan minimum (no 0.664 factor).
* Spectrum: Welch, 4096-sample Hann windows, one-sided ASD.
