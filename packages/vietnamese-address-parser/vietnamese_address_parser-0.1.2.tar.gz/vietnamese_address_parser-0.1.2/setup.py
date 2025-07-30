from setuptools import setup, find_packages

setup(
    name='vietnamese_address_parser',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        # Add dependencies here
        
    ],
    entry_points={
        'console_scripts': [
            'vietnamese_address_parser = vietnamese_address_parser:hello', 
        ],
    },
)