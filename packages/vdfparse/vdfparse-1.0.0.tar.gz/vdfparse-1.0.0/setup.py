from setuptools import setup, find_packages

setup(
    name='vdfparse',
    version='1.0.0',
    description='Valve Data Format (VDF) parser for Python',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='0xFF-SYS',
    author_email='makunzdev@gmail.com',
    url='https://github.com/0xFF-SYS/vdfparse',
    packages=find_packages(),
    py_modules=[],
    python_requires='>=3.6',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
)
