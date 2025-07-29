import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="korcen",  # Replace with your own PyPI username(id)
    version="1.0.2",
    author="Tanat",
    author_email="shrbwjd05@naver.com",
    description="한국어 비속어 검열",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KR-korcen/korcen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["better_profanity","OrderedDict"],
    python_requires='>=3.6',
)
