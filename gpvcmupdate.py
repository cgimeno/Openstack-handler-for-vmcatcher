#!/usr/bin/env python
"""
NAME: gpvmcupdate
AUTOR: Carlos Gimeno
EMAIL: cgimeno@bifi.es
DESCPRTION: Used by vmcatcher as a hook for images updates
            Inform glancepush for image updates.

            This program will write files on different locations, so run as root
            (not recommended) or be careful with permissions!
"""
import os
import sys
import tarfile
import stat



def main():
    spooldir = "/var/spool/glancepush/"
    metadata_dir = "/etc/glancepush/meta/"
    transform_dir = "/etc/glancepush/transform/"
    test_dir = "/etc/glancepush/test/"
    temp_dir = "/tmp/"

    dir_cache = os.getenv('VMCATCHER_CACHE_DIR_CACHE', 0)
    event_dc_title = os.getenv('VMCATCHER_EVENT_DC_TITLE', 0)
    identifier = os.getenv('VMCATCHER_EVENT_DC_IDENTIFIER')
    if (dir_cache == 0) or (event_dc_title == 0) or (identifier == 0):
        sys.stderr.write("Some Variables are not set")
        os._exit(1)

    # I'm going to replace backslashes and spaces to avoid problems
    image = spooldir + os.getenv('VMCATCHER_EVENT_DC_TITLE').replace(" ","_").replace("/","_")
    sys.stdout.write(os.getenv('VMCATCHER_EVENT_TYPE'))
    metadata = metadata_dir + os.getenv('VMCATCHER_EVENT_DC_TITLE').replace(" ","_").replace("/","_")
    transform = transform_dir + os.getenv('VMCATCHER_EVENT_DC_TITLE').replace(" ","_").replace("/","_")
    test = test_dir + os.getenv('VMCATCHER_EVENT_DC_TITLE').replace(" ","_").replace("/","_")

    with open(image, "w") as outfile:
        if os.getenv('VMCATCHER_EVENT_HV_FORMAT').lower() == "ova":
            to_file = "file=" + temp_dir + os.getenv('VMCATCHER_EVENT_DC_IDENTIFIER')
        else:
            to_file = "file=" + os.getenv('VMCATCHER_CACHE_DIR_CACHE') + '/' + os.getenv('VMCATCHER_EVENT_DC_IDENTIFIER')
        outfile.write(to_file)
        outfile.close()

    if os.getenv('VMCATCHER_EVENT_TYPE') == 'ProcessPostfix':
        # We need to check if image is expired
        if os.path.isfile(os.getenv('VMCATCHER_CACHE_DIR_EXPIRE') + '/' + os.getenv('VMCATCHER_EVENT_FILENAME')):
            sys.stdout.write(" Removing " + image)
            os.remove(image)
            os.remove(metadata)
            os.remove(transform)
            os.remove(test)
            # Remove expired images? Why? Why not?
            os.remove(os.getenv('VMCATCHER_CACHE_DIR_EXPIRE') + '/' + os.getenv('VMCATCHER_EVENT_FILENAME'))
    elif os.getenv('VMCATCHER_EVENT_TYPE') == 'AvailablePostfix':
        # Wait! Is an OVA Image?
        if os.getenv('VMCATCHER_EVENT_HV_FORMAT').lower() == "ova":
            # Ova File. We must extract VMDK and VDF, discard VDF and upload VMDK
            # Also, we must convert it to qcow2 to provide compatibility with old qemu versions
            downloaded_image = os.getenv('VMCATCHER_CACHE_DIR_CACHE') + '/' + os.getenv('VMCATCHER_EVENT_DC_IDENTIFIER')
            tfile = tarfile.open(downloaded_image)
            if tarfile.is_tarfile(downloaded_image):
                tfile.extractall(temp_dir)

            for file in os.listdir(temp_dir):
                if file.endswith(".ovf"):  # Delete OVF File
                    os.remove(temp_dir + file)
                elif file.endswith(".vmdk"):
                    command = "qemu-img convert -f vmdk -O qcow2 " + temp_dir + file + " " + temp_dir + file + ".qcow2"
                    os.system(command) # Convert image to qcow2
		    os.remove(temp_dir + file) # Delete old VMDK file
                    os.rename(temp_dir + file + ".qcow2", temp_dir + os.getenv('VMCATCHER_EVENT_DC_IDENTIFIER'))

        sys.stdout.write("Creating Metadata Files")
        with open(metadata, "w") as outfile:
            outfile.write("comment=\"" + os.getenv('VMCATCHER_EVENT_SL_COMMENTS') + "\"\n")
            #Images should be public? I think not
            outfile.write("is_public=\"no\"\n")
			#Careful. OpenStack Grizzly wont' allow you to delete protected images.
			#OpenStack Havana works fine.
            outfile.write("is_protected=\"no\"\n") # Protected?
            if os.getenv('VMCATCHER_EVENT_HV_FORMAT').lower() == "ova":
                outfile.write("disk_format=\"qcow2" + "\"\n")
            else:
                outfile.write("disk_format=\"" + os.getenv('VMCATCHER_EVENT_HV_FORMAT') + "\"\n")
            outfile.write("container_format=\"bare\"")
            outfile.close()
        # TODO: Load custom test script
        with open(transform, "w") as outfile:
            outfile.write("#!/bin/sh\n")
            outfile.write("cat")
            outfile.close()
        # TODO: Load Custom Transform Script
        with open(test, "w+") as outfile:
            outfile.write("#!/bin/sh\n")
            outfile.write("cat")
            outfile.close()
        #Grant execution access to owner
        os.chmod(transform,stat.S_IEXEC)
    pass


if __name__ == "__main__":
    main()

