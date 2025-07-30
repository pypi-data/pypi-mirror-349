from setuptools import find_packages, setup

setup(
    name="fraudaverse",
    packages=find_packages(include=["fraudaverse"]),
    version="0.0.6",
    description="Python lib to access FraudAverse analytical capabilities",
    author="FraudAverse GmbH",
    install_requires=["pyarrow", "python-dotenv", "pandas"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "xgboost", "pandas", "numpy"],
    test_suite="tests",
)
