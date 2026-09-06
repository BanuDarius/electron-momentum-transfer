import happi
import numpy as np
import matplotlib.pyplot as plt

c_au = 137.036
lambda_norm = 2.0 * np.pi

sim = happi.Open(".")
track = sim.TrackParticles("electron", axes=["x", "px", "py", "pz"])
data = track.getData()

x_init = data["x"][0, :]
px_final = data["px"][-1, :]
py_final = data["py"][-1, :]
pz_final = data["pz"][-1, :]

x_centered_lambda = (x_init - 2.0 * lambda_norm) / lambda_norm
px_smilei_au = px_final * c_au

sort_idx = np.argsort(x_centered_lambda)
x_smilei = x_centered_lambda[sort_idx]
px_smilei = px_smilei_au[sort_idx]

emt_raw = np.fromfile("out-final-p-electromag.bin", dtype=np.float64)
emt_momenta = emt_raw.reshape(-1, 3)
px_emt = emt_momenta[:, 0]

x_emt = np.linspace(-0.5, 0.5, len(px_emt))

max_px_emt = np.max(np.abs(px_emt))
px_smilei_interp = np.interp(x_emt, x_smilei, px_smilei)
relative_error = 100.0 * np.abs(px_smilei_interp - px_emt) / max_px_emt

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7), sharex=True)

ax1.plot(x_emt, px_emt, 'k-', linewidth=1.5, label='EMT')
ax1.plot(x_smilei, px_smilei, 'r--', linewidth=1.5, label='SMILEI')
ax1.set_ylabel(r'Final momentum $p_x$ [a.u.]', fontsize=11)
ax1.legend(loc='upper right', frameon=True)

ax2.plot(x_emt, relative_error, 'b-', linewidth=1.2)
ax2.set_xlabel(r'Initial position $x/\lambda$', fontsize=11)
ax2.set_ylabel(r'Relative error $\epsilon$ [%]', fontsize=11)
ax2.set_yscale('log')
ax2.set_xlim([-0.5, 0.5])

plt.tight_layout()
plt.savefig("emt_vs_smilei.png", dpi=300)
plt.close(fig)

print(f"Average errors: {np.mean(relative_error):0.2f}%")