import os
import json

try:
    from gams import *
except ImportError:
    raise ImportError('GAMS python api is not currently installed... must be manually installed.')

# static variable types from gams api reference
# https://www.gams.com/latest/docs/apis/python/classgams_1_1workspace_1_1VarType.html
variable_types = {0: 'Unknown variable type',
                  1: 'Binary variable',
                  2: 'Integer Variable',
                  3: 'Positive variable',
                  4: 'Negative variable',
                  5: 'Free variable',
                  6: 'Special Ordered Set 1',
                  7: 'Special Ordered Set 2',
                  8: 'Semi-continuous variable',
                  9: 'Semi-integer variable'}


def stringify(h):
    if type(h) == str:
        return h

    if type(h) == int:
        return str(h)

    if type(h) == float:
        return str(h)

    if type(h) == list:
        for i in range(len(h)):
            if type(h[i]) == list:
                h[i] = [str(j) for j in h[i]]
            elif type(h[i]) == tuple:
                h[i] = tuple(str(j) for j in h[i])
            elif type(h[i]) == int:
                h[i] = str(h[i])
            elif type(h[i]) == float:
                h[i] = str(h[i])
            elif type(h[i]) == str:
                continue
            else:
                raise Exception(
                    'gams domain contains an illegal type... must be list, tuple, int, or float')
        return h

    if type(h) == tuple:
        return tuple(str(j) for j in h)


# users should be able to add data to the bucket from an existing GDX file, read that data, and add new data all before exporting the DataBucket to a brand new GDX file
class DataBucket:
    def __init__(self):
        self.__db__ = GamsWorkspace()

    def add_from_gdx(gdxfilename=None):
        if gdxfilename != None:
            if gdxfilename[-3:] != 'gdx':
                raise Exception('check filename extension, must be gdx')

        else:
            if os.path.isabs(gdxfilename) == False:
                if gdxfilename[0] == '~':
                    gdxfilename = os.path.expanduser(gdxfilename)
                else:
                    gdxfilename = os.path.abspath(gdxfilename)

        try:
            ws = GamsWorkspace()
            self.gdxfilename = gdxfilename
            self.__db__ = ws.add_database(gdxfilename)
        except:
            raise Exception(
                'attempted to access {} and failed -- check path name'.format(gdxfilename))


