import numpy as np
import pandas as pd

import quandl
import my_key #get your own key!  
quandl.ApiConfig.api_key = my_key.get_key()


def get_historical(ticker):
    #function to grab data from Quandl and convert to dataframe 
    
    data = quandl.get_table('WIKI/PRICES',
                            qopts={'columns': ['date', 'adj_close']},
                            ticker = ticker)
    data.index = data['date']
    #data = data.iloc[:, 1]
    data = pd.DataFrame(data)
    
    if data.iloc[:, 1].values.sum() == 0: #empty
        print ('Error: No Quandl data for %s stock' %ticker)
        return 0
    else: 
        return data


#S&P 500 - scraped from wikipedia -- Separate .py file 
# , 'abbv', 'bf' #stocks w annoying tickers...
sp500 = ['Date', 'mmm', 'abt', 'acn', 'atvi', 'ayi', 'adbe', 'amd', 'aap', 'aes', 'aet', 'amg', 'afl',
         'a', 'apd', 'akam', 'alk', 'alb', 'are', 'agn', 'lnt', 'alxn', 'alle', 'ads', 'all', 'googl',
         'goog', 'mo', 'amzn', 'aee', 'aal', 'aep', 'axp', 'aig', 'amt', 'awk', 'amp', 'abc', 'ame',
         'amgn', 'aph', 'apc', 'adi', 'antm', 'aon', 'apa', 'aiv', 'aapl', 'amat', 'adm', 'arnc', 'ajg',
         'aiz', 't', 'adsk', 'adp', 'an', 'azo', 'avb', 'avy', 'bhi', 'bll', 'bac', 'bk', 'bcr', 'bax',
         'bbt', 'bdx', 'bbby', 'brk', 'bby', 'biib', 'blk', 'hrb', 'ba', 'bwa', 'bxp', 'bsx', 'bmy', 
         'avgo', 'chrw', 'ca', 'cog', 'cpb', 'cof', 'cah', 'cboe', 'kmx', 'ccl', 'cat', 'cbg', 'cbs',
         'celg', 'cnc', 'cnp', 'ctl', 'cern', 'cf', 'schw', 'chtr', 'chk', 'cvx', 'cmg', 'cb', 'chd', 'ci', 
         'xec', 'cinf', 'ctas', 'csco', 'c', 'cfg', 'ctxs', 'clx', 'cme', 'cms', 'coh', 'ko', 'ctsh', 'cl', 
         'cmcsa', 'cma', 'cag', 'cxo', 'cop', 'ed', 'stz', 'glw', 'cost', 'coty', 'cci', 'csra', 'csx', 'cmi',
         'cvs', 'dhi', 'dhr', 'dri', 'dva', 'de', 'dlph', 'dal', 'xray', 'dvn', 'dlr', 'dfs', 'disca', 'disck',
         'dish', 'dg', 'dltr', 'd', 'dov', 'dow', 'dps', 'dte', 'dd', 'duk', 'dnb', 'etfc', 'emn', 'etn', 'ebay',
         'ecl', 'eix', 'ew', 'ea', 'emr', 'etr', 'evhc', 'eog', 'eqt', 'efx', 'eqix', 'eqr', 'ess', 'el', 'es',
         'exc', 'expe', 'expd', 'esrx', 'exr', 'xom', 'ffiv', 'fb', 'fast', 'frt', 'fdx', 'fis', 'fitb', 'fe', 
         'fisv', 'flir', 'fls', 'flr', 'fmc', 'fti', 'fl', 'f', 'ftv', 'fbhs', 'ben', 'fcx', 'gps', 'grmn', 'gd',
         'ge', 'ggp', 'gis', 'gm', 'gpc', 'gild', 'gpn', 'gs', 'gt', 'gww', 'hal', 'hbi', 'hog', 'hrs', 'hig', 'has',
         'hca', 'hcp', 'hp', 'hsic', 'hes', 'hpe', 'holx', 'hd', 'hon', 'hrl', 'hst', 'hpq', 'hum', 'hban', 'idxx',
         'itw', 'ilmn', 'ir', 'intc', 'ice', 'ibm', 'incy', 'ip', 'ipg', 'iff', 'intu', 'isrg', 'ivz', 'irm', 'jec',
         'jbht', 'sjm', 'jnj', 'jci', 'jpm', 'jnpr', 'ksu', 'k', 'key', 'kmb', 'kim', 'kmi', 'klac', 'kss', 'khc', 
         'kr', 'lb', 'lll', 'lh', 'lrcx', 'leg', 'len', 'lvlt', 'luk', 'lly', 'lnc', 'lkq', 'lmt', 'l', 'low', 'lyb',
         'mtb', 'mac', 'm', 'mnk', 'mro', 'mpc', 'mar', 'mmc', 'mlm', 'mas', 'ma', 'mat', 'mkc', 'mcd', 'mck', 
         'mjn', 'mdt', 'mrk', 'met', 'mtd', 'kors', 'mchp', 'mu', 'msft', 'maa', 'mhk', 'tap', 'mdlz', 'mon', 
         'mnst', 'mco', 'ms', 'mos', 'msi', 'mur', 'myl', 'ndaq', 'nov', 'navi', 'ntap', 'nflx', 'nwl', 'nfx', 
         'nem', 'nwsa', 'nws', 'nee', 'nlsn', 'nke', 'ni', 'nbl', 'jwn', 'nsc', 'ntrs', 'noc', 'nrg', 'nue', 
         'nvda', 'orly', 'oxy', 'omc', 'oke', 'orcl', 'pcar', 'ph', 'pdco', 'payx', 'pypl', 'pnr', 'pbct', 'pep', 
         'pki', 'prgo', 'pfe', 'pcg', 'pm', 'psx', 'pnw', 'pxd', 'pnc', 'rl', 'ppg', 'ppl', 'px', 'pcln', 'pfg', 
         'pg', 'pgr', 'pld', 'pru', 'peg', 'psa', 'phm', 'pvh', 'qrvo', 'pwr', 'qcom', 'dgx', 'rrc', 'rjf', 'rtn',
         'o', 'rht', 'reg', 'regn', 'rf', 'rsg', 'rai', 'rhi', 'rok', 'col', 'rop', 'rost', 'rcl', 'r', 'crm', 
         'scg', 'slb', 'sni', 'stx', 'see', 'sre', 'shw', 'sig', 'spg', 'swks', 'slg', 'sna', 'so', 'luv', 'swn', 
         'spgi', 'swk', 'spls', 'sbux', 'stt', 'srcl', 'syk', 'sti', 'symc', 'syf', 'snps', 'syy', 'trow', 'tgt',
         'tel', 'tgna', 'tdc', 'tso', 'txn', 'txt', 'coo', 'hsy', 'trv', 'tmo', 'tif', 'twx', 'tjx', 'tmk', 'tss',
         'tsco', 'tdg', 'rig', 'trip', 'foxa', 'fox', 'tsn', 'udr', 'ulta', 'usb', 'ua', 'uaa', 'unp', 'ual', 'unh',
         'ups', 'uri', 'utx', 'uhs', 'unm', 'vfc', 'vlo', 'var', 'vtr', 'vrsn', 'vrsk', 'vz', 'vrtx', 'viab', 
         'v', 'vno', 'vmc', 'wmt', 'wba', 'dis', 'wm', 'wat', 'wec', 'wfc', 'hcn', 'wdc', 'wu', 'wrk', 'wy', 'whr',
         'wfm', 'wmb', 'wltw', 'wyn', 'wynn', 'xel', 'xrx', 'xlnx', 'xl', 'xyl', 'yhoo', 'yum', 'zbh', 'zion', 'zts']

