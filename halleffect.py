import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

FIG_DIR = "hall_effect_fig"
os.makedirs(FIG_DIR, exist_ok=True)

df = pd.read_csv("hallexp.csv", sep=";")
df.columns = df.columns.str.strip()

positive_B = df["positive B(mT)"].values
positive_V = df["positive V_h(mV)"].values
negative_B = df["negative B(mT)"].values
negative_V = df["negative V_h(mV)"].values

plt.figure(figsize=(8, 6))
plt.scatter(positive_B, positive_V, color="blue", label="Positive B data")
plt.scatter(negative_B, negative_V, color="red", label="Negative B data")
plt.axhline(0, color="black", linewidth=0.8)
plt.axvline(0, color="black", linewidth=0.8)
plt.xlabel("Magnetic Field B (mT)")
plt.ylabel("Hall Voltage V_h (mV)")
plt.title("Hall Effect: Hall Voltage vs Magnetic Field")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "hall_voltage_vs_magnetic_field.png"), dpi=300)
plt.close()

slope_pos, intercept_pos = np.polyfit(positive_B, positive_V, 1)
slope_neg, intercept_neg = np.polyfit(negative_B, negative_V, 1)

print("Positive B slope:", slope_pos)
print("Negative B slope:", slope_neg)

B_all = np.concatenate([positive_B, negative_B])
V_all = np.concatenate([positive_V, negative_V])

slope, intercept = np.polyfit(B_all, V_all, 1)
print("Overall slope:", slope)

d = 1
I = 30

R_h = (d / I) * slope
print("R_h :", R_h, "m^3/C")

if R_h < 0:
    print("the majority carriers are electrons")
else:
    print("the majority carriers are holes")

q = 1.6e-19
n = 1 / (q * abs(R_h))
print("carrier concentration :", n, "1/m^3")

V_h = df["V_h(mV)"].values
V_x = df["V_x(mV)"].values
I_mA = df["I(mA)"].values

mask = ~np.isnan(V_x) & ~np.isnan(V_h)
V_x_clean = V_x[mask]
V_h_clean = V_h[mask]

plt.figure(figsize=(8, 6))
plt.scatter(V_x_clean, V_h_clean, color="green", label="Part 2 data")
plt.axhline(0, color="black", linewidth=0.8)
plt.axvline(0, color="black", linewidth=0.8)
plt.xlabel("Sample Voltage V_x (mV)")
plt.ylabel("Hall Voltage V_h (mV)")
plt.title("Hall Voltage vs Sample Voltage")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "hall_voltage_vs_sample_voltage.png"), dpi=300)
plt.close()

slope2, intercept2 = np.polyfit(V_x_clean, V_h_clean, 1)

print("Part 2 slope:", slope2)
print("Part 2 intercept:", intercept2)

L = 20
W = 10
B = 250 / 1000

mobility = (L / W) * (1 / B) * slope2
print("mobility: ", mobility, "1/T")

Vh_pred = slope2 * V_x_clean + intercept2

ss_res = np.sum((V_h_clean - Vh_pred) ** 2)
ss_tot = np.sum((V_h_clean - np.mean(V_h_clean)) ** 2)

r2 = 1 - ss_res / ss_tot
print("R^2 =", r2)

residuals = V_h_clean - Vh_pred
sigma_Vh = np.std(residuals)
sigma_Vx = 1.0

print("Estimated sigma_Vh:", sigma_Vh)
print("Estimated sigma_Vx:", sigma_Vx)

N = 5000
q = 1.6e-19

d = 1e-3
I = 30e-3

sigma_B = 1.0
sigma_Vh1 = 0.22
sigma_d = 0.01e-3
sigma_I = 1e-3

slope_samples = []
Rh_samples = []
n_samples = []

for _ in range(N):
    B_sim = B_all + np.random.normal(0, sigma_B, size=len(B_all))
    V_sim = V_all + np.random.normal(0, sigma_Vh1, size=len(V_all))

    d_sim = d + np.random.normal(0, sigma_d)
    I_sim = I + np.random.normal(0, sigma_I)

    if d_sim <= 0 or I_sim <= 0:
        continue

    slope_sim, intercept_sim = np.polyfit(B_sim, V_sim, 1)
    Rh_sim = (d_sim / I_sim) * slope_sim
    n_sim = 1 / (q * abs(Rh_sim))

    slope_samples.append(slope_sim)
    Rh_samples.append(Rh_sim)
    n_samples.append(n_sim)

slope_samples = np.array(slope_samples)
Rh_samples = np.array(Rh_samples)
n_samples = np.array(n_samples)

