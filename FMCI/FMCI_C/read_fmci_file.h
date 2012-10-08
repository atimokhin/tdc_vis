/* #define TARGET_PLATFORM_WINDOWS */

#ifndef _READ_FMCI_FILE_H_
#define _READ_FMCI_FILE_H_

struct FMCI{

  /* dimentions of the arrays */
  int nx;
  int np;

  /* coordinates and momenta */
  double *x;
  double *p;
  /* array with statistical weights of metaparticles: nx rows, np columns */
  double **xp;

  char particle_name;           /* 'E' - Electrons; 'P' - Positrons; 'G' - gamma rays */
  
  double time;

  double B0;                    /* magnetic field [in 10^12 Gauss] */
  double X0;                    /* distance noramalization   */
};


struct FMCI read_fmci_data_file(int i, char particle_name, const char* dir_name);

void print_fmci(struct FMCI fmci);


#endif /* _READ_FMCI_FILE_H_ */
