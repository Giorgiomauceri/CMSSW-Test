
void test(void)
{
  TFile *rootfile = new TFile("testaddprofiles.root");

  if (rootfile->IsZombie()) {
    cerr << "file failed to open" << endl;
    return;
  }

  TProfile *tpop1 = (TProfile *)rootfile->Get("Tprofile_operand1");
  TProfile *tpop2 = (TProfile *)rootfile->Get("TProfile_operand2");

  if (!tpop1) {
    cerr << "couldn't find op1 profile histo." << endl;
    return;
  }

  if (!tpop2) {
    cerr << "couldn't find op2 profile histo." << endl;
    return;
  }
 
  TProfile *sumtp = new TProfile(*tpop2);
  sumtp->Reset();
  //sumtp->Draw();

  tpop1->SetTitle("TProfile Operand 1");
  tpop2->SetTitle("TProfile Operand 2");
  sumtp->SetName("op2minusop1");
  sumtp->SetTitle("TProfile_operand2 - TProfile_operand1");
  sumtp->Add(tpop1,tpop2,-1.0,1.0);

  gROOT->SetStyle("Plain");

  TCanvas *c1 = new TCanvas("c1","c1",1200,400);
  c1->Divide(3);

  c1->cd(1); tpop1->Draw();
  c1->cd(2); tpop2->Draw();
  c1->cd(3); sumtp->Draw();

}
