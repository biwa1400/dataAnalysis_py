import  pymysql
import  pymysql.cursors
import  json
import  bisect
import json

def getData():
	try:
		f = open('dbConfig.json', 'r')    # 打开文件
		dbConfigFile = f.read()          # 读取文件内容
		print(dbConfigFile)
		jsonData = json.loads(dbConfigFile)
		sql_host = jsonData['sql_host']
		sql_user = jsonData['sql_user']
		sql_password = jsonData['sql_password']
		table = jsonData['table']
	finally:
		if f:
			f.close()                     # 确保文件被关闭

	connection=pymysql.connect(host=sql_host,
							   user=sql_user,
							   password=sql_password,
							   db='lora_wan',
							   port=3306,
							   charset='utf8')
	try:
		with connection.cursor() as cursor:
			
			weaterList = []
			#weather
			sql='SELECT from_unixtime(receiveTime),temperature,humidy,airp,weaCondition FROM lora_wan.weather order by receiveTime'
			cursor.execute(sql)
			results = cursor.fetchall()
			for result in results:
				weaterList.append(tuple(x for x in result))
			
			weather_times = [x[0] for x in weaterList]
			queryResults = []
			#commvalue
			sql='SELECT from_unixtime(receiveTime),channelFrequency,sf,RSSI,SNR,cast(FRMPayload as char) FROM lora_wan.'+table
			cursor.execute(sql)
			results = cursor.fetchall()
			
			for result in results:
				#compare weather_times(time of weather web) and lora packet time
				i = bisect.bisect_left(weather_times, result[0])
				queryResults.append(tuple(x for x in result[:-1:])+(json.loads(result[5])['r'],json.loads(result[5])['l'])+weaterList[i][1::])			
	
			
	finally:
		connection.close()
		
	return queryResults

	