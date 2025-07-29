from setuptools import setup, find_packages

setup(
    name='sparkdv',  
    version='0.1.0',
    description='Data Vault automation for Apache Spark',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yorik501',
    author_email='bugakov.egor@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'pyspark>=3.0.0',
    ],
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
