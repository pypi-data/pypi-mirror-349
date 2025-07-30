from setuptools import setup, find_packages

setup(
    name='datachampsai',
    version='0.1.8',
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'langchain',
        'openai',
        'langchain-openai'
    ],
    entry_points={
        'console_scripts': [
            'datachampsai=datachampsai.app:run_chat_app',
        ],
    },
    author='DataChamps',
    description='A Streamlit app that refines data queries using chat context and reference instructions.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
