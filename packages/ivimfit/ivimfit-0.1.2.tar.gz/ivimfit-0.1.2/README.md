# ivimfit

**ivimfit** is a modular Python library for fitting Intravoxel Incoherent Motion (IVIM) diffusion MRI models.  
It supports monoexponential ADC fitting, biexponential (free and segmented) models, as well as Bayesian inference using PyMC.

Designed for researchers and clinicians working with DWI/IVIM datasets, this package offers signal filtering, robust modeling, and visualization tools for parameter evaluation.

---

## 📦 Features

- ✅ Monoexponential ADC fitting
- ✅ Full biexponential model (nonlinear free fit)
- ✅ Segmented biexponential model (2-step D + [f, D*])
- ✅ Bayesian IVIM modeling using MCMC via PyMC
- ✅ Optional exclusion of b = 0
- ✅ Automatic filtering of b-values > 1000
- ✅ R² calculation and signal-fit visualization utilities

---
## 🧳 License

This project is licensed under the MIT License - see the [LICENSE] file for details.

## 📥 Installation



```bash
pip install ivimfit .

import numpy as np
import matplotlib.pyplot as plt
from ivimfit.utils import plot_fit, calculate_r_squared
from ivimfit.adc import fit_adc, monoexp_model

b = np.array([0, 50, 100, 200, 400, 600, 800])
s = np.array([800, 654,543,423,328,236,121])
#ADC Calculation
adc = fit_adc(b, s)
r2 = calculate_r_squared(s / s[0], monoexp_model(b, adc))

fig, ax = plot_fit(b, s, monoexp_model, [adc], model_name=f"ADC Fit (R² = {r2:.4f})")
plt.show()

#Biexponential Fitting
from ivimfit.biexp import fit_biexp_free, biexp_model

b = np.array([0, 50, 100, 200, 400, 600, 800])
s = np.array([800, 654,543,423,328,236,121])

f, D, D_star = fit_biexp_free(b, s)
r2 = calculate_r_squared(s / s[0], biexp_model(b, f, D, D_star))

fig, ax = plot_fit(b, s, biexp_model, [f, D, D_star], model_name=f"Free Fit (R² = {r2:.4f})")
plt.show()
#Segmented Fitting
from ivimfit.segmented import fit_biexp_segmented, biexp_fixed_D_model

b = np.array([0, 50, 100, 200, 400, 600, 800])
s = np.array([800, 654,543,423,328,236,121])

f, D_fixed, D_star = fit_biexp_segmented(b, s)
r2 = calculate_r_squared(s / s[0], biexp_fixed_D_model(b, f, D_star, D_fixed))

fig, ax = plot_fit(
    b, s,
    lambda b_, f_, D_star_,D_fixed: biexp_fixed_D_model(b_, f_, D_star_, D_fixed),
    [f, D_star,D_fixed],
    model_name=f"Segmented Fit (R² = {r2:.4f})"
)
plt.show()
#Bayesian Approach
from ivimfit.bayesian import fit_bayesian
from ivimfit.biexp import biexp_model

b = np.array([0, 50, 100, 200, 400, 600, 800])
s = np.array([800, 654,543,423,328,236,121])

if __name__ == "__main__":
    f, D, D_star = fit_bayesian(b, s, draws=500, chains=2)
    r2 = calculate_r_squared(s / s[0], biexp_model(b, f, D, D_star))

    fig, ax = plot_fit(b, s, biexp_model, [f, D, D_star], model_name=f"Bayesian Fit (R² = {r2:.4f})")
    plt.show()




