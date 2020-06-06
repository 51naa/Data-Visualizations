import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import calendar

#loading up the temperature dataset
data = pd.read_csv('temperature.csv')

#separating minimum temperatures
datamin= data[data['Element']=='TMIN']
datamin.set_index('Date', inplace=True)
datamin.index = map(pd.to_datetime, datamin.index)

#separating 2015 data from the rest
datamin15 = datamin[datamin.index>='2015-01-01']
datamin = datamin[datamin.index<'2015-01-01']

#getting rid of the year
datamin.index = datamin.index.strftime('%m-%d')
datamin15.index = datamin15.index.strftime('%m-%d')

#calculating the minimum temperature
datamin = datamin.groupby(level=0)['Data_Value'].min()/10
datamin15 = datamin15.groupby(level=0)['Data_Value'].min()/10

#getting rid of February 29th which is absent in 2015
datamin.drop('02-29', inplace=True)

#keeping only those of 2015 that are lower than the lowest of previous years
datamin15 = datamin15[datamin15<datamin]

#doing the same for maximums
datamax= data[data['Element']=='TMAX']
datamax.set_index('Date', inplace=True)
datamax.index = map(pd.to_datetime, datamax.index)
datamax15 = datamax[datamax.index>='2015-01-01']
datamax = datamax[datamax.index<'2015-01-01']
datamax.index = datamax.index.strftime('%m-%d')
datamax15.index = datamax15.index.strftime('%m-%d')
datamax = datamax.groupby(level=0)['Data_Value'].max()/10
datamax15 = datamax15.groupby(level=0)['Data_Value'].max()/10
datamax.drop('02-29', inplace=True)
datamax15 = datamax15[datamax15>datamax]

#plotting
plt.rcParams["figure.figsize"] = (20,20)
plt.rcParams.update({'font.size': 22})
plt.plot(datamax, label='Max 2005-2014')
plt.plot(datamin, label='Min 2005-2014')
plt.gca().fill_between(range(365), 
                       datamax, datamin, 
                       facecolor='blue', 
                       alpha=0.25)
plt.scatter(datamax15.index, datamax15, c ='red', marker="v", label='Record High 2015')
plt.scatter(datamin15.index, datamin15, c ='blue', marker="^", label='Record Low 2015')
plt.xticks(np.arange(15, 351, 30), calendar.month_name[1:13])
plt.ylabel('Temperature ($^\circ$C)')
plt.title('Temperature Extermum Records For Each Month Of The Year (2005-2015)')
plt.legend(loc=4, title='Legend')
x = plt.gca().xaxis

# rotating the tick labels for the x axis
for item in x.get_ticklabels():
    item.set_rotation(45)
plt.show()
