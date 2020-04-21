import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="adara-framework",  # Replace with your own username
    version="0.0.1",
    author="DOT",
    author_email="dot@adara.com",
    description="An API framework for simplified development",
    long_description="Sample",
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/adarainc/framework-base",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['create_api=framework.core.setup.command_line:main'],
    },
    python_requires='>=3.6',
    install_requires=[
        "connexion[swagger-ui]>=2.6.0,<3",
        "aiohttp>=3.6.2<4",
        "uvicorn>=0.11.3,<1",
        "gunicorn>=20.0.4,<21",
        "aiohttp_jinja2>=1.2.0,<2",
        "python-jose[cryptography]>=3.0.1,<4",
        "auth[security]>=2.7.0,<3",

    ]
)
