import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="graiaX-not-enough-messages",  # Replace with your own username
    version="0.0.2",
    author="Xiao_Jin",
    author_email="me@xiao-jin.xyz",
    description="GraiaX -- Not Enough Messages (NEM)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jinzhijie/graiaX-nem",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
)
