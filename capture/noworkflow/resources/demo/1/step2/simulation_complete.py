import csv
import time
import tempfile
import os
#this code requires matplotlib to be installed
#please refer to http://matplotlib.org/downloads.html
import matplotlib.pyplot as plt

class TabularData:
    def __init__(self, data, header=None):
        self.data = data
        self.header = header

###############################################################

def simulation(dataA, dataB):
    time.sleep(0.2)

    all_data = dataA.data + dataB.data

    (f, name) = tempfile.mkstemp(prefix='vtweather')
    os.close(f)

    writer = csv.writer(open(name, 'w'), delimiter=':')
    writer.writerows(all_data)

    #res = registry.get_descriptor_by_name('edu.utah.sci.vistrails.basic',
    #    'File').module()
    #res.name = name
    return name


def csvRead(f):
    reader = csv.reader(open(f, 'rU'), delimiter=':')
    header = []
    data = []
    for row in reader:
        data.append(row)
    tab_data = TabularData(data, header)
    #self.setResult('data', tab_data)
    return tab_data

def extractColumn(d, column_name, column):
        data = d.data
        header = d.header

        #Test to check whether column_name is not empty
        if column_name:
            if header is None:
                print("Data does not contain header")
            #column_name = self.getInputFromPort('columnName')
            try:
                idx = header.index(column_name)
            except ValueError:
                print("Data does not contain column" + column)
        else:
                idx = column

        col_data = []
        for row in data:
            print('processing row', row)
            col_data.append(row[idx])
        return col_data

def mplScatter(x,y):
    kwargs = {}
    #kwargs['y'] = y
    #kwargs['x'] = x
    plt.scatter(x, y, s=20, c='b', marker='o', cmap=None, norm=None,
                    vmin=None, vmax=None, alpha=None, linewidths=None, verts=None, **kwargs)
    plt.xlabel('Temperature')
    plt.ylabel('Precipitation')
    plt.savefig("output.png")

######################################################################################
#Main Program
print('Reading data data1.dat...')
dataA = csvRead('data1.dat')
print('Reading data data2.dat...')
dataB = csvRead('data2.dat')
#Simulation
print('Executing simulation...')
tempFile = simulation(dataA, dataB)
#tempFile was generated by Simulation
print('Reading temporary file...')
d = csvRead(tempFile)
#GetPrecipitation
print('Extracting precipitation...')
columnY = extractColumn(d, '', 1)
#GetTemperature
print('Extracting temperature...')
columnX = extractColumn(d, '', 0)
#Transform column values in a list of float
print('Converting values...')
out1 = [float(i) for i in columnX]
out2 = [float(i) for i in columnY]
print('Generating result...')
mplScatter(out1, out2)


