import pandas as pd
import gdtools as gt


if __name__ == '__main__':

    # create instance of gams gdx data
    gdxin = gt.gdxrw.gdx_reader('trnsport_output.gdx')

    # get all symbols inside a GDX
    gdxin.getSymbols()

    # get symbol types from a GDX file
    gdxin.getSymbolTypes()

    # get read in all data from a gdx file (creates a python dictionary)
    all_data = gdxin.rgdx()

    # read in single items
    i = gdxin.rgdx(name='i')
    j = gdxin.rgdx(name='j')

    # read in multiple items
    m = gdxin.rgdx(name=['i', 'j'])

    # read in parameters and turn it into 'c' into a dataframe
    c = gdxin.rgdx(name='c')
    c_df = pd.DataFrame(data=c['values']['domain'], columns=['dim1', 'dim2'])
    c_df['value'] = c['values']['data']

    # read in a variable and turn it into a dataframe
    x = gdxin.rgdx(name='x')
    x_df = pd.DataFrame(data=x['values']['domain'], columns=['dim1', 'dim2'])
    x_df['LO'] = x['values']['lower']
    x_df['L'] = x['values']['level']
    x_df['UP'] = x['values']['upper']
    x_df['scale'] = x['values']['scale']
    x_df['M'] = x['values']['marginal']

    # --------------------------------------------------------------------------
    # Write out another GDX with the similar structure to the original input gdx
    # Does NOT support EQUATIONS or VARIABLES
    # Check can be run with gdxdiff
    # --------------------------------------------------------------------------

    gdxout = gt.gdxrw.gdx_writer('./trnsport_output_chk.gdx')

    # add sets without domain checking (universe domain)
    gdxout.add_set(gamssetname='i', toset=i['elements'], desc=i['text'])
    gdxout.add_set(gamssetname='j', toset=j['elements'], desc=j['text'])

    # there are no subsets in this example, but if you wanted to run domain checking you would use this:
    # gdxout.add_set_dc(gamssetname=, domain=, toset=, desc=)

    # add parameters, but first must zip the data into a dictionary
    a = gdxin.rgdx(name='a')
    a_p = {a: b for a, b in zip(a['values']['domain'], a['values']['data'])}
    gdxout.add_parameter_dc(gamsparametername='a',
                            domain=a['domain'], toparameter=a_p, desc=a['text'])

    b = gdxin.rgdx(name='b')
    b_p = {a: b for a, b in zip(b['values']['domain'], b['values']['data'])}
    gdxout.add_parameter_dc(gamsparametername='b',
                            domain=b['domain'], toparameter=b_p, desc=b['text'])

    d = gdxin.rgdx(name='d')
    d_p = {a: b for a, b in zip(d['values']['domain'], d['values']['data'])}
    gdxout.add_parameter_dc(gamsparametername='d',
                            domain=d['domain'], toparameter=d_p, desc=d['text'])

    f = gdxin.rgdx(name='f')
    gdxout.add_scalar(gamsparametername='f', toparameter=f['values'], desc=f['text'])

    c = gdxin.rgdx(name='c')
    c_p = {a: b for a, b in zip(c['values']['domain'], c['values']['data'])}
    gdxout.add_parameter_dc(gamsparametername='c',
                            domain=c['domain'], toparameter=c_p, desc=c['text'])

    gdxout.export_gdx()
