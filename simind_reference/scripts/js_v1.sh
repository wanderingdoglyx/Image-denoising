#!/bin/bash

num_sys=3
num_run=5
start_nr=1
end_nr=100
version=1

for (( ind_sys=1; ind_sys<=${num_sys}; ind_sys++ ))
do
  for (( ind_run=1; ind_run<=${num_run}; ind_run++ ))
  do

    screen -d -m -S mcmc_bl_v2_sys${ind_sys}_run${ind_run}
    sleep 3s
    screen -r mcmc_bl_v2_sys${ind_sys}_run${ind_run} -X exec ./scripts/scr_v1.sh ${ind_sys} ${ind_run} ${start_nr} ${end_nr} ${version}

  done
done
