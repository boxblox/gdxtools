import pandas as pd
import gdxtools as gt


if __name__ == '__main__':

    # create instance of gams gdx data
    gdxin = gt.gdxrw.gdxReader('trnsport_output.gdx')

    # get all symbols inside a GDX
    gdxin.symbols

    # get symbol types from a GDX file
    gdxin.symbolType

    # get symbol dimensions from a GDX file
    gdxin.symbolDimension

    # read in single items
    i = gdxin.rgdx(name='i')
    j = gdxin.rgdx(name='j')

    # read in multiple items
    m = gdxin.rgdx(name=['i', 'j'])

    # read in parameters and turn it into 'c' into a dataframe
    c = gdxin.rgdx(name='c')

    # create a simple index/value pandas dataframe
    c_df = pd.DataFrame(data=zip(c['values'].keys(),
                                 c['values'].values()), columns=['index', 'value'])

    # might also be helpful to split out the index tuple into different columns
    c_df2 = pd.DataFrame(data=c['values'].keys(), columns=c['domain'])
    c_df2['value'] = c['values'].values()

    # read in a variable and turn it into a dataframe
    x = gdxin.rgdx(name='x')
    x_df = pd.DataFrame(data=x['values'].keys(), columns=c['domain'])
    x_df['LO'] = [x['values'][i]['lower'] for i in x['values'].keys()]
    x_df['L'] = [x['values'][i]['level'] for i in x['values'].keys()]
    x_df['UP'] = [x['values'][i]['upper'] for i in x['values'].keys()]
    x_df['scale'] = [x['values'][i]['scale'] for i in x['values'].keys()]
    x_df['M'] = [x['values'][i]['marginal'] for i in x['values'].keys()]

    # --------------------------------------------------------------------------
    # Write out another GDX with the similar structure to the original input gdx
    # Does NOT support EQUATIONS or VARIABLES
    # Check can be run with gdxdiff
    # --------------------------------------------------------------------------

    gdxout = gt.gdxrw.gdxWriter('./trnsport_output_chk.gdx')

    # add sets without domain checking (universe domain)
    gdxout.add_set(gamssetname='i', toset=i['elements'], desc=i['text'])
    gdxout.add_set(gamssetname='j', toset=j['elements'], desc=j['text'])

    # there are no subsets in this example, but if you wanted to run domain checking you would use this:
    # gdxout.add_set_dc(gamssetname=, domain=, toset=, desc=)

    # add parameters and do the domain checking
    a = gdxin.rgdx(name='a')
    gdxout.add_parameter_dc(gamsparametername='a',
                            domain=a['domain'], toparameter=a['values'], desc=a['text'])

    b = gdxin.rgdx(name='b')
    gdxout.add_parameter_dc(gamsparametername='b',
                            domain=b['domain'], toparameter=b['values'], desc=b['text'])

    d = gdxin.rgdx(name='d')
    gdxout.add_parameter_dc(gamsparametername='d',
                            domain=d['domain'], toparameter=d['values'], desc=d['text'])

    f = gdxin.rgdx(name='f')
    gdxout.add_scalar(gamsparametername='f', toparameter=f['values'], desc=f['text'])

    c = gdxin.rgdx(name='c')
    gdxout.add_parameter_dc(gamsparametername='c',
                            domain=c['domain'], toparameter=c['values'], desc=c['text'])

    gdxout.export_gdx()
