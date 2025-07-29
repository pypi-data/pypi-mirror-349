from setuptools import setup, find_packages

setup(
    name='jaalvarez2818_ratehawk_sdk',
    version='0.1.24',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    url='https://github.com/jaalvarez2818/ratehawk-sdk',
    author='José Angel Alvarez Abraira',
    author_email='jaalvarez2818development@gmail.com',
    description='SDK para la comunicación con el API de RateHawk para las reservas de hoteles.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
