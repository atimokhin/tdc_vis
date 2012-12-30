#include <stdio.h>

#include "fmci.h"


int main(int argc, char *argv[])
{
  const char dirname[] = 
    "../../../RESULTS_VIS/__RS_2/FMCI__RS__RD_jp0.5_P0.09_L0.6_nGJ5e4_nx5e3_dt4e-5_sU/";

  /*
  const char dirname[] = 
    "..\\RESULTS_VIS\\__RS_2\\FMCI__RS__RD_jp0.5_P0.09_L0.6_nGJ5e4_nx5e3_dt4e-5_sU\\";
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
