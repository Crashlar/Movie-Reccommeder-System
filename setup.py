from setuptools import find_packages , setup
from typing import List
import os

HYPEN_E_DOT = "-e ."
REPO_NAME = "movie-recommender-system"


from typing import List

def get_requirements(file_path: str) -> List[str]:
    """
    Reads a requirements file and returns a list of dependencies.

    Parameters
    ----------
    file_path : str
        The path to the requirements file (e.g., 'requirements.txt').

    Returns
    -------
    List[str]
        A list of requirement strings, with newline characters removed.
    
    Notes
    -----
    - Each line in the file is treated as one requirement.
    - Newline characters at the end of each line are stripped.
    """
    
    requirements = []
    
    # Open the file in read mode
    with open(file_path) as file_obj:
        # Read all lines from the file
        requirements = file_obj.readlines()
        
        # Remove newline characters from each line
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements




setup(
    # --- Basic Info ---
    name=REPO_NAME,
    version="0.0.1",
    description="",
    author=os.getenv("AUTHOR_NAME"),
    author_email=os.getenv("AUTHOR_EMAIL"),
    url="https://github.com/Crashlar/multi-ml-project",

    # =========================
    #  Package Configuration
    # =========================
    packages=find_packages(),
    python_requires=">=3.11",

    # =========================
    #  Dependencies
    # =========================
    install_requires=get_requirements("requirements.txt"),


    # =========================
    #  Entry Points (CLI)
    # =========================
    entry_points={
        "console_scripts": [
            "mypackage-cli=mypackage.__main__:app",
        ],
    },

    # =========================
    #  Package Data (Optional)
    # =========================
    include_package_data=True,
    package_data={
        # changes futher through template creation
        "mypackage": ["data/*.txt" , "data/*.csv", "config/*.yaml"],
    },
)
