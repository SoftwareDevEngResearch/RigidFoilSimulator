import setuptools

with open("README.md", encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
    name="RigidFoilSimulation", # Replace with your own username
    version="0.0.1",
    author="Vickie Ngo",
    author_email="ngov@oregonstate.edu",
    description="This package contains modules to run an oscillating rigid foil simulation in ANSYS Fluent and performs limited data processing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SoftwareDevEngResearch/RigidFoilSimulator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pytest', 'matplotlib', 'scipy', 'os', 'sys', 'subprocess', 'shutil', 'sympy']
)