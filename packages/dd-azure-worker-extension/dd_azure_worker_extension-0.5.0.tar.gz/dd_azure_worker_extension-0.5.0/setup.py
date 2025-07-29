from setuptools import find_packages, setup

setup(
    name="dd-azure-worker-extension",
    version="0.5.0",
    author="Datadog",
    description="Python Worker Extension for starting Datadog Tracer and a top level span to enable auto-instrumenting of Azure Function Apps",
    include_package_data=True,
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "azure-functions >= 1.7.0, < 2.0.0",
        "ddtrace",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    license="License: Apache 2.0",
    packages=find_packages(where="."),
    zip_safe=False,
)
