#include <stdio.h>

#include "read_fmci_file.h"


int main(int argc, char *argv[])
{
  const char dirname[] = 
    "../../../RESULTS_VIS/FMCI__SCLF__jp1.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj7_sU/";

  /*
  const char dirname[] = 
    "..\\RESULTS_VIS\\FMCI__SCLF__jp1.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj7_sU\\";
  */


  struct FMCI fmci = read_fmci_data_file(412, 'E', dirname);

  /* print  fmci (for test purposes) */
  print_fmci(fmci);

  return 0;
}
