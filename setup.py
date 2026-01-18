from setuptools import setup, find_packages

setup(
    name="khmer_nlp_toolkits",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "khmer_nlp_toolkits": [
            "utils/segment/model/*.bin"
        ],
    },

)
