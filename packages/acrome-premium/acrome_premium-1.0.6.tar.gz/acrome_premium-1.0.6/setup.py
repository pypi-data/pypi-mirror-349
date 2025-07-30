import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setuptools.setup(
	name="acrome-premium",
	version="1.0.6",
	author="Berat Computer",
	author_email="beratdogan@acrome.net",
	description="Premium Board communication library. -limit switches are added.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/acrome-robotics/python-library",
	project_urls={
		"Bug Tracker": "https://github.com/acrome-robotics/python-library/issues",
    	},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	packages=setuptools.find_packages(exclude=['tests', 'test']),
	install_requires=["pyserial", "crccheck", "stm32loader==0.5.1", "requests"],
	python_requires=">=3.6"
)
