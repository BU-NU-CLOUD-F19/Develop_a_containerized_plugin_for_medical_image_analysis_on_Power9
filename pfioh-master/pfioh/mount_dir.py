"""
Handle MountDir file storage
"""

import shutil
import datetime
import zipfile
import zlib
import gzip
import base64
import os
import ast
from   io                   import BytesIO
from   io                   import StringIO
from   pfioh                import StoreHandler
from   pfioh                import base64_process, zip_process, zipdir
from   pfmisc._colors       import Colors

import pudb

class MountDir(StoreHandler):

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dp.qprint('MountDir initialized')
        

    def storeData(self, **kwargs):
        """
        Stores the file/directory at the specified location
        """

        for k,v in kwargs.items():
            if k == 'input_stream': inputStream     = v
            if k == 'client_path': str_clientPath   = v
            if k == 'path': str_destPath            = v
            if k == 'is_zip': b_zip                 = v
            if k == 'd_ret': d_ret                  = v
        
        if not os.path.exists(str_destPath):
            os.mkdir(str_destPath)
        if b_zip:
            with zipfile.ZipFile(inputStream, 'r') as zipfileObj:
                zipfileObj.extractall(path=str_destPath)
            d_ret['write']['file'] = str_destPath
        else:
            filePath = os.path.join(str_destPath, str_clientPath.split('/')[-1])
            f = open(filePath, 'wb')
            buf = 16*1024
            while 1:
                chunk = inputStream.read(buf)
                if not chunk:
                    break
                f.write(chunk)
            f.close()
            d_ret['write']['file'] = filePath
        d_ret['write']['status']    = True
        d_ret['write']['msg']       = 'File written successfully!'
        d_ret['write']['timestamp'] = '%s' % datetime.datetime.now()
        d_ret['status']             = True
        d_ret['msg']                = d_ret['write']['msg']

        return d_ret


    def getData(self, **kwargs):
        """
        Gets the file/directory from the specified location, zips and/or encodes it
        and sends it to the client
        """

        for k,v in kwargs.items():
            if k == 'path':     str_localPath   = v 
            if k == 'is_zip':   b_zip           = v
            if k == 'cleanup':  b_cleanup       = v
            if k == 'd_ret':    d_ret           = v
            if k == 'key':      key             = v
    
        if b_zip:
            with zipfile.ZipFile('/tmp/{}.zip'.format(key), 'w', compression=zipfile.ZIP_DEFLATED) as zipfileObj:
                for root, dirs, files in os.walk(str_localPath):
                    for filename in files:
                        arcname = os.path.join(root, filename)[len(str_localPath.rstrip(os.sep))+1:]
                        zipfileObj.write(os.path.join(root, filename), arcname=arcname)
                        fileToProcess = "/tmp/{}.zip".format(key)
        else:
            fileToProcess = os.walk(str_localPath).next()[2][0]
        d_ret['status'] = True
        d_ret['msg'] = "File/Directory downloaded"
        self.buffered_response(fileToProcess)
        if b_cleanup:
            if b_zip:
                self.dp.qprint("Removing '%s'..." % (fileToProcess), comms = 'status')
                if os.path.isfile(fileToProcess): os.remove(fileToProcess)

        return d_ret
