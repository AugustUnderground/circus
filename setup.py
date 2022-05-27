from setuptools import setup, find_packages

package_name = 'circus'

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as req:
    requirements = req.read().splitlines()

scripts: [str] = [ f'carnival = {package_name}.__main__:carnival']

setup( name                          = package_name
     , version                       = '0.0.1'
     , author                        = 'Yannick Uhlmann'
     , author_email                  = 'augustunderground@getgoogleoff.me'
     , description                   = 'Analog Circuit Sizing Gym Environment'
     , long_description              = long_description
     , long_description_content_type = 'text/markdown'
     , url                           = 'https://github.com/augustunderground/circus'
     , packages                      = find_packages()
     , classifiers                   = [ 'Development Status :: 2 :: Pre-Alpha'
                                       , 'Programming Language :: Python :: 3'
                                       , 'Operating System :: POSIX :: Linux' ]
     , python_requires               = '>=3.9'
     , install_requires              = requirements
     , entry_points                  = { 'console_scripts': scripts }
     , package_data                  = { '': ['__pycache__/*']}
     , )
