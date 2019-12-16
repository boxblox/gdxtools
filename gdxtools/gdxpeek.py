import os
import json
import gdxrw

try:
    from gams import *
except ImportError:
    raise ImportError('GAMS python api is not currently installed... must be manually installed.')


class gdxInspector:
    def __init__(self, gdxfilename):

        if gdxfilename[-3:] != 'gdx':
            raise Exception('check filename extension, must be gdx')

        if os.path.isabs(gdxfilename) == False:
            if gdxfilename[0] == '~':
                gdxfilename = os.path.expanduser(gdxfilename)
            else:
                gdxfilename = os.path.abspath(gdxfilename)

        try:
            ws = GamsWorkspace()
            self.gdxfilename = gdxfilename
            self.__db__ = ws.add_database_from_gdx(gdxfilename)
        except:
            raise Exception(
                'attempted to access {} and failed -- check path name'.format(gdxfilename))

        # get symbols
        gdxin = gdxrw.gdxReader(self.gdxfilename)
        self.symbols = gdxin.symbols

        # get symbols
        gdxin = gdxrw.gdxReader(self.gdxfilename)
        self.symbols = gdxin.symbols
