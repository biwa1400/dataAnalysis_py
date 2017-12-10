import pandas as pd
import loraSql
import matplotlib.pyplot as pyplot

def barShow(results, itemNums):
	for itemNum in itemNums:
		item = results[itemNum]
		labels = [str(value) for value in set(item)]
		sizes = [item.count(float(label)) for label in labels]
		
		pyplot.bar(labels,sizes,width=0.1)
		pyplot.xticks(rotation=90)
		pyplot.show()

def pieShow(results, itemNums):
	for itemNum in itemNums:
		item = results[itemNum]
		labels = [str(value) for value in set(item)]
		sizes = [item.count(float(label)) for label in labels]
		pyplot.pie(sizes,labels=labels,autopct='%1.2f%%')
		pyplot.show()
		
def lineShow(results, items):
	x = results[0]
	for item in items:
		y = item
		pyplot.plot(x,y)
	pyplot.show()

if __name__ == '__main__':
	results = loraSql.getData()
	
	kindTuple = tuple(tuple(result[i] for result in results) for i in range(11))
	time, frequency, sf, rssi, snr, re, val, temp, humidy, airp, weaCondition = kindTuple
	
	weaConditionKind = tuple(set(weaCondition))
	weaConditionKindNum = tuple(weaConditionKind.index(i) for i in weaCondition)
	
	items = (snr,)
	#print(set(weaCondition))
	lineShow(kindTuple,items)

	

