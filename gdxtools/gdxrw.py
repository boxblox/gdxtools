import os

try:
    from gams import *
except ImportError:
    raise ImportError('GAMS python api is not currently installed... must be manually installed.')


class gdx_reader:
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
            self.db = ws.add_database_from_gdx(gdxfilename)
        except:
            raise Exception(
                'attempted to access {} and failed -- check path name'.format(gdxfilename))

    def getSymbols(self):
        symbols = []
        for i in self.db:
            symbols.append(i.name)
        return symbols

    def getSymbolTypes(self, **kwargs):
        name = kwargs.get('name', None)

        if name is None:
            t = self.getSymbols()
        else:
            if type(name) == str:
                t = [name]
            elif type(name) == list:
                t = name
            else:
                raise Exception('kwarg must be of type str or list')

        types = {}
        for i in t:
            types[i] = str(type(self.db[i])).split("'")[1].split('.')[-1]
        return types

    def rgdx(self, **kwargs):
        name = kwargs.get('name', None)

        if name is None:
            t = self.getSymbolTypes()
        else:
            if type(name) == str:
                t = self.getSymbolTypes(name=[name])
            elif type(name) == list:
                t = self.getSymbolTypes(name=name)
            else:
                raise Exception('kwarg must be of type str or list')

        d = {}
        for i in t.keys():
            d[i] = {}
            if t[i] == 'GamsSet':
                if self.db[i].dimension == 1:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text
                    d[i]['elements'] = [rec.keys[0] for rec in self.db[i]]

                else:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text
                    d[i]['elements'] = [tuple(rec.keys) for rec in self.db[i]]

            elif t[i] == 'GamsParameter':
                if self.db[i].dimension == 0:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text
                    d[i]['values'] = self.db[i].first_record().value

                elif self.db[i].dimension == 1:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text

                    d[i]['values'] = {}
                    d[i]['values']['domain'] = [rec.keys[0] for rec in self.db[i]]
                    d[i]['values']['data'] = [rec.value for rec in self.db[i]]

                else:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text

                    d[i]['values'] = {}
                    d[i]['values']['domain'] = [tuple(rec.keys) for rec in self.db[i]]
                    d[i]['values']['data'] = [rec.value for rec in self.db[i]]

            elif t[i] == 'GamsVariable':
                if self.db[i].dimension == 0:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text
                    d[i]['vartype'] = self.db[i].vartype

                    d[i]['values'] = {}
                    d[i]['values']['domain'] = []
                    d[i]['values']['lower'] = self.db[i].first_record().lower
                    d[i]['values']['level'] = self.db[i].first_record().level
                    d[i]['values']['upper'] = self.db[i].first_record().upper
                    d[i]['values']['scale'] = self.db[i].first_record().scale
                    d[i]['values']['marginal'] = self.db[i].first_record().marginal

                elif self.db[i].dimension == 1:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text
                    d[i]['vartype'] = self.db[i].vartype

                    d[i]['values'] = {}
                    d[i]['values']['domain'] = [rec.keys[0] for rec in self.db[i]]
                    d[i]['values']['lower'] = [rec.lower for rec in self.db[i]]
                    d[i]['values']['level'] = [rec.level for rec in self.db[i]]
                    d[i]['values']['upper'] = [rec.upper for rec in self.db[i]]
                    d[i]['values']['scale'] = [rec.scale for rec in self.db[i]]
                    d[i]['values']['marginal'] = [rec.marginal for rec in self.db[i]]

                else:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text
                    d[i]['vartype'] = self.db[i].vartype

                    d[i]['values'] = {}
                    d[i]['values']['domain'] = [tuple(rec.keys) for rec in self.db[i]]
                    d[i]['values']['lower'] = [rec.lower for rec in self.db[i]]
                    d[i]['values']['level'] = [rec.level for rec in self.db[i]]
                    d[i]['values']['upper'] = [rec.upper for rec in self.db[i]]
                    d[i]['values']['scale'] = [rec.scale for rec in self.db[i]]
                    d[i]['values']['marginal'] = [rec.marginal for rec in self.db[i]]

            elif t[i] == 'GamsEquation':
                if self.db[i].dimension == 0:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text

                    d[i]['values'] = {}
                    d[i]['values']['domain'] = []
                    d[i]['values']['lower'] = self.db[i].first_record().lower
                    d[i]['values']['level'] = self.db[i].first_record().level
                    d[i]['values']['upper'] = self.db[i].first_record().upper
                    d[i]['values']['scale'] = self.db[i].first_record().scale
                    d[i]['values']['marginal'] = self.db[i].first_record().marginal

                elif self.db[i].dimension == 1:
                    d[i]['type'] = t[i]
                    d[i]['dimension'] = self.db[i].dimension
                    d[i]['domain'] = self.db[i].domains_as_strings
                    d[i]['number_records'] = self.db[i].number_records
                    d[i]['text'] = self.db[i].text

                    d[i]['values'] = {}
                    d[i]['values']['domain'] = [rec.keys[0] for rec in self.db[i]]
                    d[i]['values']['lower'] = [rec.lower for rec in self.db[i]]
                    d[i]['values']['level'] = [rec.level for rec in self.db[i]]
                    d[i]['values']['upper'] = [rec.upper for rec in self.db[i]]
                    d[i]['values']['scale'] = [rec.scale for rec in self.db[i]]
                    d[i]['values']['marginal'] = [rec.marginal for rec in self.db[i]]

        if len(t) == 1:
            return d[list(t.keys())[0]]
        else:
            return d


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


class gdx_writer:
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
            self.db = ws.add_database(gdxfilename)
        except:
            raise Exception(
                'attempted to access {} and failed -- check path name'.format(gdxfilename))

    def add_set_dc(self, **kwargs):
        gamssetname = kwargs.get('gamssetname', None)
        domain = kwargs.get('domain', None)
        toset = kwargs.get('toset', None)
        desc = kwargs.get('desc', None)

        i = self.db.add_set_dc(gamssetname, domain, desc)
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

        i = self.db.add_set(gamssetname, dimension, desc)
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

        i = self.db.add_parameter(gamsparametername, dimension, desc)
        for k, v in iter(toparameter.items()):
            i.add_record(stringify(k)).value = v

    def add_parameter_dc(self, **kwargs):
        gamsparametername = kwargs.get('gamsparametername', None)
        domain = kwargs.get('domain', None)
        toparameter = kwargs.get('toparameter', None)
        desc = kwargs.get('desc', None)

        i = self.db.add_parameter_dc(gamsparametername, domain, desc)
        for k, v in iter(toparameter.items()):
            i.add_record(stringify(k)).value = v

    def add_scalar(self, **kwargs):
        gamsparametername = kwargs.get('gamsparametername', None)
        toparameter = kwargs.get('toparameter', None)
        desc = kwargs.get('desc', None)

        i = self.db.add_parameter(gamsparametername, 0, desc)
        i.add_record().value = toparameter

    def export_gdx(self):
        self.db.export(self.gdxfilename)
