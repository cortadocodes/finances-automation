from setuptools import setup, find_packages

setup(
    name='finances-automation',
    version='0.0.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'psycopg2',
        'pytest',
        'sphinx',
        'sphinx_rtd_theme'
    ],
    url='www.github.com/cortadocodes/finances-automation',
    license='',
    author='Marcus Lugg',
    author_email='marcuslugg@googlemail.com',
    description=''
)
