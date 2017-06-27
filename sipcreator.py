#!/usr/bin/env python
'''
Generates SIPS by calling various microservices and functions.
'''
import os
import argparse
import ififuncs
import sys
import subprocess


def make_folder_path(path):
    '''
    Generates objects/logs/metadata/UUID folder structure in output.
    Returns the path.
    '''
    representation_uuid = ififuncs.create_uuid()
    path = os.path.join(path, representation_uuid)
    ififuncs.make_folder_structure(path)
    return path

def extract_checksums(manifest, path_list, basename):
    new_manifest = []
    manifest_ =  '/%s_manifest.md5' % basename
    desktop_manifest_dir = ififuncs.make_desktop_manifest_dir()
    manifest_textfile = "%s/%s" % (desktop_manifest_dir, manifest_)
    if os.path.isfile(manifest):
        with open(manifest, 'r') as fo:
            manifest_lines = fo.readlines()
            for path in path_list:
                for i in manifest_lines:
                    if path in i:
                        if path[0] == '/':
                            path = path[1:]
                        new_manifest.append(i[:32] + '  ' + path)
    with open(manifest_textfile,"wb") as fo:
        for i in new_manifest:
            fo.write(i + '\n')


def get_relative_filepaths(inputs):
    path_list = []
    for paths in inputs:
        for root, dirnames, filenames in os.walk(paths):
            for filename in filenames:
                path_list.append(os.path.join(root.replace(paths,''), filename))
    return sorted(path_list)

def main():
    '''
    Generates SIPS by calling various microservices and functions.
    '''
    parser = argparse.ArgumentParser(
        description='Wraps objects into a SIP'
        ' Written by Kieran O\'Leary.'
    )
    parser.add_argument(
        '-i', nargs='+',
        help='full path of input directory', required=True
    )
    parser.add_argument(
        '-o', '-output',
        help='full path of output directory', required=True
    )
    parser.add_argument(
        '-m', '-manifest',
        help='full path to a pre-existing manifest'
    )
    args = parser.parse_args()
    sip_path = make_folder_path(os.path.join(args.o))
    path_list = get_relative_filepaths(args.i)
    print sip_path
    '''
    print args.i
    basename = os.path.basename(args.i[0])
    
    print basename
    extract_checksums(args.m, path_list, basename)
    '''
    for t in args.i:
        print t
        moveit_cmd = [
                        sys.executable,
                        os.path.expanduser("~/ifigit/ifiscripts/moveit.py"),
                        t, os.path.join(sip_path, 'objects')]
        subprocess.check_call(moveit_cmd)
        
        '''
        bring ubunutu and macbook to loopline,do transfers there
        take manifests, add uuid, put in correct location, delete orig manifests
        '''

if __name__ == '__main__':
    main()
