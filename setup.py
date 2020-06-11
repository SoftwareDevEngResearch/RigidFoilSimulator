import setuptools

with open("README.md", encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
    name="RigidFoilSimer", # Replace with your own username
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
    zip_safe=False,
    package_dir={'RigidFoilSimer':'RigidFoilSimer'},
    include_package_data=True,
    package_data={'RigidFoilSimer': [
        'AnsysFiles/*',
        'Tests/*'
        'Tests/Assets/*.txt',
        'AnsysFiles/WorkbenchProjectTemplate_files/*',
        'AnsysFiles/WorkbenchProjectTemplate_files/dp0/*',
        'AnsysFiles/WorkbenchProjectTemplate_files/dp0/FFF/DM/*',
        'AnsysFiles/WorkbenchProjectTemplate_files/dp0/FFF/MECH/*',
        'AnsysFiles/WorkbenchProjectTemplate_files/dp0/global/MECH/*',
        'AnsysFiles/WorkbenchProjectTemplate_files/user_files/*',
        ]},
    install_requires=['pytest', 'matplotlib', 'scipy', 'sympy']

)
