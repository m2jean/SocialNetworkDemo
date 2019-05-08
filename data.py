import pandas
from datetime import timedelta

def load_events():
    events = pandas.read_csv('events.csv',names=['dt','curr','desc','imp','a','f','p','key'])
    events['dt'] = pandas.to_datetime(events['dt'],format="%Y-%m-%dT%H:%M:%S").dt.tz_localize('UTC').dt.tz_convert("US/Central").dt.tz_localize(None)
    grouped = events.groupby('key')
    return grouped
    
df = None
sym = None
def load_data(sec,dt,window=60,useDollar=False): # window : one side window size in mins
    global df, sym
    if df is None or sec[0] != sym:
        sym = sec[0]
        df = pandas.read_hdf('ticks30s.h5',sym)
    before = (dt - timedelta(minutes=window)).floor('D')
    after = (dt + timedelta(minutes=window)).ceil('D')
    ret = df[(before <= df.index) & (df.index <= after)].copy()
    if useDollar:
        ret['o'] *= sec[3]
        ret['h'] *= sec[3]
        ret['l'] *= sec[3]
        ret['c'] *= sec[3]
    return ret

securities = (('ES',('es',4,2,50,1)),('TU',('tu',256,8,2000,4)),('UB',('ub',32,5,1000,2)))
events = load_events()