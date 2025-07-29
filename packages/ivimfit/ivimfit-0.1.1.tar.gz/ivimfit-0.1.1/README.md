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

For local development:

```bash
pip install ivimfit .

Example:
    import numpy as np
    from ivimfit.biexp import fit_biexp_free
    from ivimfit.utils import plot_fit, calculate_r_squared
    from ivimfit.biexp import biexp_model
    import matplotlib.pyplot as plt

    # Simulated IVIM signal
    b = np.array([0, 50, 100, 200, 400, 600, 800])
    s = 0.12 * np.exp(-b * 0.02) + 0.88 * np.exp(-b * 0.0012)

    # Fit
    f, D, D_star = fit_biexp_free(b, s, omit_b0=False)

    # Plot
    fig, ax = plot_fit(b, s, biexp_model, [f, D, D_star], model_name="IVIM Free Fit")
    plt.show()

