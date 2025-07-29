from setuptools import setup, find_packages

setup(
    name="django-azuread-token-validator",
    version="0.1.0",
    description="Django middleware to validate Azure AD JWT tokens and enrich requests with user data",
    author="Marlon Passos",
    author_email="marlonjbpassos@gmail.com",
    packages=find_packages(),
    install_requires=[
        "Django>=3.2",
        "PyJWT>=2.0",
        "requests>=2.25",
        "cryptography>=40.0.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
