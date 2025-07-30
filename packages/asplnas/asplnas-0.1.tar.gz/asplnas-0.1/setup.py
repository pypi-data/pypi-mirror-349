from setuptools import setup, find_packages
setup(
    name='asplnas', 
    version='0.1',

    packages=find_packages(),
    install_requires=[

    ],
    entry_points={
        'console_scripts': [
            'asplnas = asplnas:hello',
        ]
    },
)