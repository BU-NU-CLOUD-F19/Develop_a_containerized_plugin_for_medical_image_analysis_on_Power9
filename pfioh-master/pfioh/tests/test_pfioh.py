import  unittest
import  urllib
import  sys
import  os
import  http
from    unittest        import     TestCase
from    argparse        import     ArgumentParser
from    argparse        import     RawTextHelpFormatter
from    unittest        import     mock
from    cgi             import     FieldStorage
from    unittest.mock   import     patch, MagicMock

try:
    sys.path.insert(0,'/home/travis/build/FNNDSC/pfioh/pfioh')
    sys.path.insert(0, os.path.dirname(http.__file__))
    import mount_dir
    import swift_store
    import pfioh
    import server
    
except Exception as err:
    import mount_dir
    import swift_store


str_desc    = """
        
                                    pfioh -- internal testing

"""

class TestPfioh(TestCase):

    def test_pfioh_constructor(self):

        parser  = ArgumentParser(description = str_desc, formatter_class = RawTextHelpFormatter)

        parser.add_argument(
            '--ip',
            action  = 'store',
            dest    = 'ip',
            default = 'localhost',
            help    = 'IP to expose.'
        )
        parser.add_argument(
            '--port',
            action  = 'store',
            dest    = 'port',
            default = '5055',
            help    = 'Port to use.'
        )
        parser.add_argument(
            '--forever',
            help    = 'if specified, serve forever, otherwise terminate after single service.',
            dest    = 'b_forever',
            action  = 'store_true',
            default = False
        )
        parser.add_argument(
            '--storeBase',
            action  = 'store',
            dest    = 'storeBase',
            default = '/tmp',
            help    = 'Base path for internal storage.'
        )
        parser.add_argument(
            '--swift-storage',
            action  = 'store_true',
            dest    = 'b_swiftStorage',
            default = False,
            help    = 'If specified, use Swift as object Storage'
        )
        parser.add_argument(
            '--httpResponse',
            help    = 'if specified, return HTTP responses',
            dest    = 'b_httpResponse',
            action  = 'store_true',
            default = False
        )
        parser.add_argument(
            '--createDirsAsNeeded',
            help    = 'if specified, allow the service to create base storage directories as needed',
            dest    = 'b_createDirsAsNeeded',
            action  = 'store_true',
            default = False
        )

        args            = parser.parse_args()
        args.port       = int(args.port)

        server          = pfioh.ThreadedHTTPServer((args.ip, args.port), pfioh.StoreHandler)
        server.setup(args = vars(args), desc = str_desc)

        handler     = pfioh.StoreHandler(test = True)
        handler.do_POST(
            d_msg = {
                "action": "hello",
                "meta": {
                    "askAbout":     "sysinfo",
                    "echoBack":     "Hi there!"
                }
            }
        )
        self.assertTrue(True)



