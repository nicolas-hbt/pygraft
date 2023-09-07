from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'pygraft',
  version = '0.1.1',
  packages = find_packages(),
  package_data={
        'pygraft': ['examples/template.json', 'examples/template.yml', 'property_checks/combinations.json', 'property_checks/compat_p1p2_inverseof.txt']
  },
  license='MIT',
  description = 'PyGraft: Configurable Generation of Schemas and Knowledge Graphs at Your Fingertips',
  author = 'Nicolas Hubert',
  author_email = 'nicolas.hubert@univ-lorraine.fr',
  url = 'https://github.com/nicolas-hbt',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
  # py_modules=["generate"],
  long_description=long_description,
  long_description_content_type="text/markdown",
  keywords = ['Knowledge Graph',
              'Ontology', 
              'Schema',
              'Semantic Web',
              'Synthetic Data Generator'],
  install_requires=[            
          'art',
          'numpy',
          'Owlready2',
          'rdflib',
          'tabulate',
          'tqdm',
          'pyyaml'
      ],
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