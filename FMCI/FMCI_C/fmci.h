/* #define TARGET_PLATFORM_WINDOWS */

#ifndef _FMCI_H_
#define _FMCI_H_


/*
  Structure holding FMCI data
*/
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
  
  double time;                  /* time of the timeshot */

  double P;                     /* pulsar period [sec] */
  double B12;                   /* magnetic field [in 10^12 Gauss] */
  double Lcm;                   /* domain length [cm]  */

  double Theta;                 /* Colatitude of the field line \theta/\theta_{pc} */
  double Chi;                   /* Pulsar inclination angle */

  int __need_memory_allocation; /* internal variable, do not chnage it! */
};


/*
  Initialize struct FMCI

  Always do initialization before using struct FMCI!
*/
void fmci__initialize(struct FMCI* p_fmci);


/*
  Reads data file 'xp_{>i<}.dat' 
  for particle >particle_name< [either 'E' - Electrons, 'P' - Positrons, 'G' -gamma-rays ]
  from directory >dir_name</[Electrons|Positrons|Pairs]/
  and populates FMCI structure given by pointer >*p_fmci< with read data

  i.e. file to be read is:
  >dir_name</[Electrons|Positrons|Pairs]/xp_{>i<}.dat
  
  if provided structure *p_fmci cannot hold reda data, structure's
  arrays will be deleted and the space will be allocated anew
*/
void fmci__read_data_file(int i, char particle_name, const char* dir_name, struct FMCI* p_fmci);


/* 
   Prints structure data into standard output 
*/
void fmci__print(struct FMCI* p_fmci);


#endif /* _FMCI_H_ */
