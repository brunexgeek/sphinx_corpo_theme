from setuptools import setup, find_packages

setup(
    name='sphinx_corpo_theme',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'sphinx.html_themes': [
            'sphinx_corpo_theme = sphinx_corpo_theme', # theme name = directory
        ]
    },
    package_data={
        'sphinx_corpo_theme': ['**/*'], # relative to the theme directory
    },
    install_requires=['sphinx>=7.0.0'],
    classifiers=[
        'Framework :: Sphinx',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
)