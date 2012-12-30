#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#include "fmci.h"

/* auxiliary function for reading data group in the .dat file */
int _fmci__read_group_start(FILE * pFile, const char *group_name);


void fmci__read_data_file(int i_ts, char particle_name, const char* dir_name, struct FMCI* p_fmci)
{
  char *particle_directory_name;
  char filename[255] = {0};
  char  aux_str[80];
  int   aux_n;

  FILE *pFile;                  /* file pointer */
  int   i, j;                   /* index variables in loops */


  p_fmci->particle_name = particle_name;  
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
  _fmci__read_group_start(pFile,"params_data:");
  fscanf(pFile,"nx=%d\n", &aux_n);
  if (aux_n != p_fmci->nx)
    {
      p_fmci->nx = aux_n;
      p_fmci->__need_memory_allocation = 1;
    } 
  fscanf(pFile,"np=%d\n", &aux_n);
  if (aux_n != p_fmci->np)
    {
      p_fmci->np = aux_n;
      p_fmci->__need_memory_allocation = 1;
    } 
  /* -------------------------------------------------- */

  /* read x ------------------------------------------- */
  _fmci__read_group_start(pFile,"x:");
  if (p_fmci->__need_memory_allocation == 1)
    {
      free(p_fmci->x);
      p_fmci->x = (double*) calloc (p_fmci->nx, sizeof(double));      
    }
  for (i = 0; i < p_fmci->nx; i++)
    fscanf(pFile,"%lE\n", &p_fmci->x[i]);
  /* -------------------------------------------------- */

  /* read p ------------------------------------------- */
  _fmci__read_group_start(pFile,"p:");
  if (p_fmci->__need_memory_allocation == 1)
    {
      free(p_fmci->p);
      p_fmci->p = (double*) calloc (p_fmci->np, sizeof(double));      
    }
  for (i = 0; i < p_fmci->np; i++)
    fscanf(pFile,"%lE\n", &p_fmci->p[i]);
  /* -------------------------------------------------- */

  /* read xp ------------------------------------------ */
  _fmci__read_group_start(pFile,"XP:");
  fgets(aux_str,80,pFile);
  /* allocate/deallocate memory for p_fmci->xp */
  if (p_fmci->__need_memory_allocation == 1)
    {
      /* free memory if necessary */
      if (p_fmci->xp != NULL)
        {
          for (i = 0; i < p_fmci->nx; i++)
            free(p_fmci->xp[i]);
          free(p_fmci->xp);
        }
      /* allocate memory */
      p_fmci->xp = (double**) calloc ( p_fmci->nx, sizeof(double*) );
      for (i = 0; i < p_fmci->nx; i++)
        p_fmci->xp[i] = (double*) calloc ( p_fmci->np, sizeof(double) );
    }
  /* read data into p_fmci->xp */
  for (i = 0; i < p_fmci->nx; i++)
    for (j = 0; j < p_fmci->np; j++)
      fscanf(pFile,"%lE", &p_fmci->xp[i][j]);
  fscanf(pFile,"\n");
  /* -------------------------------------------------- */

  /* set memory request flag to zero */
  p_fmci->__need_memory_allocation = 0;

  /* read physical parameters ------------------------- */
  _fmci__read_group_start(pFile,"params_physics:");
  fscanf(pFile,"particle=%c\n", &p_fmci->particle_name);

  fscanf(pFile,"time=%lG\n", &p_fmci->time);

  fscanf(pFile,"P=%lG\n",   &p_fmci->P);
  fscanf(pFile,"B12=%lG\n", &p_fmci->B12);
  fscanf(pFile,"Lcm=%lG\n", &p_fmci->Lcm);

  fscanf(pFile,"Theta=%lG\n", &p_fmci->Theta);
  fscanf(pFile,"Chi=%lG\n",   &p_fmci->Chi);
  /* -------------------------------------------------- */

  fclose (pFile);
}


int _fmci__read_group_start(FILE * pFile, const char *group_name)
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


void fmci__initialize(struct FMCI* p_fmci)
{
  /* request memory allocation for arrays */
  p_fmci->__need_memory_allocation=1;

  /* sell all array pointers to NULL */
  p_fmci->x  = NULL;
  p_fmci->p  = NULL;
  p_fmci->xp = NULL;
};


void fmci__print(struct FMCI* p_fmci)
{
  int i, j;

  printf("#>>params_data:\nnx=%d\nnp=%d\n", p_fmci->nx, p_fmci->np);

  printf("\n#>>x:\n");
  for ( i = 0; i < p_fmci->nx; i++)
    {
      printf("%.8lE\n", p_fmci->x[i]);
    }

  printf("\n#>>p:\n");
  for ( i = 0; i < p_fmci->np; i++)
    {
      printf("%.8lE\n", p_fmci->p[i]);
    }

  printf("\n#>>XP: (rows:%4d, columns:%4d)\n", p_fmci->nx, p_fmci->np);
  for ( i = 0; i < p_fmci->nx; i++)
    {
      printf("%.8lE", p_fmci->xp[i][0]);
      for ( j = 1; j < p_fmci->np; j++)
        {
          printf(" %.8lE", p_fmci->xp[i][j]);
        }
      printf("\n");
    }

  printf("\n#>>params_physics:\n");
  printf("particle=%c\n", p_fmci->particle_name);
  printf("time=%.8E\n",   p_fmci->time);

  printf("P=%.8lE\n",   p_fmci->P);
  printf("B12=%.8lE\n", p_fmci->B12);
  printf("Lcm=%.8lE\n", p_fmci->Lcm);

  printf("Theta=%.8lE\n", p_fmci->Theta);
  printf("Chi=%.8lE\n",   p_fmci->Chi);
}
