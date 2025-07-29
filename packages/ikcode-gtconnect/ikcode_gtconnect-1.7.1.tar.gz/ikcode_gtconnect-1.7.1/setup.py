from setuptools import setup, find_packages

setup(
    name='ikcode-gtconnect',
    version='1.7.1',
    description='IKcode - GUI Terminal Connector',
    author='IKcode',
    author_email='ikcode.offical@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyqt5',
    ],
    entry_points={
        'console_scripts': [
            'ikcode-gtconnect=ikcode_gtconnect.main:runGUI'
        ]
    },
    package_data={
        'ikcode_gtconnect': ['ikcode.png']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    python_requires='>=3.7',
)


