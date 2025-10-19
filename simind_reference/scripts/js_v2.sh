#!/bin/bash

num_sys=2
num_run=3
start_nr=1
end_nr=1
version=1

for (( ind_sys=1; ind_sys<=${num_sys}; ind_sys++ ))
do
  for (( ind_run=1; ind_run<=${num_run}; ind_run++ ))
  do

    screen -d -m -S mcmc_bl_v2_sys${ind_sys}_run${ind_run}
    sleep 3s
    screen -r mcmc_bl_v2_sys${ind_sys}_run${ind_run} -X exec /home/cced/MCMC_LB_IO_BLSYS_v2/scripts/scr_v1.sh ${ind_sys} ${ind_run} ${start_nr} ${end_nr} ${version}

  done
done
