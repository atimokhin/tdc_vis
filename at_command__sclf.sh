#!/bin/bash

#PBS -N make_movie_jm0.5
#PBS -e ../RESULTS_VIS/make_movie_jm0.5.err
#PBS -o ../RESULTS_VIS/make_movie_jm0.5.out

#PBS -l nodes=1:ppn=1,walltime=72:00:00
#PBS -q henyey_serial 
#PBS -V

# if in on henyey cd to working directory 
if [ "$MY_HOST" = "henyey" ]
then
    cd $PBS_O_WORKDIR
fi

# start simulations
python _working/sclf/make_movie.py