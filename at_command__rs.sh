#!/bin/bash

#PBS -N movie_RS
#PBS -e ../RESULTS_VIS/movie_RS.err
#PBS -o ../RESULTS_VIS/movie_RS.out

#PBS -l nodes=1:ppn=1,walltime=72:00:00
#PBS -q henyey_serial 
#PBS -V

# if in on henyey cd to working directory 
if [ "$MY_HOST" = "henyey" ]
then
    cd $PBS_O_WORKDIR
fi

# start simulations
python _working/rs/make_movie.py