class gdxReader:
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
        self.symbols = []
        for i in self.__db__:
            self.symbols.append(i.name)

        # get symbol types
        self.symbolType = {}
        for i in self.symbols:
            self.symbolType[i] = str(type(self.__db__[i])).split("'")[1].split('.')[-1]

        # get symbol dimension
        self.symbolDimension = {}
        for i in self.symbols:
            self.symbolDimension[i] = self.__db__[i].dimension

    def rgdx(self, **kwargs):
        name = kwargs.get('name', None)

        if name is None:
            t = self.symbols
        elif isinstance(name, str):
            t = [name]
        elif isinstance(name, list):
            t = name
        else:
            raise Exception('name must be either type list or str')

        for i in t:
            if i not in self.symbols:
                raise Exception('"{}" is not in the GDX file, check spelling?'.format(i))

        self.__query__ = {}
        for i in t:
            self.__query__[i] = {}
            if self.symbolType[i] == 'GamsSet':
                if self.symbolDimension[i] == 1:
                    self.__query__[i]['type'] = self.symbolType[i]
                    self.__query__[i]['dimension'] = self.symbolDimension[i]
                    self.__query__[i]['domain'] = self.__db__[i].domains_as_strings
                    self.__query__[i]['number_records'] = self.__db__[i].number_records
                    self.__query__[i]['text'] = self.__db__[i].text
                    self.__query__[i]['elements'] = [rec.keys[0] for rec in self.__db__[i]]

                else:
                    self.__query__[i]['type'] = self.symbolType[i]
                    self.__query__[i]['dimension'] = self.symbolDimension[i]
                    self.__query__[i]['domain'] = self.__db__[i].domains_as_strings
                    self.__query__[i]['number_records'] = self.__db__[i].number_records
                    self.__query__[i]['text'] = self.__db__[i].text
                    self.__query__[i]['elements'] = [tuple(rec.keys) for rec in self.__db__[i]]

            elif self.symbolType[i] == 'GamsParameter':
                if self.symbolDimension[i] == 0:
                    self.__query__[i]['type'] = self.symbolType[i]
                    self.__query__[i]['dimension'] = self.symbolDimension[i]
                    self.__query__[i]['domain'] = self.__db__[i].domains_as_strings
                    self.__query__[i]['number_records'] = self.__db__[i].number_records
                    self.__query__[i]['text'] = self.__db__[i].text
                    self.__query__[i]['values'] = self.__db__[i].first_record().value

                elif self.symbolDimension[i] == 1:
                    self.__query__[i]['type'] = self.symbolType[i]
                    self.__query__[i]['dimension'] = self.symbolDimension[i]
                    self.__query__[i]['domain'] = self.__db__[i].domains_as_strings
                    self.__query__[i]['number_records'] = self.__db__[i].number_records
                    self.__query__[i]['text'] = self.__db__[i].text

                    self.__query__[i]['values'] = {rec.keys[0]: rec.value for rec in self.__db__[i]}

                else:
                    self.__query__[i]['type'] = self.symbolType[i]
                    self.__query__[i]['dimension'] = self.symbolDimension[i]
                    self.__query__[i]['domain'] = self.__db__[i].domains_as_strings
                    self.__query__[i]['number_records'] = self.__db__[i].number_records
                    self.__query__[i]['text'] = self.__db__[i].text

                    self.__query__[i]['values'] = {
                        tuple(rec.keys): rec.value for rec in self.__db__[i]}

            elif self.symbolType[i] == 'GamsVariable':
                if self.symbolDimension[i] == 0:
                    self.__query__[i]['type'] = self.symbolType[i]
                    self.__query__[i]['dimension'] = self.symbolDimension[i]
                    self.__query__[i]['domain'] = self.__db__[i].domains_as_strings
                    self.__query__[i]['number_records'] = self.__db__[i].number_records
                    self.__query__[i]['text'] = self.__db__[i].text
                    self.__query__[i]['vartype'] = variable_types[self.__db__[i].vartype]

                    self.__query__[i]['values'] = {'lower': self.__db__[i].first_record().lower,
                                                   'level': self.__db__[i].first_record().level,
                                                   'upper': self.__db__[i].first_record().upper,
                                                   'scale': self.__db__[i].first_record().scale,
                                                   'marginal': self.__db__[i].first_record().marginal}

                elif self.symbolDimension[i] == 1:
                    self.__query__[i]['type'] = self.symbolType[i]
                    self.__query__[i]['dimension'] = self.symbolDimension[i]
                    self.__query__[i]['domain'] = self.__db__[i].domains_as_strings
                    self.__query__[i]['number_records'] = self.__db__[i].number_records
                    self.__query__[i]['text'] = self.__db__[i].text
                    self.__query__[i]['vartype'] = variable_types[self.__db__[i].vartype]

                    self.__query__[i]['values'] = {rec.keys[0]: {'lower': rec.lower,
                                                                 'level': rec.level,
                                                                 'upper': rec.upper,
                                                                 'scale': rec.scale,
                                                                 'marginal': rec.marginal} for rec in self.__db__[i]}

                else:
                    self.__query__[i]['type'] = self.symbolType[i]
                    self.__query__[i]['dimension'] = self.symbolDimension[i]
                    self.__query__[i]['domain'] = self.__db__[i].domains_as_strings
                    self.__query__[i]['number_records'] = self.__db__[i].number_records
                    self.__query__[i]['text'] = self.__db__[i].text
                    self.__query__[i]['vartype'] = variable_types[self.__db__[i].vartype]

                    self.__query__[i]['values'] = {tuple(rec.keys): {'lower': rec.lower,
                                                                     'level': rec.level,
                                                                     'upper': rec.upper,
                                                                     'scale': rec.scale,
                                                                     'marginal': rec.marginal} for rec in self.__db__[i]}

            elif self.symbolType[i] == 'GamsEquation':
                if self.symbolDimension[i] == 0:
                    self.__query__[i]['type'] = self.symbolType[i]
                    self.__query__[i]['dimension'] = self.symbolDimension[i]
                    self.__query__[i]['domain'] = self.__db__[i].domains_as_strings
                    self.__query__[i]['number_records'] = self.__db__[i].number_records
                    self.__query__[i]['text'] = self.__db__[i].text

                    self.__query__[i]['values'] = {'lower': self.__db__[i].first_record().lower,
                                                   'level': self.__db__[i].first_record().level,
                                                   'upper': self.__db__[i].first_record().upper,
                                                   'scale': self.__db__[i].first_record().scale,
                                                   'marginal': self.__db__[i].first_record().marginal}

                elif self.symbolDimension[i] == 1:
                    self.__query__[i]['type'] = self.symbolType[i]
                    self.__query__[i]['dimension'] = self.symbolDimension[i]
                    self.__query__[i]['domain'] = self.__db__[i].domains_as_strings
                    self.__query__[i]['number_records'] = self.__db__[i].number_records
                    self.__query__[i]['text'] = self.__db__[i].text

                    self.__query__[i]['values'] = {rec.keys[0]: {'lower': rec.lower,
                                                                 'level': rec.level,
                                                                 'upper': rec.upper,
                                                                 'scale': rec.scale,
                                                                 'marginal': rec.marginal} for rec in self.__db__[i]}

                else:
                    self.__query__[i]['type'] = self.symbolType[i]
                    self.__query__[i]['dimension'] = self.symbolDimension[i]
                    self.__query__[i]['domain'] = self.__db__[i].domains_as_strings
                    self.__query__[i]['number_records'] = self.__db__[i].number_records
                    self.__query__[i]['text'] = self.__db__[i].text

                    self.__query__[i]['values'] = {tuple(rec.keys): {'lower': rec.lower,
                                                                     'level': rec.level,
                                                                     'upper': rec.upper,
                                                                     'scale': rec.scale,
                                                                     'marginal': rec.marginal} for rec in self.__db__[i]}

        if len(t) == 1:
            return self.__query__[t[0]]
        else:
            return self.__query__
