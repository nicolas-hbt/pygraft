from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
  name = 'pygraft',
  version = '0.0.3',
  packages = find_packages(exclude=('docs')),
  include_package_data=True,
  zip_safe=False,
  package_data={
        'pygraft': ['examples/template.json', 'examples/template.yml', 'property_checks/combinations.json', 'property_checks/compat_p1p2_inverseof.txt']
  },
    entry_points={
    'console_scripts': [
        'pygraft = pygraft.main:main',
    ],
  },
  license='MIT',
  description = 'PyGraft: Configurable Generation of Schemas and Knowledge Graphs at Your Fingertips',
  author = 'Nicolas Hubert',
  author_email = 'nicolas.hubert@univ-lorraine.fr',
  url = 'https://github.com/nicolas-hbt',
  long_description=long_description,
  long_description_content_type="text/markdown",
  keywords = ['Knowledge Graph',
              'Ontology', 
              'Schema',
              'Semantic Web',
              'Synthetic Data Generator'],
  install_requires=[ 
      'numpy>=1.24.0',         
      'matplotlib>=3.7.0',
      'Owlready2>=0.41',
      'rdflib>=6.2.0',
      'pyyaml',
      'tabulate',
      'art',
      'tqdm'
      ],
  python_requires='>=3.7',
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Information Analysis'
  ],
)
