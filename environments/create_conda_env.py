conda create -n yourenvname python=x.x anaconda
#4. Activate your virtual environment.
source activate yourenvname
#5. Install additional Python packages to a virtual environment.
conda install -n yourenvname [package]
#6. Deactivate your virtual environment.
source deactivate
#Delete a no longer needed virtual environment
conda remove -n yourenvname -all