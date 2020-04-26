import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
with open('requirements.txt') as f:
    requirements = f.readlines()
setuptools.setup(
    name="adara-framework-core",  # Replace with your own username
    version="0.0.4",
    author="DOT",
    author_email="dot@adara.com",
    description="An API framework for simplified development",
    long_description="Sample",
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://bitbucket.org/adarainc/framework-base",
    packages=['framework.core'],
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['create_api=framework.core.setup.command_line:main'],
    },
    python_requires='>=3.6',
    install_requires=requirements
)
