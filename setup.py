from setuptools import setup, find_packages

setup(
    name='nlp_job_analysis',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'nltk',
        'scikit-learn',
        'spacy'
    ],
    entry_points={
        'console_scripts': [
            'nlp_job_analysis=nlp_job_analysis.main:main',
        ],
    },
)