from setuptools import setup, find_packages

setup(
    name="transcriber_service",
    version="0.1.0",
    description="A toolkit for transcribing",
    author="Tatsiana Kozlova",
    author_email="tanya126060@gmail.com",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "pydantic>=2.11.4",
        "typing>=3.7.4.3",
        "password_strength>=0.0.3.post2",
        "email_validator>=2.2.0",
        "python-docx>=1.1.2",
        "pymongo>=4.12.1",
        "msgpack>=1.1.0",
        "audio_transcribing>=0.2.6",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries",
    ],
    include_package_data=True,
    zip_safe=False,
)
