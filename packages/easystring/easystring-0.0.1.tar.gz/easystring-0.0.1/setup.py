from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'Programming Language :: Python :: 3'
]

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
  name='easystring',
  version='0.0.1',
  description='a toolkit of necessary & useful string operations',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='',  
  author='Ashish Kumar Dash',
  author_email='ashishdash2410@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='string', 
  packages=find_packages(),
  install_requires=[]
)
