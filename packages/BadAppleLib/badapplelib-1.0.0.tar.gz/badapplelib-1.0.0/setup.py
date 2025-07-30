from setuptools import setup, find_packages

setup(
    name='BadAppleLib',
    version='1.0.0', # Version
    description='A library specifically made to just play bad apple!',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Ricca665/BadAppleLib',
    author='Ricca665',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    python_requires='>=3.12',
    install_requires=[],
    include_package_data=True,
    package_data={
        'BadApple': ['frames/*'],
    }
)