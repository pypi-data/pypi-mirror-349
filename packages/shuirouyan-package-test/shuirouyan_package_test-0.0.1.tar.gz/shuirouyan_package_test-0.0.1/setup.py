from setuptools import setup, find_packages

name='shuirouyan_package_test'
'vQ%2QcgV2vy.Vqe'
requires_list = open(f'project/requirements.txt', 'r', encoding='utf8').readlines()
requires_list = [i.strip() for i in requires_list]

setup(
    name = name, 
    version = '0.0.1', 
    author='shuirouyan',
    author_email='ck163114@163.com',
    description='pythonpypi',
    python_requires='>=3.6',
    package_data={"": ["*"]}, 
    license='MIT',
    packages = find_packages(), 
    install_requires = requires_list, 
    include_package_data=True,
    entry_points = { 
        'console_scripts': ['pythonpypi = pythonpypi.__main__:main'] 
    } 
)