print("Part 1 Monte Carlo results:")
print("Slope  = {:.6f} ± {:.6f} V/T".format(np.mean(slope_samples), np.std(slope_samples)))
print("R_H    = {:.6e} ± {:.6e} m^3/C".format(np.mean(Rh_samples), np.std(Rh_samples)))
print("n      = {:.6e} ± {:.6e} m^-3".format(np.mean(n_samples), np.std(n_samples)))

Vh_pred = slope2 * V_x_clean + intercept2
residuals = V_h_clean - Vh_pred
sigma_Vh = np.std(residuals)
sigma_Vx = 1.0

print("Estimated sigma_Vh:", sigma_Vh)
print("Estimated sigma_Vx:", sigma_Vx)

sigma_d = 0.01e-3
sigma_w = 0.01e-3
sigma_V = 0.001

N = 5000

slope_samples = []
mu_samples = []

for _ in range(N):
    Vx_sim = V_x_clean + np.random.normal(0, sigma_Vx, size=len(V_x_clean))
    Vh_sim = V_h_clean + np.random.normal(0, sigma_Vh, size=len(V_h_clean))

    d_sim = np.random.normal(L, sigma_d)
    w_sim = np.random.normal(W, sigma_w)
    V_sim = np.random.normal(B, sigma_V)

    if d_sim <= 0 or w_sim <= 0 or V_sim <= 0:
        continue

    slope_sim, intercept_sim = np.polyfit(Vx_sim, Vh_sim, 1)
    mu_sim = (d_sim / w_sim) * (1 / V_sim) * slope_sim

    slope_samples.append(slope_sim)
    mu_samples.append(mu_sim)

slope_samples = np.array(slope_samples)
mu_samples = np.array(mu_samples)

mean_slope = np.mean(slope_samples)
std_slope = np.std(slope_samples)

mean_mu = np.mean(mu_samples)
std_mu = np.std(mu_samples)

print("\nPart 2 Monte Carlo results:")
print("Slope = {:.6f} ± {:.6f}".format(mean_slope, std_slope))
print("Mobility = {:.6e} ± {:.6e} m^2/(V·s)".format(mean_mu, std_mu))

plt.figure(figsize=(8, 5))
plt.hist(mu_samples, bins=40, edgecolor="black")
plt.axvline(mean_mu, linestyle="--", label="Mean")
plt.axvline(mean_mu + std_mu, linestyle=":")
plt.axvline(mean_mu - std_mu, linestyle=":")
plt.xlabel("Mobility μ (m²/(V·s))")
plt.ylabel("Frequency")
plt.title("Monte Carlo Distribution of Hall Mobility")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "mobility_distribution.png"), dpi=300)
plt.close()

plt.figure(figsize=(8, 5))
plt.hist(Rh_samples, bins=40, edgecolor="black")
plt.axvline(np.mean(Rh_samples), linestyle="--", label="Mean")
plt.axvline(np.mean(Rh_samples) + np.std(Rh_samples), linestyle=":")
plt.axvline(np.mean(Rh_samples) - np.std(Rh_samples), linestyle=":")
plt.xlabel("Hall Coefficient R_H (m³/C)")
plt.ylabel("Frequency")
plt.title("Monte Carlo Distribution of Hall Coefficient")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "hall_coefficient_distribution.png"), dpi=300)
plt.close()

plt.figure(figsize=(8, 5))
plt.hist(n_samples, bins=40, edgecolor="black")
plt.axvline(np.mean(n_samples), linestyle="--", label="Mean")
plt.axvline(np.mean(n_samples) + np.std(n_samples), linestyle=":")
plt.axvline(np.mean(n_samples) - np.std(n_samples), linestyle=":")
plt.xlabel("Carrier Concentration n (m⁻³)")
plt.ylabel("Frequency")
plt.title("Monte Carlo Distribution of Carrier Concentration")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "carrier_concentration_distribution.png"), dpi=300)
plt.close()

plt.figure(figsize=(8, 6))
plt.scatter(V_x_clean, V_h_clean, label="Data", alpha=0.6)

for _ in range(50):
    Vx_sim = V_x_clean + np.random.normal(0, sigma_Vx, size=len(V_x_clean))
    Vh_sim = V_h_clean + np.random.normal(0, sigma_Vh, size=len(V_h_clean))
    slope_sim, intercept_sim = np.polyfit(Vx_sim, Vh_sim, 1)
    plt.plot(V_x_clean, slope_sim * V_x_clean + intercept_sim, alpha=0.1)

plt.xlabel("V_x (mV)")
plt.ylabel("V_h (mV)")
plt.title("Monte Carlo Simulated Fits")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "monte_carlo_simulated_fits.png"), dpi=300)
plt.close()