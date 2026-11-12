#!/usr/bin/env python3

import ROOT
import numpy as np

# --------------------------------------------------
# Load txt file
# --------------------------------------------------
filename = "stack_contents.txt"

data = np.loadtxt(filename, skiprows=1)

bin_number = data[:, 0]
bin_center = data[:, 1]

h1_vals = data[:, 2]
h2_vals = data[:, 3]
h3_vals = data[:, 4]

# --------------------------------------------------
# Sum first three histograms
# --------------------------------------------------
yvals = h1_vals + h2_vals + h3_vals

# --------------------------------------------------
# Determine binning
# --------------------------------------------------
nbins = len(bin_center)

if nbins < 2:
    raise RuntimeError("Need at least 2 bins")

bin_width = bin_center[1] - bin_center[0]

xmin = bin_center[0] - bin_width / 2.
xmax = bin_center[-1] + bin_width / 2.

# --------------------------------------------------
# Rebuild histograms
# --------------------------------------------------
h1 = ROOT.TH1D("h1", "", nbins, xmin, xmax)
h2 = ROOT.TH1D("h2", "", nbins, xmin, xmax)
h3 = ROOT.TH1D("h3", "", nbins, xmin, xmax)

for i in range(nbins):
    h1.SetBinContent(i + 1, h1_vals[i])
    h2.SetBinContent(i + 1, h2_vals[i])
    h3.SetBinContent(i + 1, h3_vals[i])

h1.SetFillColor(ROOT.kGray + 2)
h2.SetFillColor(ROOT.kAzure - 2)
h3.SetFillColor(ROOT.kYellow - 7)

# --------------------------------------------------
# Create THStack
# --------------------------------------------------
stack = ROOT.THStack("stack", "Stack + Fit")

stack.Add(h1)
stack.Add(h2)
stack.Add(h3)

print(bin_center, yvals)
# --------------------------------------------------
# Build graph from summed entries
# --------------------------------------------------
graph = ROOT.TGraph()

for i in range(nbins):
    graph.SetPoint(i, float(bin_center[i]), float(yvals[i]))

graph.SetMarkerStyle(20)
graph.SetMarkerSize(1.0)

# --------------------------------------------------
# Fit function
# Replace "pol1" by your own function later
# --------------------------------------------------
fitfunc = ROOT.TF1("fitfunc", "[0]*0.06/(sin(2*atan(exp(-x))))", xmin, xmax)

fit_result = graph.Fit(fitfunc, "S", xmin=-3, xmax=3)

# --------------------------------------------------
# Print fit information
# --------------------------------------------------
print("\n===================================")
print("Fit results")
print("===================================")

npar = fitfunc.GetNpar()

for ipar in range(npar):
    print(
        f"Parameter {ipar}: "
        f"{fitfunc.GetParameter(ipar):.6g} "
        f"+/- {fitfunc.GetParError(ipar):.6g}"
    )

print(f"\nChi2      = {fitfunc.GetChisquare():.6g}")
print(f"NDF       = {fitfunc.GetNDF()}")
print(f"Chi2/NDF  = {fitfunc.GetChisquare()/fitfunc.GetNDF():.6g}")

print("===================================\n")

# --------------------------------------------------
# Draw everything
# --------------------------------------------------
canvas = ROOT.TCanvas("c", "Fit", 1000, 800)

stack.Draw("HIST")

stack.GetXaxis().SetTitle("Eta")
stack.GetYaxis().SetTitle("MB(x/X0)")

# Draw graph points (optional)
graph.Draw("P SAME")

# Draw fitted curve
fitfunc.SetLineColor(ROOT.kRed)
fitfunc.SetLineWidth(3)
fitfunc.Draw("SAME")

# Legend
leg = ROOT.TLegend(0.42, 0.70, 0.65, 0.88)
leg.AddEntry(h1, "BeamPipe", "f")
leg.AddEntry(h2, "PhaseII Pixel Barrel", "f")
leg.AddEntry(h3, "PhaseII Pixel Endcap", "f")
leg.AddEntry(fitfunc, "Fit", "l")
leg.Draw()

canvas.Update()

# --------------------------------------------------
# Save plot
# --------------------------------------------------
canvas.SaveAs("stack_fit.png")
canvas.SaveAs("stack_fit.pdf")

print("Saved:")
print("  stack_fit.png")
print("  stack_fit.pdf")
