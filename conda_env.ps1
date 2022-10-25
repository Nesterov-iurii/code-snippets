conda create --name myenv
conda activate myenv
# install packages
pip install jupyter
python -m ipykernel install --user --name myenv --display-name "My environment"