from os.path import join
from os import getcwd
from db import instance
from pathlib import Path

def exportSimpleGraphics():
    from bokeh.plotting import figure
    from bokeh.resources import CDN
    from bokeh.embed import file_html
    from bokeh.models import ColumnDataSource
    from os import getcwd
    from pathlib import Path
    dataframe = instance.all()
    # source = ColumnDataSource(data=dataframe)
    for column in dataframe:
    # for column in source:
        p = figure(width=1600, height=500, x_axis_type="datetime")
        p.line(dataframe['date'], dataframe[column], color='navy', alpha=0.5)
        filepath = Path(getcwd()) / Path("{variable}.html".format(variable=column))
        htmlpath = Path('file://') / filepath
        html = file_html(p,CDN,"{variable}.html".format(variable=column))
        with open(str(htmlpath),'w') as file :
            file.write(html)


def filter(dataframe):
    from pandas.core.window.Rolling import median
    for i in ['temperature','humidity', 'luminosity']:
        dataframe[i] = median(dataframe[i],5)

# exportSimpleGraphics()

def acquire(interval):
    import sensors
    # sensor_bme280 = sensors.bme280()

    sensor_bme280 = sensors.sen0193()

    # import threading
    # threading.Timer(interval, acquire,args=[instance]).start()
    temperature, pressure, humidity = sensor_bme280.read()
    # luminosity = 0 #tsl2561()
    # instance.add(humidity,temperature,luminosity)

print(acquire(1))
