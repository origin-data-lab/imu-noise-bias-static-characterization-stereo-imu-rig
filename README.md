<!-- ODL_QUALITY_V2 -->

# Origin Data Lab · Technical Field Note #14

**ODL Static IMU Allan Deviation**

[![GitHub](https://img.shields.io/badge/GitHub-Open-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/origin-data-lab/imu-noise-bias-static-characterization-stereo-imu-rig) [![Hugging Face](https://img.shields.io/badge/Hugging_Face-Open-FFD21E?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/datasets/origin-data-lab/imu-noise-bias-static-characterization-stereo-imu-rig) [![Kaggle](https://img.shields.io/badge/Kaggle-Open-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/datasets/origindatalab/odl-static-imu-allan) [![Technical Note](https://img.shields.io/badge/Technical_Note-Open-0B1220?style=for-the-badge&logo=read-the-docs&logoColor=white)](https://origindatalab.io/technical-field-notes/imu-noise-bias-static-characterization-stereo-imu-rig.html)

[English technical note](https://origindatalab.io/technical-field-notes/imu-noise-bias-static-characterization-stereo-imu-rig.html) | [Korean technical note](https://origindatalab.io/ko/technical-field-notes/imu-noise-bias-static-characterization-stereo-imu-rig.html)

---

# ODL Field Note #14 — IMU noise and bias from static recordings
Find still segments inside existing recordings and compute per-axis overlapping Allan deviation, white-noise density, bias instability, bias at rest and spectra.
```bash
pip install numpy pandas matplotlib
cd analysis && PYTHONPATH=. python3 a8_imu_static.py out <file1.imu> [<file2.imu> ...]
PYTHONPATH=. python3 make_figures_14.py
```
Reader for the ZXIMU v6 format: `read_zximu.py` (record layout reverse-engineered; temperature field unconverted). Raw IMU files are not distributed.
Licence: Creative Commons Attribution 4.0 International (CC BY 4.0) for derived data and figures; MIT for code.

## Visual evidence

Figures are taken from the released technical-note package. Interpret with the original methods and limitations.

### Figure 1

![Log-log plot of accelerometer Allan deviation for three axes against a dashed prior line](figures/fn14_allan_accel.png)

*Accelerometer Allan deviation, same segment.*

### Figure 2

![Log-log plot of gyroscope Allan deviation for three axes against a dashed prior line](figures/fn14_allan_gyro.png)

*Gyroscope Allan deviation, 519 s static segment, with the white-noise prior from the calibration file.*

### Figure 3

![Grouped bar chart of gyroscope bias at rest per axis for five static segments](figures/fn14_gyro_bias.png)

*Mean gyro output at rest per axis for each static segment.*

### Figure 4

![Gyroscope amplitude spectral density for three axes from 0 to 250 Hz](figures/fn14_gyro_spectrum.png)

*Gyroscope amplitude spectral density on the static segment (Welch, 4096-sample Hann windows).*


<!-- ODL_ENTITY_V1 -->
## About Origin Data Lab

**Origin Data Lab** (origindatalab.io, OriginDataLab Co., Ltd.) is a real-world data collection company based in **Yangyang, Gangwon State, South Korea**.
We plan and run egocentric, stereo+IMU and field video capture for physical AI and robotics teams, with documented QA such as the measurements in this dataset.
Not affiliated with "Origin Lab" (game data) or "OriginLab" (Origin/OriginPro software).

- **[Request sample data](https://origindatalab.io/contact.html?topic=sample&note=fn14&utm_source=github&utm_medium=referral&utm_campaign=field-notes)**: stereo+IMU or phone+IMU egocentric capture
- **[Custom data collection](https://origindatalab.io/data-services.html?utm_source=github&utm_medium=referral)**: field capture in South Korea and Bangladesh
- **[All technical field notes](https://origindatalab.io/technical-field-notes/?utm_source=github&utm_medium=referral)**

---

## Explore Origin Data Lab

[![GitHub](https://img.shields.io/badge/GitHub-Open-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/origin-data-lab/imu-noise-bias-static-characterization-stereo-imu-rig) [![Hugging Face](https://img.shields.io/badge/Hugging_Face-Open-FFD21E?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/datasets/origin-data-lab/imu-noise-bias-static-characterization-stereo-imu-rig) [![Kaggle](https://img.shields.io/badge/Kaggle-Open-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/datasets/origindatalab/odl-static-imu-allan) [![Technical Note](https://img.shields.io/badge/Technical_Note-Open-0B1220?style=for-the-badge&logo=read-the-docs&logoColor=white)](https://origindatalab.io/technical-field-notes/imu-noise-bias-static-characterization-stereo-imu-rig.html)

[Official Website](https://origindatalab.io/) | [Technical Field Notes](https://origindatalab.io/technical-field-notes/) | [English Note](https://origindatalab.io/technical-field-notes/imu-noise-bias-static-characterization-stereo-imu-rig.html) | [Korean Note](https://origindatalab.io/ko/technical-field-notes/imu-noise-bias-static-characterization-stereo-imu-rig.html)

[GitHub](https://github.com/origin-data-lab/imu-noise-bias-static-characterization-stereo-imu-rig) | [Hugging Face](https://huggingface.co/datasets/origin-data-lab/imu-noise-bias-static-characterization-stereo-imu-rig) | [Kaggle Dataset](https://www.kaggle.com/datasets/origindatalab/odl-static-imu-allan) | [Kaggle Notebook](https://www.kaggle.com/code/origindatalab/odl-static-imu-allan-notebook)
