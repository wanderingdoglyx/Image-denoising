#!/bin/bash

screen -d -m -S mcmc_bl_v2_sys_eval
sleep 3s
screen -r mcmc_bl_v2_sys_eval -X exec /home/cced/MCMC_LB_IO_BLSYS_v2/scripts/scr_eval.sh
