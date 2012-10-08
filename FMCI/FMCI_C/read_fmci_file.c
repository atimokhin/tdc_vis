#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#include "read_fmci_file.h"

/* auxiliary function for reading data group in the .dat file */
int _read_group_start(FILE * pFile, const char *group_name);


struct FMCI read_fmci_data_file(int i_ts, char particle_name, const char* dir_name)
{
  struct FMCI fmci; /* structure to be returned */

  char *particle_directory_name;
  char filename[255] = {0};
  char aux_str[80];

  FILE *pFile;                  /* file pointer */
  int   i, j;                   /* index variables in loops */


  fmci.particle_name = particle_name;  
  switch (particle_name )
    {
    case 'E':
      particle_directory_name = "Electrons";
      break;
    case 'P':
      particle_directory_name = "Positrons";
      break;
    case 'G':
      particle_directory_name = "Pairs";
      break;
    default:
      printf("Wrong particle name!\n");
      exit(EXIT_FAILURE);
    } 

  /* construct full file name: maximum length 255 characters */
  /* if TARGET_PALTFORM_WINDOWS is defined make windows style file names */
#ifndef TARGET_PLATFORM_WINDOWS
  sprintf(filename, "%s/%s/xp_%04d.dat", dir_name, particle_directory_name, i_ts);  
#else  
  sprintf(filename, "%s\\%s\\xp_%04d.dat", dir_name, particle_directory_name, i_ts);  
#endif 

  /* open data file ----------------------------------- */
  pFile = fopen (filename,"r");
  if (pFile==NULL)
  {
    printf("Can not open file %s!\n", filename);
    exit(EXIT_FAILURE);
  }
  /* -------------------------------------------------- */

  /* read dimensions ---------------------------------- */
  _read_group_start(pFile,"params_data:");
  fscanf(pFile,"nx=%d\n", &fmci.nx);
  fscanf(pFile,"np=%d\n", &fmci.np);
  /* -------------------------------------------------- */

  /* allocate memory and read arrays ------------------ */
  /* read x */
  _read_group_start(pFile,"x:");
  fmci.x = (double*) calloc (fmci.nx, sizeof(double));
  for (i = 0; i < fmci.nx; i++)
    fscanf(pFile,"%lE\n", &fmci.x[i]);

  /* read p */
  _read_group_start(pFile,"p:");
  fmci.p = (double*) calloc (fmci.np, sizeof(double));
  for (i = 0; i < fmci.np; i++)
    fscanf(pFile,"%lE\n", &fmci.p[i]);

  /* read xp */
  _read_group_start(pFile,"XP:");
  fgets(aux_str,80,pFile);
  fmci.xp = (double**) calloc ( fmci.nx, sizeof(double*) );
  for (i = 0; i < fmci.nx; i++)
    fmci.xp[i] = (double*) calloc ( fmci.np, sizeof(double) );
  for (i = 0; i < fmci.nx; i++)
    for (j = 0; j < fmci.np; j++)
      fscanf(pFile,"%lE", &fmci.xp[i][j]);
  fscanf(pFile,"\n");
  /* -------------------------------------------------- */

  /* read physical parameters ------------------------- */
  _read_group_start(pFile,"params_physics:");
  fscanf(pFile,"particle=%c\n",  &fmci.particle_name);
  fscanf(pFile,"time=%lG\n", &fmci.time);
  /* -------------------------------------------------- */

  fclose (pFile);
  
  return fmci;
}


int _read_group_start(FILE * pFile, const char *group_name)
{
  char *group_name_read = (char*) malloc (strlen(group_name)*sizeof(char));
  if ( fscanf(pFile,"#>>%s\n",group_name_read) == EOF || strcmp (group_name_read, group_name) !=0  )
    {
      printf("Did not find group \"%s\" => read \"%s\"!\n", group_name, group_name_read);
      exit(EXIT_FAILURE);
    }

#ifndef _DEBUG /* VS 6.0 doesn't like it in debug mode */
  free(group_name_read);
#endif

  return 0;
};


void print_fmci(struct FMCI fmci)
{
  int i, j;

  printf("#>>params_data:\nnx=%d\nnp=%d\n", fmci.nx, fmci.np);

  printf("\n#>>x:\n");
  for ( i = 0; i < fmci.nx; i++)
    {
      printf("%.8lE\n", fmci.x[i]);
    }

  printf("\n#>>p:\n");
  for ( i = 0; i < fmci.np; i++)
    {
      printf("%.8lE\n", fmci.p[i]);
    }

  printf("\n#>>XP: (rows:%4d, columns:%4d)\n", fmci.nx, fmci.np);
  for ( i = 0; i < fmci.nx; i++)
    {
      printf("%.8lE", fmci.xp[i][0]);
      for ( j = 1; j < fmci.np; j++)
        {
          printf(" %.8lE", fmci.xp[i][j]);
        }
      printf("\n");
    }

  printf("\n#>>params_physics:\n");
  printf("particle=%c\n", fmci.particle_name);
  printf("time=%.8E\n",   fmci.time);
}
