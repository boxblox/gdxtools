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

        for i in name:
            if i not in self.symbols:
                raise Exception('"{}" is not in the GDX file, check spelling?'.format(i))

        if name is None:
            t = self.symbols
        elif isinstance(name, str):
            t = [name]
        elif isinstance(name, list):
            t = name
        else:
            raise Exception('name must be either type list or str')

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
        return self.__query__


class gdxWriter:
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
            self.__db__ = ws.add_database(gdxfilename)
        except:
            raise Exception(
                'attempted to access {} and failed -- check path name'.format(gdxfilename))

    def add_set_dc(self, **kwargs):
        gamssetname = kwargs.get('gamssetname', None)
        domain = kwargs.get('domain', None)
        toset = kwargs.get('toset', None)
        desc = kwargs.get('desc', None)

        i = self.__db__.add_set_dc(gamssetname, domain, desc)
        for p in toset:
            i.add_record(stringify(p))

    def add_set(self, **kwargs):
        gamssetname = kwargs.get('gamssetname', None)
        toset = kwargs.get('toset', None)
        desc = kwargs.get('desc', None)

        if type(toset) == list:
            if type(toset[0]) == tuple:
                dimension = len(toset[0])
            elif type(toset[0]) != tuple:
                dimension = 1
        else:
            raise Exception('Set being added must be type list')

        i = self.__db__.add_set(gamssetname, dimension, desc)
        for p in toset:
            i.add_record(stringify(p))

    def add_parameter(self, **kwargs):
        gamsparametername = kwargs.get('gamsparametername', None)
        toparameter = kwargs.get('toparameter', None)
        desc = kwargs.get('desc', None)

        if type(list(toparameter.keys())[0]) != tuple:
            dimension = 1
        else:
            dimension = len(list(toparameter.keys())[0])

        i = self.__db__.add_parameter(gamsparametername, dimension, desc)
        for k, v in iter(toparameter.items()):
            i.add_record(stringify(k)).value = v

    def add_parameter_dc(self, **kwargs):
        gamsparametername = kwargs.get('gamsparametername', None)
        domain = kwargs.get('domain', None)
        toparameter = kwargs.get('toparameter', None)
        desc = kwargs.get('desc', None)

        i = self.__db__.add_parameter_dc(gamsparametername, domain, desc)
        for k, v in iter(toparameter.items()):
            i.add_record(stringify(k)).value = v

    def add_scalar(self, **kwargs):
        gamsparametername = kwargs.get('gamsparametername', None)
        toparameter = kwargs.get('toparameter', None)
        desc = kwargs.get('desc', None)

        i = self.__db__.add_parameter(gamsparametername, 0, desc)
        i.add_record().value = toparameter

    def export_gdx(self):
        self.__db__.export(self.gdxfilename)
