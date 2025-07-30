from setuptools import setup, find_packages

setup(
    name="custom_flet_components",
    version="0.1.3",
    packages=find_packages(),
    install_requires=["flet>=0.27.6"],
    tests_require=["pytest"],
    test_suite="tests",
    description="Custom Components For Flet Python",
    author="Mudassir Farooq",
    author_email="pktechmania21@gmail.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    #url="https://github.com/yourusername/custom_flet_components",
    license="MIT",
)
