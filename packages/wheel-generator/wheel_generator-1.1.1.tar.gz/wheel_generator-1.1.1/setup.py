from setuptools import setup, find_packages

setup(
    name='wheel_generator',
    version='1.1.1',
    packages=find_packages(),  # it will find 'wheel_generator' folder as package
    description='Blender addon to generate wheels and gears',
    author='Adhithiyan',
    author_email='adhithiyan12899@gmail.com',
    url='https://github.com/A-D-H-I/wheel_generator',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
