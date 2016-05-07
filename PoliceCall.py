__author__ = 'Ghiat Mira'

import pandas
import glob
import os
import numpy
import time
import datetime
import math
import sys
from datetime import timedelta
 

# clean data
def clean_data(x):
	y = x[x.PoliceDistrict != 0]
	y = x.fillna(0, axis=1)       # fill with 0 
	return y
# set to_datetime
def f(date):
    date_s = pandas.to_datetime(date, unit = 's')
    return date_s	 
	
# Load the whole data into a one DataFrame
path = r'C:/Users/ROC/documents/challenge data'
files = glob.glob(os.path.join( path, "*.csv"))
data = pandas.concat(pandas.read_csv(f, parse_dates=True, infer_datetime_format = True, index_col = False) for f in files)
data = clean_data(data)
	
# Calculate the fraction of the most common call
bytype = data.groupby(['Type_'])
call_count_bygroup = bytype['NOPD_Item'].count() 
print("Count by call type", "\n",call_count_bygroup, "\n")
fraction_most_common_call = call_count_bygroup.max()
bool= call_count_bygroup==fraction_most_common_call 
Type_most_common_call = call_count_bygroup.index[bool == True]
print("The most common call Fraction: ", "%.10f" %fraction_most_common_call, "\n")
print("Type of most common call: ", Type_most_common_call, "\n")

# Median reponse time  ///no need to groupby
Timearrive = data['TimeArrive']
Timedispatch = data['TimeDispatch']
ResponseTime = pandas.Series(f(Timearrive) - f(Timedispatch), name = 'ResponseTime')
ResponseTime = ResponseTime.fillna(0)
           			
Newdata = pandas.concat([data, ResponseTime], axis = 1) # add a new colunm #ResponseTime to data
median_response_time = ResponseTime.median()
print("Median Response Time is : ", "%.10f" %median_response_time)

# Compute the difference between the average response time (mean) and max and min time  
mean_response_time = ResponseTime.mean().seconds
max_response_time = ResponseTime.max().seconds
min_response_time = ResponseTime.min().seconds 
print("Mean Response time is: ", "%.10f" %mean_response_time,"\n","Distance from max is: ", "%.10f" %(max_response_time - mean_response_time),"\n","Distance from min is: ", "%.10f" %(mean_response_time - min_response_time), "\n",)

# Compute the Largest ratio of a conditional probability of an event given a district to a unconditional probabilty of that event
bydistrict = data.groupby('PoliceDistrict')
nb_call_district = bydistrict['NOPD_Item'].count() 
nb_call_district = nb_call_district[nb_call_district > 100]
nb_call_all_district = nb_call_district.sum()
pratio_bydistrict = nb_call_district/nb_call_all_district
max_ratio = pratio_bydistrict.max()
print("the Largest ratio of a conditional probability:", "%.10f" %max_ratio, "\n",)

# Compute the largest decrease in volume of a call between 2011 and 2015, compute the fraction of 2011 that this decrease represent
# ///largest_decrease11-15/fraction call of 2011
data2011 = pandas.read_csv('C:/Users/ROC/documents/challenge data/Calls_for_Service_2011.csv', parse_dates=True, infer_datetime_format = True, index_col = False)
data2015 = pandas.read_csv('C:/Users/ROC/documents/challenge data/Calls_for_Service_2015.csv', parse_dates=True, infer_datetime_format = True, index_col = False)
data2011 = clean_data(data2011)
data2015 = clean_data(data2015)
bytype11 = data2011.groupby('Type_')
bytype15 = data2015.groupby('Type_')
count11 = bytype11['NOPD_Item'].count()
count15 = bytype15['NOPD_Item'].count()
difference = count11 - count15
calls2011 = count11.sum()
difference = difference[difference > 0]            # decrease 2011 calls > 2015calls
largest_decrease = difference.max()
percentage_decrease = largest_decrease/calls2011
print("the Largest decrease between 11-15:", "%.10f" %largest_decrease, "\n","the decrease represent: ", "%.10f" %percentage_decrease, "of 2011 call fraction", "\n",)

# Compute the largest fraction of disposition change within a hour of creation //maxfraction-minfraction 
timecreate = data['TimeCreate'].apply(f)
starttime = timecreate[0]                   # could be choosen randomly from the time series
data['TimeCreate'] = ((timecreate-starttime) / numpy.timedelta64(1, 'h')).reset_index()                
prev = 0
for i in range(1,25):    # i hour time in 24 hours frame
	Hour_data =data[data['TimeCreate'] <= i ] 
	Hour_data =data[data['TimeCreate'] > prev]
	bydisposition = Hour_data.groupby('Disposition')
	nb_disposition = bydisposition['NOPD_Item'].count()
	max_disp = nb_disposition.max()
	min_disp = nb_disposition.min()
	prev = i
	print('the largest disposition change within the hour', i, "is", "%.10f" %(max_disp - min_disp), "\n")

# Compute the area in square kilometres of the largest district
Xkilom = data['MapX']/1000
Ykilom = data['MapY']/1000
area = Xkilom*Ykilom*math.pi                             #area of an eclipse
largest_distArea = area.max()
print("area in square kilometres of the largest district: ", "%.10f" %largest_distArea, "\n")

# compute the type of call whose most common priority is the smallest fraction of all calls of that type, compute that fraction
data = data[data['Type_'] == Type_most_common_call.any()]   # Type_most_common_call already computed in the first section
bypriority = data.groupby('Priority') 
priority_count = bypriority['NOPD_Item'].count()
print("Priority Fraction count of the of the most common call",priority_count, "\n") 
least_priority_fraction = priority_count.min()
bool= priority_count==least_priority_fraction 
calltype_leastprio = priority_count.index[bool == True]

print("Smallest Fraction of the of the most common call priority: ", "%.10f" %least_priority_fraction, "\n","Type of the Least Priority fraction of the most common call: ", calltype_leastprio)



