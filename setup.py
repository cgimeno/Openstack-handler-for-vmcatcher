from sys import version_info
import os

try:
    from setuptools import setup, find_packages
except ImportError:
	try:
            from distutils.core import setup
	except ImportError:
            from ez_setup import use_setuptools
            use_setuptools()
            from setuptools import setup, find_packages
            
version = "0.0.3"
productname = "gpvcmupdate"


data_files_installdir = "/usr/share/doc/gpvcmupdate-%s" % (version)
if "VIRTUAL_ENV" in  os.environ:
    data_files_installdir = 'doc'


setup(name=productname,
    version=version,
    description="%s manages images in fedcloud for openstack" % (productname),
    long_description="""This software, fills the gap between 
[vmcatcher](https://github.com/hepix-virtualisation/vmcatcher) and 
[glancepush](https://github.com/EGI-FCTF/glancepush/wiki)""",
    author="Carlos Gimeno Yanez",
    author_email="cgimeno@bifi.es",
    license='MIT License',
    url = 'https://github.com/cgimeno/Openstack-handler-for-vmcatcher',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research'
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        ],

    scripts=['gpvcmupdate.py'],
    data_files=[(data_files_installdir ,['README.md','ChangeLog','LICENSE'])]
    )
