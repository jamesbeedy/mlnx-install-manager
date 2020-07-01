from setuptools import find_packages, setup


setup(
    name='mlnx-install-manager',
    packages=find_packages(include=['mlnx_install_manager']),
    version='0.0.1',
    license='MIT',
    long_description=open('README.md', 'r').read(),
    url='https://github.com/omnivector-solutions/mlnx-install-manager',
    install_requires=[],
    python_requires='>=3.6',
)
