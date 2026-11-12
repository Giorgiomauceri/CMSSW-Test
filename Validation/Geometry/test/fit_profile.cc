
using namespace std;

Double_t fitf(Double_t *x, Double_t *par)
{
   
   Double_t arg =0.;
    arg = pow(x[0],par[1]);
   Double_t fitval = par[0] * arg;
   return fitval;
}

void fit_profile()
{

    TCanvas *c1 = new TCanvas ("c1","",1600,800);//c1->Divide(2,1);
    TFile *f2 = TFile::Open("h_prof.root","read");
    TH2D *h_prof = (TH2D*) f2->Get("h_prof");    
    
    Double_t x1 = 0.046, x2 = 0.1995;
    Int_t i1 = h_prof->FindFixBin(x1); i1 = std::max(i1, 1);
    Int_t i2 = h_prof->FindFixBin(x2); i2 = std::min(i2, h_prof->GetNbinsX());
    x1 = h_prof->GetBinCenter(i1);
    x2 = h_prof->GetBinCenter(i2);
    Double_t y1 = h_prof->GetBinContent(i1);
    Double_t y2 = h_prof->GetBinContent(i2);
    Double_t p1 = std::log(y1 / y2) / std::log(x1 / x2);
    Double_t p0 = y1 / std::pow(x1, p1);
    // std::cout << "at start: p0 = " << p0 << " , p1 = " << p1 << std::endl;
    TF1 *func = new TF1("func", fitf, x1, x2, 2);
    func->SetParameters(p0, p1);
    h_prof->Fit(func, "R");
    
}
