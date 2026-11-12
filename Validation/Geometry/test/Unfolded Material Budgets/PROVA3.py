import numpy as np
import matplotlib.pyplot as plt

with open('Unfolded Material Budgets/MB_Tracker_Unfolded.txt', 'r') as file:
    a = [float(line) for line in file]
npa = np.asarray(a)
npa2 = npa.reshape(290, 1200)
fig, ax = plt.subplots()
#mh.cms.label("Private work (CMS simulation), 2022+2023", data=False, com=13.6)
#mh.add_text("2022+2023", loc="over right", ax=ax)
fig.set_size_inches(40, 30, forward=True)
im = ax.imshow(npa2, origin="lower", cmap="jet", aspect='auto')
cbar = ax.figure.colorbar(im, orientation="horizontal", ax=ax)
#cbar.ax.set_ylabel("Correlation", rotation=-90, va="bottom")
plt.tight_layout()
plt.savefig("TEST.pdf", dpi=300)

