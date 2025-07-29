from setuptools import setup, find_packages

setup(
    name='libbr',
    version='0.1.0',
    author='Renata Machado Barreto Braga',
    description='Uma biblioteca gráfica simples e brasileira, estilo PySimpleGUI.',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
