import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

with open('Unfolded Material Budgets/MB_BeamPipe_Unfolded_1.txt', 'r') as file:
    a = [float(line) for line in file]
print('a')
npa = np.asarray(a)
npa2 = npa.reshape(290, 1200)
j=5
#npa2 = npa2.reshape(-1,j).mean(axis=1).reshape(npa2.shape[0],-1)
#npa2 = npa2.reshape(j,-1).mean(axis=0).reshape(npa2.shape[1],-1)
fig, ax = plt.subplots()
print('a')
#mh.cms.label("Private work (CMS simulation), 2022+2023", data=False, com=13.6)
#mh.add_text("2022+2023", loc="over right", ax=ax)
fig.set_size_inches(20, 10, forward=True)
#im = ax.imshow(npa2, origin="lower", cmap="jet", extent=[-2935, 2935, 25, 1235], norm=colors.LogNorm(vmin=1e-3), aspect='auto')
im = ax.imshow(npa2, origin="lower", cmap="jet", norm=colors.LogNorm(vmin=1e-3), aspect='auto')
ax.set_xlabel("z (mm)")
ax.set_ylabel("r (mm)")
cbar = ax.figure.colorbar(im, orientation="vertical", norm=colors.LogNorm(vmin=1e-3), ax=ax)
cbar.ax.set_ylabel("x/X0", rotation=-90, va="bottom")
print('a')
plt.tight_layout()
plt.savefig("TEST.png", dpi=3000)
print('b')
