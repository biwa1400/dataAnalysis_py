import urllib.request
from bs4 import BeautifulSoup
import time
import  pymysql

def getHtml(url):
	print ('access:',url)
	try:
		html = urllib.request.urlopen(url).read()
	except urllib.request.URLError as e:
		print ('Download Error',e.reason)
		html = None
	return html
	
def convertTime2String(year,month,day,timeString):
	timeSeg = timeString[-2::]
	hour_str = timeString.split(':')[0]
	hour = int(hour_str)
	minSec = timeString[len(hour_str)+1:-(len(timeSeg)+1)]
	
	if hour>12:
		return None
	
	if timeSeg == 'AM':
		hour = 0 if hour == 12 else hour
	elif timeSeg == 'PM':
		hour = 12 if hour == 12 else hour + 12
	else:
		return None
		
	return (str(year)+'-'+str(month)+'-'+str(day)+' '+str(hour)+':'+str(minSec)+':'+'00')
	
if __name__ == '__main__':
	year = 2017
	month = 11
	
	# connect mysql
	connection=pymysql.connect(host='108.61.171.128',
						   user='*',
						   password='*',
						   db='lora_wan',
						   port=3306,
						   charset='utf8')
						   
	try:
		with connection.cursor() as cursor:
			for i in range (1,31):
				day = i
				results = []

				html = getHtml('https://www.wunderground.com/history/airport/ESNN/'+str(year)+'/'+str(month)+'/'+str(day)+'/DailyHistory.html?req_city=Sundsvall&req_state=Y&req_statename=Sweden&reqdb.zip=00000&reqdb.magic=198&reqdb.wmo=02354')
				soup = BeautifulSoup(html,'html.parser')
				table = soup.find(attrs={'id':'obsTable'}).contents[3]
				for i in range (1,200,2):
					try:
						Dayitme = table.contents[i]
						timeString = convertTime2String(year,month,day,Dayitme.contents[1].string)
						timeArray = time.strptime(convertTime2String(year,month,day,Dayitme.contents[1].string),"%Y-%m-%d %H:%M:%S")
						timeStamp = int(time.mktime(timeArray))
						temperature = int(float(Dayitme.contents[3].find(attrs={'class':'wx-value'}).string))
						humidy = int(Dayitme.contents[9].string[:-1])
						try:
							airp = int(Dayitme.contents[11].find(attrs={'class':'wx-value'}).string)
						except:
							airp = 'null'
						
						condition = Dayitme.contents[-2].string
						if condition is None:
							condition='null'
						
						sql = 'insert into weather set serialNumber = null, receiveTime ='+str(timeStamp)+',temperature ='+str(temperature)+',humidy ='+str(humidy)+',airp ='+str(airp)+',weaCondition ="'+str(condition)+'";'
						cursor.execute(sql)
					except IndexError:
						pass
				connection.commit()	
	finally:
		connection.close()
	
	'''

