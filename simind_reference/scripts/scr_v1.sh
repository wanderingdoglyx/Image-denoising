#!/bin/bash

ind_sys=${1}
ind_run=${2}
start_nr=${3}
end_nr=${4}
version=${5}


matlab_dir=${PWD%/*}


for (( ind_nr=$start_nr; ind_nr<=$end_nr; ind_nr++ ))
do
  for (( ind_spsa=1; ind_spsa<=2; ind_spsa++ ))
  do
    echo "matlab -batch \"run('${matlab_dir}/run_MCMC_IO_cluster(${ind_spsa}, ${ind_sys}, ${ind_nr}, ${ind_run}, ${version})')\""
    matlab -batch "run('${matlab_dir}/run_MCMC_IO_cluster(${ind_spsa}, ${ind_sys}, ${ind_nr}, ${ind_run}, ${version})')"
  done
done
