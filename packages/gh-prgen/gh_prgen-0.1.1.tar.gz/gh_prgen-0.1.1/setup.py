from setuptools import setup, find_packages

setup(
    name='gh-prgen',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        # List dependencies here
    ],
    entry_points={
        'console_scripts': [
            'gh-prgen=gh_prgen.cli:main',  # maps CLI command to your main function
        ],
    },
    author='Venigalla Siva Srinivas',
    description='Generate GitHub PR titles and descriptions using Ollama AI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/venigallasivasrinivas/gh-prgen',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)