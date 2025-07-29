from setuptools import setup, find_packages

setup(
    name="vaspflow",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.15.0",
        "matplotlib>=2.0.0",
    ],
    entry_points={
        'console_scripts': [
            'vaspflow=vaspflow.core:main',
        ],
    },
    author="Dinghui Wang",
    author_email="wangdh@cumt.edu.cn",
    description="VASP Workflow Automation and Band Structure Analysis Tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ooteki-teo/vaspflow",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Chemistry",
    ],
    python_requires=">=3.6",
    keywords="vasp, dft, band-structure, materials-science",
) 