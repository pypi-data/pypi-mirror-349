from setuptools import setup, find_packages

setup(
    name="efxtv-linkgen",
    version="0.1.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "linkgen = linkgen.app:main",
        ],
    },
    python_requires='>=3.6',
)

