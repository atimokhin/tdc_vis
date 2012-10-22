#include <stdio.h>

#include "fmci.h"


int main(int argc, char *argv[])
{
  const char dirname[] = 
    "../../../RESULTS_VIS/FMCI__SCLF__jp1.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj7_sU/";

  /*
  const char dirname[] = 
    "..\\RESULTS_VIS\\FMCI__SCLF__jp1.5_Pcf1e8_L1_nGJ5e4_nx5e3_dt4e-5__RhoGJConst__R6C_Xb0.7__dP5e-2_inj7_sU\\";
  */


  struct FMCI fmci;
  /* Always do initialization of each newly created FMCI structure! */
  fmci__initialize(&fmci);

  /* read data into FMCI structure */ 
  fmci__read_data_file(412, 'E', dirname, &fmci);

  /* print  fmci (for test purposes) */
  fmci__print(&fmci);

  return 0;
}
