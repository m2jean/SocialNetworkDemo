from plotly.offline import download_plotlyjs,init_notebook_mode, iplot
from plotly.graph_objs import Candlestick

init_notebook_mode(connected=True)

periods = {
'10 minutes': lambda dts: dts.floor('10T'),
'5 minutes': lambda dts: dts.floor('5T'),
'1 minute': lambda dts: dts.floor('1T'),
'30 seconds': lambda dts: dts,
}

def plot(data, event, groupfunc, precision):
    data.index = groupfunc(data.index)
    ohlc = data.groupby(data.index).agg({'o':['first'],'h':['max'],'l':['min'],'c':['last']})
    O,H,L,C = ohlc['o']['first'],ohlc['h']['max'],ohlc['l']['min'],ohlc['c']['last']
    htext = []
    for o,h,l,c in zip(O,H,L,C):
        htext.append("open: {o:.{p}f}<br>high: {h:.{p}f}<br>low: {l:.{p}f}<br>close: {c:.{p}f}".format(
            p=precision,o=o,h=h,l=l,c=c))
    candles = Candlestick(x=ohlc.index,open=O,high=H,low=L,close=C
                          ,whiskerwidth=1,text=htext,hoverinfo='text')
    title = "{}<br>Forecast: {}  Actual: {}  Previous: {}".format(event.desc, event.f, event.a, event.p)
    layout = {
    'title': title,
    'shapes': [{
    'type': 'line', 'x0': event[0], 'y0': 0, 'x1': event[0], 'y1': 1,
    'xref': 'x', 'yref': 'paper', 'line': {'color': 'rgb(0, 0, 255)'}
    }]
    }

    return iplot({'data':[candles],'layout':layout})

class EventObserver:
    def __init__(self, events, evdrop, dtdrop):
        self.events, self.evdrop, self.dtdrop = events, evdrop, dtdrop

    def onSelectEvent(self, *args):
        group = self.events.get_group(self.evdrop.value).set_index('dt')
        dtstrs = group.index.strftime('%b %d %Y, %r')
        self.dtdrop.value = None
        self.dtdrop.options = reversed(list(zip(dtstrs, group.itertuples())))