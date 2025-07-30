# mzcst-test

conda create -n mzcst-test python=3.10
conda activate mzcst-test
conda install numpy sympy scipy matplotlib h5py # pymoo ipykernel
conda install build twine
pip install --no-index --find-links "C:/Program Files (x86)/CST Studio Suite 2024/Library/Python/repo/simple" cst-studio-suite-link


# 封包

python -m build
python -m twine upload --repository testpypi dist/* --verbose
python -m twine upload dist/* --verbose

# API token
# 测试服
pypi-AgENdGVzdC5weXBpLm9yZwIkOWY4MGZkZDctYjRmZi00ZjFhLTk4YTMtMDQ4MDRmYjUwYTg0AAIqWzMsImI2NzE2ZjVmLTQyODgtNDgzOC04ZjI1LTU0NDFiNGMzNTgzNiJdAAAGIJN2f7_xKktXaPZIw3xI7mk-RgC8qM6gDidCpctVxc-X

# 安装
pip install -i https://test.pypi.org/simple/ mzcst-2024
pip install -i https://test.pypi.org/simple/ --upgrade mzcst-2024


# 正式服
pypi-AgEIcHlwaS5vcmcCJDc2NGFiY2YzLTBhYWMtNDc0NS1hNWYyLWE0Y2M3MTY3NzgyMgACElsxLFsibXpjc3QtMjAyNCJdXQACLFsyLFsiMzVkMmM1MWUtYTAwZS00MWNkLThhYzEtZjMxYzQ1Y2M1NjI5Il1dAAAGINNydcdmgmsInFdjM5aO3t36YEIK1oPiV262S3rAUQPq

pip install mzcst-2024
pip install --upgrade mzcst-2024



#恢复环境
conda env create --file=mzcst-test-raw.yml