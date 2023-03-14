import setuptools


AUTHORS = ['Felix Book']

with open('requirements.txt', 'r') as f:
  requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
      name='control_block_diagram',
      version='0.6.0',
      description='Visualization of controller block diagrams',
      packages=setuptools.find_packages(),
      install_requires=requirements,
      python_requires='>=3.6',
      author=', '.join(sorted(AUTHORS, key=lambda n: n.split()[-1].lower())),
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/upb-lea/control-block-diagram",
      )
