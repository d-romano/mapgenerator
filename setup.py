import setuptools


# Copy README as description
with open("README.md", "r") as fh:
	long_description  = fh.read()


def requirements():
	with open('requirements.txt') as f:
		reqs = [req.strip() for req in f]
	return reqs

# Allows for compiling of shared c++ libraries.
dsMod = setuptools.Extension('dr_mapgen.diamondsquare.diamond', sources = ['diamondsquare/DiamondSquare.cpp'],)
pnMod = setuptools.Extension('dr_mapgen.perlin.perlin', sources = ['perlin/Perlin.cpp'],)

# Metadata for setup.
setuptools.setup(
	name='dr_mapgen',
	version="0.0.1",
	author="Daniel Romano",
	author_email="drom96@gmail.com",
	description="A simple randomized map generator",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/d-romano/mapgenerator",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Lanugage :: Python :: 3",
		"Programming Language :: C++",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=requirements(),
	python_requires=">=3.6",
	ext_modules=[dsMod, pnMod]
)