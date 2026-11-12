#!/usr/bin/env python3

import ROOT
import numpy as np

# --------------------------------------------------
# Open ROOT file
# --------------------------------------------------
f = ROOT.TFile.Open("Figures/Tracker_SubDetectors_x_vs_eta.root")

if not f or f.IsZombie():
    raise RuntimeError("Cannot open a.root")

# --------------------------------------------------
# Find first TCanvas in file
# --------------------------------------------------
canvas = None

for key in f.GetListOfKeys():
    obj = key.ReadObj()
    if obj.InheritsFrom("TCanvas"):
        canvas = obj
        break

if canvas is None:
    raise RuntimeError("No TCanvas found in file")

# --------------------------------------------------
# Find THStack inside canvas
# --------------------------------------------------
stack = None

for obj in canvas.GetListOfPrimitives():
    if obj.InheritsFrom("THStack"):
        stack = obj
        break

if stack is None:
    raise RuntimeError("No THStack found in canvas")

# --------------------------------------------------
# Retrieve histograms from stack
# --------------------------------------------------
hist_list = stack.GetHists()

if not hist_list:
    raise RuntimeError("THStack contains no histograms")

histograms = []
for h in hist_list:
    histograms.append(h)

n_hists = len(histograms)

print(f"Found {n_hists} histograms in THStack")

# --------------------------------------------------
# Use first histogram to define binning
# --------------------------------------------------
ref_hist = histograms[0]

n_bins = ref_hist.GetNbinsX()

# Array structure:
# [bin_number, bin_center, hist1, hist2, ...]
data = np.zeros((n_bins, 2 + n_hists))

# --------------------------------------------------
# Fill array
# --------------------------------------------------
for ibin in range(1, n_bins + 1):

    data[ibin - 1, 0] = ibin
    data[ibin - 1, 1] = ref_hist.GetBinCenter(ibin)

    for ih, hist in enumerate(histograms):
        data[ibin - 1, 2 + ih] = hist.GetBinContent(ibin)

# --------------------------------------------------
# Save to text file
# --------------------------------------------------
header = ["bin", "bin_center"]

for hist in histograms:
    header.append(hist.GetName())

header_str = " ".join(header)

np.savetxt(
    "stack_contents.txt",
    data,
    fmt="%.8g",
    header=header_str,
    comments=""
)

print("\nSaved results to stack_contents.txt")

# --------------------------------------------------
# Print maximum bin height for each histogram
# --------------------------------------------------
print("\nMaximum bin height per histogram:")

for hist in histograms:

    max_height = max(
        hist.GetBinContent(i)
        for i in range(1, hist.GetNbinsX() + 1)
    )

    print(f"{hist.GetName():30s} : {max_height}")