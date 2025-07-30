from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

class CreateExeCommand(install):
    def run(self):
        install.run(self)
        subprocess.call(['pyinstaller', '--onefile', '--windowed', '--add-data', '.;.', 'main.py'])


setup(
    name="App",
    version="1.0",
    description="",
    author="Author",
    scripts=["main.py"],
    packages=find_packages(),
    include_package_data=True,
    cmdclass={
        'make_exe': CreateExeCommand,
    }
)