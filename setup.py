from setuptools import setup, find_packages


__VERSION__ = '1.0.0'


setup(
    author='Marcus Lugg',
    author_email='marcuslugg@googlemail.com',
    description='Automate your finances analysis.',
    entry_points={
        'console_scripts': [
            'finances-automation = finances_automation.command.command:start'
        ]
    },
    extras_require={
        'development': [
            'flake8',
            'pytest',
            'pytest-cov',
            'sphinx==1.4.8',
            'sphinx_rtd_theme==0.4.2'
        ]
    },
    install_requires=[
        'matplotlib==3.0.2',
        'numpy==1.15.2',
        'pandas==0.23.4',
        'psycopg2-binary==2.7.5',
    ],
    license='',
    name='finances-automation',
    packages=find_packages(),
    url='www.github.com/cortadocodes/finances-automation',
    version=__VERSION__
)
