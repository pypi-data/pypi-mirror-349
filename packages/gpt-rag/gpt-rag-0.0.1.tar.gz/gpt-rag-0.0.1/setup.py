from setuptools import setup, find_packages

setup(
    name='gpt-rag',
    version='0.0.1',
    author='Chris Givens',
    author_email='v-cgivens@microsoft.com',
    description='GPT RAG (Retrieval-Augmented Generation) common library',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)