class TestFilesPush(TestCase):
    """
    Tests the file push operation and internally mountdir and swift functionality
    """

    def setUp(self):
        #Create the json message
        """
        PushPath request= 
        '{  
        "action": "pushPath", \
                    "meta": { \
                        "remote": { \
                            "key":         "121215" \
                        }, \
                        "local": { \
                            "path":         "/tmp/datadir" \
                        }, \
                        "transport": { \
                            "mechanism":    "compress", \
                            "compress": { \
                                "archive":  "zip", \
                                "unpack":   true, \
                                "cleanup":  true \
                            } \
                        } \
                    } \
        }'
        """

        self.storeObject = mount_dir.MountDir(test=True)

        self.length = 1660

        self.data = b'--------------------------ab333d11461fc3e3\r\nContent-Disposition: form-data; name="local"; filename="81d9a05a-4eff-4c8a-9de4-930dab3fc32b.zip.b64"\r\nContent-Type: application/octet-stream\r\n\r\nUEsDBBQAAAAIAHN2AkuemRG8BwAAAAUAAAANAAAAZGF0YWRpci8yLnR4dMvMUzDiAgBQSwMEFAAAAAgAqG4CS13KPJcHAAAABQAAAA0AAABkYXRhZGlyLzEudHh0y8xTMOQCAFBLAwQUAAAACACFdgJL36gKpQcAAAAFAAAAEgAAAGRhdGFkaXIvZGF0YS8zLnR4dMvMUzDmAgBQSwMEFAAAAAgAmXYCS88IW5JZAAAAmwAAADUAAABkYXRhZGlyL2RhdGEvODFkOWEwNWEtNGVmZi00YzhhLTlkZTQtOTMwZGFiM2ZjMzJiLnppcAvwZmYRYWBg4GAoLmPynjdTcA87kMcKxLxAnJJYkpiSWaRvpFdSUXL6TLDBIyaGALiOFXlM3rGnbKZj02EI0/EEWUcr0I77K7iWwnQIIekA0frGMG3PmBgAUEsBAhQDFAAAAAgAc3YCS56ZEbwHAAAABQAAAA0AAAAAAAAAAAAAALSBAAAAAGRhdGFkaXIvMi50eHRQSwECFAMUAAAACACobgJLXco8lwcAAAAFAAAADQAAAAAAAAAAAAAAtIEyAAAAZGF0YWRpci8xLnR4dFBLAQIUAxQAAAAIAIV2AkvfqAqlBwAAAAUAAAASAAAAAAAAAAAAAAC0gWQAAABkYXRhZGlyL2RhdGEvMy50eHRQSwECFAMUAAAACACZdgJLzwhbklkAAACbAAAANQAAAAAAAAAAAAAAtIGbAAAAZGF0YWRpci9kYXRhLzgxZDlhMDVhLTRlZmYtNGM4YS05ZGU0LTkzMGRhYjNmYzMyYi56aXBQSwUGAAAAAAQABAAZAQAARwEAAAAA\r\n--------------------------ab333d11461fc3e3\r\nContent-Disposition: form-data; name="d_msg"\r\n\r\n{"meta": {"local": {"path": "/tmp/datadir"}, "transport": {"checkRemote": false, "compress": {"unpack": true, "cleanup": true, "archive": "zip"}, "mechanism": "compress"}, "remote": {"key": "121215"}}, "action": "pushPath"}\r\n--------------------------ab333d11461fc3e3\r\nContent-Disposition: form-data; name="filename"\r\n\r\n81d9a05a-4eff-4c8a-9de4-930dab3fc32b.zip.b64\r\n--------------------------ab333d11461fc3e3--\r\n'

        self.form = 'FieldStorage(None, None, [FieldStorage(\'local\', \'7d97663b-191d-4175-a9dd-5bf28a6803c2.zip.b64\', b\'UEsDBBQAAAAIAHqDCUuemRG8BwAAAAUAAAANAAAAZGF0YWRpci8yLnR4dMvMUzDiAgBQSwMEFAAAAAgAeIMJS13KPJcHAAAABQAAAA0AAABkYXRhZGlyLzEudHh0y8xTMOQCAFBLAwQUAAAACABOhwlLNpTSE0MAAABkAAAANQAAAGRhdGFkaXIvZGF0YS83ZDk3NjYzYi0xOTFkLTQxNzUtYTlkZC01YmYyOGE2ODAzYzIuemlwC/BmZhFhYGDgYKhq5vSeN1NwDzuQxwrEvECckliSmJJZpG+kV1JRcvpMsMEjJoYAuI4KoI7YUzbTsekwhOl4wsQAAFBLAwQUAAAACACEgwlL36gKpQcAAAAFAAAAEgAAAGRhdGFkaXIvZGF0YS8zLnR4dMvMUzDmAgBQSwECFAMUAAAACAB6gwlLnpkRvAcAAAAFAAAADQAAAAAAAAAAAAAAtIEAAAAAZGF0YWRpci8yLnR4dFBLAQIUAxQAAAAIAHiDCUtdyjyXBwAAAAUAAAANAAAAAAAAAAAAAAC0gTIAAABkYXRhZGlyLzEudHh0UEsBAhQDFAAAAAgATocJSzaU0hNDAAAAZAAAADUAAAAAAAAAAAAAALSBZAAAAGRhdGFkaXIvZGF0YS83ZDk3NjYzYi0xOTFkLTQxNzUtYTlkZC01YmYyOGE2ODAzYzIuemlwUEsBAhQDFAAAAAgAhIMJS9+oCqUHAAAABQAAABIAAAAAAAAAAAAAALSB+gAAAGRhdGFkaXIvZGF0YS8zLnR4dFBLBQYAAAAABAAEABkBAAAxAQAAAAA=\'), FieldStorage(\'d_msg\', None, \'{"action": "pushPath", "meta": {"remote": {"key": "121215"}, "local": {"path": "/tmp/datadir"}, "transport": {"compress": {"cleanup": true, "unpack": true, "archive": "zip"}, "mechanism": "compress", "checkRemote": false}}}\'), FieldStorage(\'filename\', None, \'7d97663b-191d-4175-a9dd-5bf28a6803c2.zip.b64\')])\''
        self.d_form = {'d_msg': '{"meta": {"local": {"path": "/tmp/datadir"}, "transport": {"compress": {"cleanup": true, "archive": "zip", "unpack": true}, "checkRemote": false, "mechanism": "compress"}, "remote": {"key": "121215"}}, "action": "pushPath"}', 'filename': 'a573d22f-2621-4174-827b-2b91798d6007.zip.b64', 'local': b'UEsDBBQAAAAIAHN2AkuemRG8BwAAAAUAAAANAAAAZGF0YWRpci8yLnR4dMvMUzDiAgBQSwMEFAAAAAgAqG4CS13KPJcHAAAABQAAAA0AAABkYXRhZGlyLzEudHh0y8xTMOQCAFBLAwQUAAAACACFdgJL36gKpQcAAAAFAAAAEgAAAGRhdGFkaXIvZGF0YS8zLnR4dMvMUzDmAgBQSwMEFAAAAAgA0nkCS88IW5JZAAAAmwAAADUAAABkYXRhZGlyL2RhdGEvYTU3M2QyMmYtMjYyMS00MTc0LTgyN2ItMmI5MTc5OGQ2MDA3LnppcAvwZmYRYWBg4GAoLmPynjdTcA87kMcKxLxAnJJYkpiSWaRvpFdSUXL6TLDBIyaGALiOFXlM3rGnbKZj02EI0/EEWUcr0I77K7iWwnQIIekA0frGMG3PmBgAUEsBAhQDFAAAAAgAc3YCS56ZEbwHAAAABQAAAA0AAAAAAAAAAAAAALSBAAAAAGRhdGFkaXIvMi50eHRQSwECFAMUAAAACACobgJLXco8lwcAAAAFAAAADQAAAAAAAAAAAAAAtIEyAAAAZGF0YWRpci8xLnR4dFBLAQIUAxQAAAAIAIV2AkvfqAqlBwAAAAUAAAASAAAAAAAAAAAAAAC0gWQAAABkYXRhZGlyL2RhdGEvMy50eHRQSwECFAMUAAAACADSeQJLzwhbklkAAACbAAAANQAAAAAAAAAAAAAAtIGbAAAAZGF0YWRpci9kYXRhL2E1NzNkMjJmLTI2MjEtNDE3NC04MjdiLTJiOTE3OThkNjAwNy56aXBQSwUGAAAAAAQABAAZAQAARwEAAAAA'}

        self.filename = '/tmp/share/key-121215/datadir.zip'

        self.filecontent = b'PK\x03\x04\x14\x00\x00\x00\x08\x00sv\x02K\x9e\x99\x11\xbc\x07\x00\x00\x00\x05\x00\x00\x00\r\x00\x00\x00datadir/2.txt\xcb\xccS0\xe2\x02\x00PK\x03\x04\x14\x00\x00\x00\x08\x00\xa8n\x02K]\xca<\x97\x07\x00\x00\x00\x05\x00\x00\x00\r\x00\x00\x00datadir/1.txt\xcb\xccS0\xe4\x02\x00PK\x03\x04\x14\x00\x00\x00\x08\x005}\x02K\x0b h\x18D\x00\x00\x00d\x00\x00\x005\x00\x00\x00datadir/data/786dcffd-5a0d-4e17-9c9d-4e0ccc69ab6d.zip\x0b\xf0ff\x11a``\xe0`(.c\xf2\x9e7Sp\x0f;\x90\xc7\n\xc4\xbc@\x9c\x92X\x92\x98\x92Y\xa4o\xa4WRQr\xfaL\xb0\xc1#&\x86\x00\xb8\x8e\x15yL\xde\xb1\xa7l\xa6c\xd3a\x08\xd3\xf1\x84\x89\x01\x00PK\x03\x04\x14\x00\x00\x00\x08\x00\x85v\x02K\xdf\xa8\n\xa5\x07\x00\x00\x00\x05\x00\x00\x00\x12\x00\x00\x00datadir/data/3.txt\xcb\xccS0\xe6\x02\x00PK\x01\x02\x14\x03\x14\x00\x00\x00\x08\x00sv\x02K\x9e\x99\x11\xbc\x07\x00\x00\x00\x05\x00\x00\x00\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb4\x81\x00\x00\x00\x00datadir/2.txtPK\x01\x02\x14\x03\x14\x00\x00\x00\x08\x00\xa8n\x02K]\xca<\x97\x07\x00\x00\x00\x05\x00\x00\x00\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb4\x812\x00\x00\x00datadir/1.txtPK\x01\x02\x14\x03\x14\x00\x00\x00\x08\x005}\x02K\x0b h\x18D\x00\x00\x00d\x00\x00\x005\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb4\x81d\x00\x00\x00datadir/data/786dcffd-5a0d-4e17-9c9d-4e0ccc69ab6d.zipPK\x01\x02\x14\x03\x14\x00\x00\x00\x08\x00\x85v\x02K\xdf\xa8\n\xa5\x07\x00\x00\x00\x05\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb4\x81\xfb\x00\x00\x00datadir/data/3.txtPK\x05\x06\x00\x00\x00\x00\x04\x00\x04\x00\x19\x01\x00\x002\x01\x00\x00\x00\x00'

        self.storeObject.headers = {'Content-Type' : 'some type', 'Content-length' : 1660, 'user-agent' : 'PycURL/7.43.0 libcurl/7.35.0 OpenSSL/1.0.1f zlib/1.2.8 libidn/1.28 librtmp/2.3'}  

        self.Path = '/tmp/share/key-121215'

        self.d_msg = {'meta': {'remote': {'key': '121215'}, 'local': {'path': '/tmp/datadir'}, 'transport': {'mechanism': 'compress', 'compress': {'cleanup': True, 'unpack': True, 'archive': 'zip'}, 'checkRemote': False}}, 'action': 'pushPath'}

        self.d_ret = {'decode': {'msg': 'base64 decode successful!', 'status': True}, 'write': {}}

    @patch('pfioh.StoreHandler.do_POST_withCompression')
    @patch('pfioh.StoreHandler.do_POST_withCopy')
    @patch('pfioh.StoreHandler.getHeaders')
    @patch('pfioh.StoreHandler.rfileRead')
    @patch('pfioh.StoreHandler.unpackForm')
    @patch('pfioh.StoreHandler.ret_client')
    def test_doPost(self, mock_retClient, mock_formUnpack, mock_data, mock_length, mock_postCopy, mock_postCompress):
        mock_length.return_value = 1660
        mock_data.return_value = self.data
        mock_formUnpack.return_value = self.d_msg
        mock_retClient.return_value = None

        d_ret = self.storeObject.do_POST()
        assert mock_postCopy.call_count == 0
        assert mock_postCompress.call_count == 1
 
    @patch('pfioh.StoreHandler.remoteLocation_resolve')
    @patch('mount_dir.MountDir.storeData')
    @patch('pfioh.StoreHandler.send_response')
    @patch('pfioh.StoreHandler.end_headers')
    def test_doPostwithCompression(self, mock_endHeaders, mock_sendResponse, mock_store_data, mock_remoteLocation_resolve):
        
        mock_remoteLocation_resolve.return_value = {'path': '/tmp/share/somefolder'}
        mock_sendResponse.return_value = 'Response has been sent'
        mock_store_data.return_value = self.d_ret

        d_ret = self.storeObject.do_POST_withCompression(
                    data    = self.data,
                    length  = self.length,
                    form    = 'some form',
                    d_form  = self.d_form)

        assert mock_store_data.call_count == 1

        self.assertIsInstance(d_ret, dict)

    @patch('mount_dir.MountDir.getSize')
    @patch('mount_dir.zip_process')
    @patch('os.remove')
    @patch('builtins.open', mock.mock_open(read_data='****************test******************'))
    def test_mount_dir_store_data(self, mock_remove, mock_zip_process, mock_size):
    
        mock_zip_process.return_value = {
            'msg':              'zip operation successful' ,
            'fileProcessed':    self.filename,
            'status':           True,
            'path':             'Some path',
            'zipmode':          'some mode',
            'filesize':         100,
            'timestamp':        'Some datetime'
        }

        mock_remove.return_value = None
        mock_size.return_value   = 100000


        d_ret = self.storeObject.storeData(file_name= self.filename, 
                              file_content= self.filecontent, Path= self.Path, is_zip= True,d_ret= self.d_ret)

        assert mock_size.call_count == 1
        self.assertIsInstance(d_ret, dict)
 

    @patch('swift_store.SwiftStore.zipUpContent')
    @patch('swift_store.SwiftStore._initiateSwiftConnection')
    @patch('swift_store.SwiftStore._putObject')
    @patch('swift_store.SwiftStore._putContainer')
    def test_swift_store_store_data(self, mock_putContainer, mock_putObject, mock_SwiftConnectionInitialization, mock_zipUp):
    
        self.storeObject = swift_store.SwiftStore(test=True)

        d_ret = self.storeObject.storeData(file_name= self.filename, 
                              file_content= self.filecontent, Path= self.Path, is_zip= True,d_ret= self.d_ret)

        assert mock_SwiftConnectionInitialization.call_count == 1
        
        self.assertIsInstance(d_ret, dict)