#sp400
sp400 = ['aos', 'aan', 'abmd', 'acc', 'achc', 'aciw', 'acm', 'acxm', 'aeo', 'afg', 'agco', 'ahl', 'akrx', 'alex',
         'algn', 'y', 'ati', 'amcx', 'anss', 'wtr', 'arw', 'arrs', 'asb', 'ash', 'ato', 'atr', 'car', 'avt', 'avp',
         'bc', 'bdc', 'bid', 'big', 'bio', 'bivv', 'bkh', 'bms', 'boh', 'br', 'brcd', 'bro', 'bwld', 'bxs', 'caa',
         'cab', 'cabo', 'cake', 'casy', 'caty', 'cbsh', 'cbt', 'cc', 'ccp', 'cdk', 'cdns', 'cfr', 'cgnx', 'chdn',
         'chfc', 'chs', 'cien', 'clgx', 'clh', 'cli', 'cmc', 'cmp', 'cnk', 'cno', 'cohr', 'cone', 'cprt', 'cpt', 'cr',
         'cree', 'cri', 'crl', 'crs', 'crus', 'cnx', 'csl', 'cst', 'ctb', 'ctlt', 'cuz', 'cvg', 'cvlt', 'cxw', 'cw',
         'cbrl', 'cy', 'dan', 'dbd', 'dci', 'dct', 'ddd', 'dds', 'deck', 'dei', 'df', 'dks', 'dlx', 'dnb', 'dnkn',
         'dnow', 'do', 'dpz', 'dre', 'drq', 'dst', 'dv', 'dy', 'eat', 'edr', 'egn', 'eme', 'endp', 'enr', 'ens', 'epc',
         'epr', 'esl', 'esv', 'ev', 'ewbc', 'exp', 'faf', 'fcn', 'fds', 'fhn', 'fico', 'fii', 'flo', 'fr', 'fnb',
         'fslr', 'ftnt', 'ftr', 'fult', 'gatx', 'gef', 'geo', 'ggg', 'ghc', 'gme', 'gmed', 'gntx', 'gnw', 'gpor',
         'gva', 'gwr', 'gxp', 'hain', 'hbhc', 'he', 'hele', 'hfc', 'hii', 'hiw', 'hls', 'hni', 'hpt', 'hr', 'hrc',
         'hsni', 'hubb', 'hyh', 'iboc', 'ida', 'idcc', 'idti', 'iex', 'incr', 'ingr', 'int', 'ipgp', 'isca', 'itt',
         'jack', 'jbl', 'jblu', 'jcom', 'jcp', 'jkhy', 'jll', 'jns', 'jw.a', 'kate', 'kbh', 'kbr', 'kex', 'keys',
         'klxi', 'kmpr', 'kmt', 'kn', 'krc', 'lamr', 'lanc', 'ldos', 'leco', 'lfus', 'lho', 'lii', 'livn', 'lm', 
         'lnce', 'logm', 'lpnt', 'lpt', 'lpx', 'lsi', 'lstr', 'lw', 'lyv', 'man', 'manh', 'masi', 'mbfi', 'mcy',
         'md', 'mdp', 'mdrx', 'mdu', 'mik', 'mktx', 'mlhr', 'mms', 'moh', 'mpw', 'mpwr', 'msa', 'mscc', 'msci',
         'msm', 'mtx', 'musa', 'nati', 'nbr', 'ncr', 'ndsn', 'ne', 'neu', 'nfg', 'njr', 'nnn', 'nsr', 'ntct', 'nus',
         'nuva', 'nvr', 'nwe', 'nycb', 'nyt', 'oa', 'odfl', 'odp', 'ofc', 'oge', 'ogs', 'ohi', 'oii', 'ois', 'oln',
         'oi', 'omi', 'ori', 'osk', 'ozrk', 'pacw', 'pbf', 'pay', 'pb', 'pbh', 'pbi', 'pch', 'pii', 'pkg', 'plt',
         'pnm', 'pnra', 'pol', 'pool', 'post', 'pri', 'prxl', 'ptc', 'pten', 'pvtb', 'pzza', 'qcp', 'qep', 'rbc',
         'rdc', 're', 'rga', 'rgld', 'rmd', 'rnr', 'rol', 'rpm', 'rs', 'ryn', 'sabr', 'saic', 'sam', 'sbh', 'sbny',
         'sci', 'seic', 'sf', 'sfm', 'sivb', 'skt', 'skx', 'slab', 'slgn', 'slm', 'sm', 'smg', 'snh', 'snv', 'snx', 
         'son', 'spn', 'ste', 'stld', 'swn', 'swx', 'sxt', 'syna', 'tcb', 'tcbi', 'tco', 'tds', 'tdy', 'tecd', 'tech',
         'ter', 'tex', 'tfx', 'thc', 'thg', 'tho', 'ths', 'time', 'tkr', 'tol', 'tph', 'tpx', 'tr', 'trmb', 'trmk',
         'trn', 'ttc', 'ttwo', 'tup', 'txrh', 'tyl', 'ubsi', 'ue', 'ufs', 'ugi', 'ulti', 'umbf', 'umpq', 'unfi', 
         'uthr', 'unit', 'urbn', 'vly', 'vmi', 'val', 'woof', 'vvc', 'vsm', 'vsat', 'vsh', 'wrb', 'wab', 'wafd', 
         'wbmd', 'wbs', 'wcg', 'wen', 'wern', 'wex', 'wgl', 'wnr', 'wor', 'wpg', 'wpx', 'wr', 'wri', 'wsm', 'wso',
         'wst', 'wtfc', 'wwd', 'x', 'zbra']



crawl = True #to prevent overwriting data 
if crawl: 
    
    #stocks of interest not in sp500
    #names = ['fb', 'inod']
    names = ['tsla', 'lulu', 'onvo', 'yelp', 'twtr', 'z', 'aapl', 'amrs', 'inod']
    
    names = names+sp500+sp400
    names = list(set(names)) #delete duplicates
    
    print ('initializing...')
    delete_col = 'aapl' #setup df 'Date', pick stock with long history 
    df = get_historical(delete_col)
    df = df.rename(columns={'adj_close': 'delete_me'})

    for i, name in enumerate(names):
        print ("collecting data: ", name )
        share_df = get_historical(name) #pull stock from api 
        if isinstance(share_df, int): #test if API returned data 
            continue 
        share_df = share_df.rename(columns={'adj_close': names[i]})
        df = pd.merge(df, share_df, on='date', how='left')
        
    df = df.drop(['delete_me'], axis=1)
    df.index = df['date']

    df.to_csv('quandl_new.csv') #for safe keeping :) 
    print (df.tail(2) )#spot check 
    print (df.head(2))
    
else: 
    print ('crawling is off')
