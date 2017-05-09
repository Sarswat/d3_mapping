# quick-n-dirty script for taking subset of data: 
# Save records within a certain distance from a lat/lng point, to another file
import csv
from geopy.distance import great_circle


file_in = "Parking_meters.csv"
file_out = "Parking_meters_sm.csv"


locationIndex = 15				 	# This is just the index is for "Location" in the csv
center = (37.78449, -122.40769)		# Point in downtown SF
maxMiles = 1  						# Max distance from center point

def getRows(file_path):
	rows = []

	with open(file_path, 'rb') as f:
		reader = csv.reader(f)

		# save header row, before looking through data
		headers = next(reader, None)  # returns the headers or `None` if the input is empty
		if headers:
			rows.append(headers)
		    

		for row in reader:
			# convert string from csv to array of lat,lng
			loc = row[locationIndex][1:-1]
			loc = loc.replace(' ', '')
			loc = loc.split(',')
			lat = loc[0]
			lng = loc[1]  
			loc = (lat,lng)

			dist = great_circle(center, loc).miles

			if dist < maxMiles:
				rows.append(row)
			
		f.close()
	return rows


def saveAsCSV(rows, file_name):
	with open( file_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerows(rows)

	f.close()



rows = getRows(file_in)
saveAsCSV(rows, file_out)
	
print 'Meterss within ', maxMiles, 'miles: ', len(rows)