class TestFilesPull(TestCase):
    """
    Tests the file pull operation and internally mountdir and swift functionality
    """

    def setUp(self):
        #Create the json message
        
        #PullPath request 
        self.d_server = '{  "action": "pullPath", \
                                "meta": { \
                                    "remote": { \
                                        "key":         "121215" \
                                    }, \
                                    "local": { \
                                        "path":         "/tmp/localstore" \
                                    }, \
                                    "transport": { \
                                        "mechanism":    "compress", \
                                        "compress": { \
                                            "archive":  "zip", \
                                            "unpack":   true, \
                                            "cleanup":  true \
                                        } \
                                    } \
                                } \
                            }'

        self.storeObject = mount_dir.MountDir(test=True)

        self.Path = '/tmp/share/key-121215'
        self.storeObject.path=  'some path'

        self.d_ret = {'some': 'dictionary'}

    @patch('pfioh.StoreHandler.do_GET_remoteStatus')
    @patch('pfioh.StoreHandler.do_GET_withCompression')
    @patch('pfioh.StoreHandler.do_GET_withCopy')
    @patch('urllib.parse.parse_qsl')
    def test_doGet(self, mock_urllib, mock_getCopy, mock_getCompress, mock_getRemoteStatus):
        
        mock_urllib.return_value = {'action': 'pullPath', 'meta': "{'local': {'path': '/tmp/localstore'}, 'transport': {'compress': {'unpack': True, 'cleanup': True, 'archive': 'zip'}, 'mechanism': 'compress'}, 'remote': {'key': '121215'}}"}
        d_ret = self.storeObject.do_GET()
        assert mock_getCopy.call_count == 0
        assert mock_getCompress.call_count == 1
    

    @patch('pfioh.StoreHandler.remoteLocation_resolve')
    @patch('mount_dir.MountDir.getData')
    @patch('os.path.isdir')
    @patch('pfioh.StoreHandler.ret_client')
    def test_doGetwithCompression(self, mock_retClient, mock_osPathIsDir, mock_get_data, mock_remoteLocation_resolve):
        
        mock_remoteLocation_resolve.return_value = {'path': '/tmp/share/key-121215'}
        mock_osPathIsDir.return_value = True
        mock_get_data.return_value = self.d_ret
        mock_retClient.return_value = None

        d_ret = self.storeObject.do_GET_withCompression(
                        {'action': 'pullPath',
                         'meta'  : {"remote":{ "key":"121215"},"local":{"path":"/tmp/localstore"},"transport":{"mechanism":"compress","compress":{"archive":"zip","unpack":True,"cleanup":True}}}})
        
        assert mock_get_data.call_count == 1

        self.assertIsInstance(d_ret, dict)

    @patch('mount_dir.zip_process')
    @patch('pfioh.StoreHandler.ret_client')
    @patch('mount_dir.MountDir.readData')
    @patch('mount_dir.MountDir.getSize')
    @patch('os.remove')
    @patch('os.path.isfile')
    def test_mount_dir_get_data(self, mock_isFile, mock_remove, mock_size, mock_read, mock_retClient, mock_zip_process):
    
        mock_zip_process.return_value = {      
            'msg':              'zip operation successful' ,
            'fileProcessed':    'Some filename',    
            'status':           True,
            'path':             'Some path',
            'zipmode':          'some mode',
            'filesize':         100,
            'timestamp':        'Some datetime'
        }
        
        mock_size.return_value = 1660
        mock_read.return_value = self.d_ret
        mock_retClient.return_value = None
        

        d_ret = self.storeObject.getData(path= self.Path, is_zip= True, 
                                encoding= True, cleanup= True, d_ret= self.d_ret)

        self.assertIsInstance(d_ret, dict)
    
    @patch('swift_store.SwiftStore._initiateSwiftConnection')
    @patch('swift_store.SwiftStore._getObject')
    @patch('swift_store.SwiftStore.writeData')
    def test_swift_store_get_data(self, mock_wfileObject, mock_getObject , mock_SwiftConnectionInitialization):
    
        self.storeObject = swift_store.SwiftStore(test=True)

        mock_getObject.return_value = ({'content-length': '311', 'server': 'Apache/2.4.6 (Red Hat Enterprise Linux) OpenSSL/1.0.2k-fips mod_fcgid/2.3.9', 'date': 'Wed, 15 Nov 2017 18:51:06 GMT', 'content-type': 'text/plain; charset=UTF-8', 'accept-ranges': 'bytes', 'etag': '1aafc94c2a0b8c01ac60435ccc74a8fd', 'x-trans-id': 'tx000000000000000002041-005a0c8c9a-c15974-default', 'x-timestamp': '1510768953.10244', 'last-modified': 'Wed, 15 Nov 2017 18:02:33 GMT'}, b'PK\x03\x04\x14\x00\x00\x00\x08\x00\xcam\x11K\x9e\x99\x11\xbc\x07\x00\x00\x00\x05\x00\x00\x00\x05\x00\x00\x002.txt\xcb\xccS0\xe2\x02\x00PK\x03\x04\x14\x00\x00\x00\x08\x00\xc2m\x11K]\xca<\x97\x07\x00\x00\x00\x05\x00\x00\x00\x05\x00\x00\x001.txt\xcb\xccS0\xe4\x02\x00PK\x03\x04\x14\x00\x00\x00\x08\x00\xcfm\x11K\xdf\xa8\n\xa5\x07\x00\x00\x00\x05\x00\x00\x00\n\x00\x00\x00data/3.txt\xcb\xccS0\xe6\x02\x00PK\x01\x02\x14\x03\x14\x00\x00\x00\x08\x00\xcam\x11K\x9e\x99\x11\xbc\x07\x00\x00\x00\x05\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x81\x00\x00\x00\x002.txtPK\x01\x02\x14\x03\x14\x00\x00\x00\x08\x00\xc2m\x11K]\xca<\x97\x07\x00\x00\x00\x05\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x81*\x00\x00\x001.txtPK\x01\x02\x14\x03\x14\x00\x00\x00\x08\x00\xcfm\x11K\xdf\xa8\n\xa5\x07\x00\x00\x00\x05\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x81T\x00\x00\x00data/3.txtPK\x05\x06\x00\x00\x00\x00\x03\x00\x03\x00\x9e\x00\x00\x00\x83\x00\x00\x00\x00\x00')
        
        d_ret = self.storeObject.getData(file_name= '121215', path= self.Path, is_zip= True, 
                                encoding= True, cleanup= True, d_ret= self.d_ret)

        assert mock_SwiftConnectionInitialization.call_count == 1
        
        self.assertIsInstance(d_ret, dict)
 

suite = unittest.TestLoader().loadTestsFromTestCase(TestFilesPush)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(TestFilesPull)
unittest.TextTestRunner(verbosity=2).run(suite)
