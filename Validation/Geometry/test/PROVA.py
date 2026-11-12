import ROOT
import numpy as np
from decimal import *

def unfold_th2f(hist2d):
    """
    Unfold a ROOT TH2F histogram into a 1D array, row by row.
    Excludes overflow/underflow bins.
    
    Parameters:
        hist2d: ROOT.TH2F object
    
    Returns:
        numpy array of shape (N*M,) with bin contents
    """
    nx = hist2d.GetNbinsX()  # number of columns
    ny = hist2d.GetNbinsY()  # number of rows
    print(nx, ny)
    values = np.zeros(nx * ny)
    edges_x = np.zeros((nx * ny, 2))
    edges_y = np.zeros((nx * ny, 2))
    
    #edges_x = np.array([hist2d.GetXaxis().GetBinLowEdge(ix) for ix in range(1, nx + 2)])
    #edges_y = np.array([hist2d.GetYaxis().GetBinLowEdge(iy) for iy in range(1, ny + 2)])


    for iy in range(1, ny + 1):       # ROOT bins are 1-indexed
        for ix in range(1, nx + 1):
            flat_idx = (iy - 1) * nx + (ix - 1)
            values[flat_idx] = hist2d.GetBinContent(ix, iy)
            edges_x[flat_idx, 0] = hist2d.GetXaxis().GetBinLowEdge(ix)
            edges_x[flat_idx, 1] = hist2d.GetXaxis().GetBinLowEdge(ix+1)
            edges_y[flat_idx, 0] = hist2d.GetYaxis().GetBinLowEdge(iy)
            edges_y[flat_idx, 1] = hist2d.GetYaxis().GetBinLowEdge(iy+1)
    return values, edges_x, edges_y, nx, ny


f = ROOT.TFile("matbdg_Tracker_ExtendedRun4D121.root", "READ")
h = f.Get("1060")   # retrieve your TH2F
getcontext().prec=7

arr, edges_x, edges_y, Nx, Ny = unfold_th2f(h)
with open('Unfolded Material Budgets/MB_Tracker_Unfolded.txt', 'w') as f:
    #print("Bin_Content", "\t", "Bin_Number", "\t", "Bin_x_edges", "\t", "Bin_y_edges", file=f)
    for iy in range(1, Ny + 1):       # ROOT bins are 1-indexed
        for ix in range(1, Nx + 1):
            i = (iy - 1) * Nx + (ix - 1)
            ID= [ix, iy]
            print(arr[i],  ID, edges_x[i], edges_y[i], file=f)
#        print("\n", file=f)
with open('Unfolded Material Budgets/MB_Tracker_Unfolded_1.txt', 'w') as f:
    #print("Bin_Content", "\t", "Bin_Number", "\t", "Bin_x_edges", "\t", "Bin_y_edges", file=f)
    for iy in range(1, Ny + 1):       # ROOT bins are 1-indexed
        for ix in range(1, Nx + 1):
            i = (iy - 1) * Nx + (ix - 1)
            ID= [ix, iy]
            print(arr[i], file=f)
            #print(arr[i],  ID, edges_x[i], edges_y[i], file=f)
#        print("\n", file=f)
with open('Unfolded Material Budgets/MB_Tracker_Unfolded_2.txt', 'w') as f:
    #print("Bin_Content", "\t", "Bin_Number", "\t", "Bin_x_edges", "\t", "Bin_y_edges", file=f)
    for ix in range(1, Nx + 1):       # ROOT bins are 1-indexed
        for iy in range(1, Ny + 1):
            i = (iy - 1) * Nx + (ix - 1)
            print(edges_x[i][0]/10., edges_y[i][0]/10., arr[i], file=f)
#        print("\n", file=f)


print(f"Shape: {arr.shape}")        # (N*M,)
#print(arr)
print(max(arr))
#print(edges_x, edges_y)
