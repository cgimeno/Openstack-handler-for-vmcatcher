Openstack handler for vmcatcher
===============================

This software, fills the gap between [vmcatcher](https://github.com/hepix-virtualisation/vmcatcher) and [glancepush](https://github.com/EGI-FCTF/glancepush/wiki)

Registering and creating required files to each new image manually doesn't make any sense, so I've developed my own solution for OpenStack

Requirements:

 - **Python 2.7.3** (Tested)
 - **qemu-img 1.2.0+** (You'll need to convert images from VMDK to qcow2 format)



----------
First of all, you'll need to install vmcatcher. You can find detailed instructions about how to install it [here](https://github.com/hepix-virtualisation/vmcatcher). Install [glancepush](https://github.com/EGI-FCTF/glancepush/wiki)
Export all required enviroment variables. For example:

    export VMCATCHER_RDBMS="sqlite:////var/lib/vmcatcher/vmcatcher.db"
    export VMCATCHER_CACHE_DIR_CACHE="/var/lib/vmcatcher/cache"
    export VMCATCHER_CACHE_DIR_DOWNLOAD="/var/lib/vmcatcher/cache/partial"
    export VMCATCHER_CACHE_DIR_EXPIRE="/var/lib/vmcatcher/cache/expired"
    export VMCATCHER_CACHE_EVENT="python /var/lib/vmcatcher/gpvcmupdate.py"

Subscribe to an image list:

    vmcatcher_subscribe  -s https://cernvm.cern.ch/releases/image.list

List all available images:

    vmcatcher_image -l
    327016b0-6508-41d2-bce0-c1724cb3d3e2    2       63175437-7d59-4851-b333-c96cb6545a86
    858a817e-0ca2-473f-89d3-d5bdfc51968e    3       63175437-7d59-4851-b333-c96cb6545a86
    da42ca85-179b-4873-b12e-32d549bf02b6    2       63175437-7d59-4851-b333-c96cb6545a86

Subscribe to an image:

    vmcatcher_image -a -u 327016b0-6508-41d2-bce0-c1724cb3d3e2

Launch vmcatcher_cache. The image downloading will start automatically. When it finishes, you'll see the necessary files for glancepush at /etc/glancepush/meta, /etc/glancepush/test, /etc/glancepush/transform. Launch gpupdate and the image will be uploaded to Openstack. If image passes all policy checks, it will be published to your site.


----------


Troubleshooting
===============================

**qemu-img: error while reading sector 131072:** If you see this error, you need to update qemu.

Ubuntu 12.04 LTS doesn't have the latest version in his repositories.

You can solve it by adding this PPA repository to your sources:

    add-apt-repository ppa:miurahr/vagrant

If you don't want to add new sources, or you're not using a Debian based system, you can always download the source from qemu webpage.
