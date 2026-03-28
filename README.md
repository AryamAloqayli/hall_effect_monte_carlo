# hall_effect_monte_carlo
Hall Effect experiment analysis with carrier identification and Monte Carlo uncertainty estimation.
---

# Hall Effect Experiment + Monte Carlo Uncertainty Analysis

This project is based on a Hall Effect experiment performed in the lab, followed by computational analysis to extract physical parameters and estimate their uncertainty using Monte Carlo simulation.

The goal is not only to compute quantities like the Hall coefficient and mobility, but also to understand how measurement uncertainty affects the final results.

---

## Overview

The project is divided into two parts:

### Part 1
- Hall voltage vs magnetic field  
- Extraction of Hall coefficient (R_H)  
- Determination of carrier type and concentration  

### Part 2
- Hall voltage vs sample voltage  
- Extraction of mobility  

After that, Monte Carlo simulation is used to propagate experimental uncertainty into the final results.

---

## Experimental Data

The data was obtained from a real Hall Effect experiment.

Measured quantities include:
- Magnetic field (B)
- Hall voltage (V_h)
- Sample voltage (V_x)
- Current (I)

---

## Physics Background

The Hall coefficient is given by:

R_H = (d / I) * (dV_h / dB)

Carrier concentration:

n = 1 / (q |R_H|)

Mobility:

μ = (L / W) * (1 / B) * (dV_h / dV_x)

---

## Results

### Hall Coefficient

R_H ≈ -5.41 × 10⁻³ m³/C

Since R_H is negative:

→ The majority charge carriers are **electrons**

---

### Carrier Concentration

n ≈ 1.15 × 10²¹ m⁻³

---

### Mobility

μ ≈ -0.2509 m²/(V·s)

---

### Model Fit Quality

R² ≈ 0.999

The linear model fits the experimental data very well, indicating strong linear dependence between variables.

---

## Data Analysis

### Hall Voltage vs Magnetic Field

- Clear linear relationship  
- Positive and negative B values produce symmetric behavior  
- Confirms expected Hall Effect behavior  

---

### Hall Voltage vs Sample Voltage

- Linear relationship observed  
- Used to extract mobility  
- Small deviations likely due to experimental noise  

---

## Monte Carlo Uncertainty Analysis

To improve reliability, uncertainty was propagated using Monte Carlo simulation:

- Experimental values were randomly perturbed  
- Linear fits were recomputed thousands of times  
- Distributions of results were analyzed  

---

### Hall Coefficient Distribution

- Approximately Gaussian  
- Small spread → stable measurement  
- Indicates low uncertainty in R_H  

---

### Carrier Concentration Distribution

- Centered around calculated value  
- Slight spread due to uncertainty in slope  

---

### Mobility Distribution

- Also approximately Gaussian  
- Narrow spread → consistent estimation  

---

### Monte Carlo Simulated Fits

- Multiple fitted lines overlap closely  
- Shows robustness of the linear model  
- Confirms that noise does not significantly affect slope  

---

## Key Insights

- The experiment confirms **electron conduction** (negative Hall coefficient)  
- Linear relationships validate the theoretical model  
- Monte Carlo shows that results are **statistically stable**  
- Uncertainty is small relative to measured values  

---

## Why Monte Carlo?

Instead of reporting a single value, Monte Carlo allows:

- estimation of uncertainty  
- visualization of variability  
- understanding sensitivity to measurement noise  

This makes the analysis more realistic and closer to actual research practice.

