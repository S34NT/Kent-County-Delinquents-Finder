# import mysql.connector
# from mysql.connector import Error
# from mysql.connector import errorcode
import pandas as pd

def readData():
	counter = 0
	dataFields = {"Parcel Number":[],"Government Unit":[],"Owner Name One":[],"Owner Name Two":[],"Property Address":[],
	"Property Classification":[],"School District Number & Name":[],"taxOwed":[],"Years Delinquent":[],"Most Recent Sale Date":[],
	"Liber / Page":[],"Instrument #":[],"Qualification":[],"Type":[],"Most Recent Sale Price":[],"Net Price":[]}; #dataFields will contain every field for a single row


	tempFields = "" #tempFields is used to create the last two fields
	# with open('KCscraperData.txt', 'r') as file:
	file = open("theData.txt", 'r')

	
	#Loop through the file and process it 7 lines at a time
	rowCounter = 0
	loopControl = True
	while(loopControl):

		#Every 7 lines in the file makes up a single row to be sent to the database
		for x in range(0, 8):
	
			#Read a line from the file and send it to clean()
			oneLine = file.readline()
			
			if not oneLine:
				
				df = pd.DataFrame(dataFields)
				print(df)

				df.to_csv('FinalData.csv')

				loopControl = False
				
				return
			

			oneLine = clean(oneLine, x)
		
				#For every line except for the last 2  store the value returned from
				#the clean() function inside the dataFields dictionary
			if(x==0):
				dataFields['Parcel Number'].append(oneLine)

			elif(x==1):
				dataFields['Government Unit'].append(oneLine)

			elif(x==2):
				dataFields['Owner Name One'].append(oneLine)

			elif(x==3):
				if not oneLine:
					oneLine = "None"
					dataFields['Owner Name Two'].append(oneLine.rstrip("\n"))
				else:
					dataFields["Owner Name Two"].append(oneLine)

			elif(x==4):
				dataFields['Property Address'].append(oneLine)

			elif(x==5):
				dataFields['Property Classification'].append(oneLine)
				
			elif(x==6):
				sep = '\n'
				
				tempFields = oneLine.rstrip("\n")
				district = tempFields.split(sep, 1)[0]
				taxOwed = tempFields.split(sep, 1)[1]

				#Add the district to the dictionary
				dataFields["School District Number & Name"].append(district)                   

				taxOwedAndYearsDelinquent = findYearsTotal(taxOwed)
				dataFields['taxOwed'].append(str(taxOwedAndYearsDelinquent[0]))
				dataFields['Years Delinquent'].append(str(taxOwedAndYearsDelinquent[1]))
				
			elif(x==7):
				if(oneLine[0] != ',>>\n'):
					dataFields['Most Recent Sale Date'].append(oneLine[0])
					dataFields['Liber / Page'].append(oneLine[1])
					dataFields['Instrument #'].append(oneLine[2])
					dataFields['Qualification'].append(oneLine[3])
					dataFields['Type'].append(oneLine[4])
					dataFields['Most Recent Sale Price'].append(oneLine[5])
					dataFields['Net Price'].append(oneLine[6])
				else:
				
					dataFields['Most Recent Sale Date'].append("None")
					dataFields['Liber / Page'].append("None")
					dataFields['Instrument #'].append("None")
					dataFields['Qualification'].append("None")
					dataFields['Type'].append("None")
					dataFields['Most Recent Sale Price'].append("None")
					dataFields['Net Price'].append("None")
					
					
				# dataSeries = pd.Series(dataFields)
				# df = df.append(dataSeries, ignore_index=True)
				

				# print("row 0: " + dataFields[0])
				# print("row 1: " + dataFields[1])
				# print("row 2: " + dataFields[2])
				# print("row 3: " + dataFields[3])
				# print("row 4: " + dataFields[4])
				# print("row 5: " + dataFields[5])
				# print("row 6: " + dataFields[6])
				# print("row 7: " + dataFields[7])
				# print("row 8: " + dataFields[8])
				# print("row 9: " +dataFields[9])
				# print("row 10: " +dataFields[10])
				# print("row 11: " +dataFields[11])
				# print("row 12: " +dataFields[12])
				# print("row 13: " +dataFields[13])
				# print("row 14: " +dataFields[14])


	

			
				

				# print(dataSeries)

		

				# oneLine = ''



				# print(dataFields)
				

				#sendtoDB method takes the datafields dictionary as an argument
	file.close()			# sendToDB(dataFields)


#FindYearsTotal takes the taxOwed String and
def findYearsTotal(taxOwed):
	count = 0
	for x in taxOwed:
		if(x == '$'):
			if('$0.00' not in taxOwed):
				count+=1
	if(count == 1):
		taxOwed = taxOwed.replace(",","")
		taxOwed = taxOwed.lstrip("$")
		return (float(taxOwed), count)
	else:
		taxDefaults = taxOwed.split(",$")
		taxDefaults[0] = taxDefaults[0].lstrip("$")
		taxDefaultsTotal = 0.0
		for i in range(0, len(taxDefaults)):
			taxDefaultsTotal += float(taxDefaults[i].replace(",",""))


		
		return (taxDefaultsTotal, count)

		
def clean(oneLine, index):

    #If this line is the last line, set index to the first '$' char
	if(index == 6):
		idx = oneLine.find("$")
        
        #taxOwed is set to  the right hand portion of the string
		taxOwed = oneLine[idx:].rstrip(",> \n")
        #district is set to the left hand portion of the string
		district = oneLine[:idx].rstrip(",")
        
		return(district + '\n' + taxOwed)

	if index == 7:
		oneLine = oneLine.split('\t')

		if(oneLine[0].find('/') == -1):
			oneLine[0] = ',>>\n'

		for element in oneLine:
			if oneLine == '':
				element = 'None'
	else:

		#Find the index of the first colon char and remove it
		#Along with every other character to the left
		idx = oneLine.find(":") + 1
		oneLine = oneLine[idx:].lstrip()
		
	return oneLine


if __name__=="__main__":
	readData()

# def sendToDB(dataFields):
	
# 	try:
# 		connection = mysql.connector.connect(host='******',
# 	                                         database='housingGR2',
# 	                                         user='root',
# 	                                         password='******')

# 		dataFields['ParcelNumber'] = dataFields.pop(0)
# 		dataFields["GovernmentUnit"] = dataFields.pop(1)
# 		dataFields["Owner1"] = dataFields.pop(2)
# 		dataFields["Owner2"] = dataFields.pop(3)
# 		dataFields["Address"] = dataFields.pop(4)
# 		dataFields["Classification"] = dataFields.pop(5)
# 		dataFields["District"] = dataFields.pop(6)
# 		dataFields["taxOwed"] = dataFields.pop(7)
# 		dataFields["years"] = dataFields.pop(8)

		
# 		columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in dataFields.keys())
# 		values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in dataFields.values())



# 		mySql_insert_query = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('property', columns, values)

# 		cursor = connection.cursor()
# 		cursor.execute(mySql_insert_query, dataFields.values())
# 		connection.commit()
# 		print(cursor.rowcount, "Record inserted successfully into property table")
# 		cursor.close()

# 	except mysql.connector.Error as error:
# 	    print("Failed to insert record into table {}".format(error))

# 	finally:
# 		if (connection.is_connected()):
# 			connection.close()
# 			print("MySQL connection is closed")

