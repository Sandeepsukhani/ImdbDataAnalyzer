ratingsFile=open('ratings.list','r')
releaseDatesFile=open('release-dates.list','r')
output=open('movieData.list','w')

#Bringing read head to point where required data starts
while True:
	if releaseDatesFile.readline()[0] == "=":
		break;

while True:
	if ratingsFile.readline()=="MOVIE RATINGS REPORT\n":
		break;
ratingsFile.readline()
ratingsFile.readline()

#Extracting details of first movie record from ratings file
ratingLine=ratingsFile.readline().rstrip("\n")
ratingLine=ratingLine.split()
ratingMovieName=" ".join(ratingLine[3:len(ratingLine)])
rating=ratingLine[2]

#Extracting details of first movie record from release-dates file
releaseDateLine=releaseDatesFile.readline().rstrip("\n")
i=releaseDateLine.rfind(":")
releaseDate=releaseDateLine[i+1:len(releaseDateLine)]
while releaseDateLine[i]!=" " and releaseDateLine[i]!="\t":
	i-=1
releaseMovieName=releaseDateLine[0:i+1]
releaseMovieName=releaseMovieName.replace("	","")
releaseMovieName=releaseMovieName.rstrip(" ")

while True:
	#Iterating over records from file
	if ratingLine=="" or releaseDateLine[0:3]=="---":
		break

	#Skipping episodes from serials
	if ratingMovieName.find("{")!=-1:
		ratingLine=ratingsFile.readline().rstrip("\n")
		if ratingLine=="":
			break
		ratingLine=ratingLine.split()
		ratingMovieName=" ".join(ratingLine[3:len(ratingLine)])
		rating=ratingLine[2]
		continue

	if releaseDateLine.find("{")!=-1 or releaseDateLine.find(":")==-1:
		releaseDateLine=releaseDatesFile.readline().rstrip("\n")
		if releaseDateLine[0:3]=="---":
			break
		i=releaseDateLine.rfind(":")
		releaseDate=releaseDateLine[i+1:len(releaseDateLine)]
		while releaseDateLine[i]!=" " and releaseDateLine[i]!="\t":
			i-=1
		releaseMovieName=releaseDateLine[0:i+1]
		releaseMovieName=releaseMovieName.replace("	","")
		releaseMovieName=releaseMovieName.rstrip(" ")
		continue

	#Adding matched record from rating and release date file	
	if ratingMovieName==releaseMovieName:
		output.write("attribute:"+ratingMovieName)
		output.write("attribute:"+rating)
		output.write("attribute:"+releaseDate)
		output.write("\n")
		ratingLine=ratingsFile.readline().rstrip("\n")
		if ratingLine=="":
			break
		ratingLine=ratingLine.split()
		ratingMovieName=" ".join(ratingLine[3:len(ratingLine)])
		rating=ratingLine[2]

		releaseDateLine=releaseDatesFile.readline().rstrip("\n")
		if releaseDateLine[0:3]=="---":
			break
		if releaseDateLine.find(":")==-1:
			continue
		i=releaseDateLine.rfind(":")
		releaseDate=releaseDateLine[i+1:len(releaseDateLine)]
		while releaseDateLine[i]!=" " and releaseDateLine[i]!="\t":
			i-=1
		releaseMovieName=releaseDateLine[0:i+1]
		releaseMovieName=releaseMovieName.replace("	","")
		releaseMovieName=releaseMovieName.rstrip(" ")
		continue
	
	if ratingLine=="" or releaseDateLine[0:3]=="---":
		break

	#Moving read pointer to handle problem of missing records
	while ratingMovieName<releaseMovieName:
		ratingLine=ratingsFile.readline().rstrip("\n")
		if ratingLine=="":
			break
		if ratingLine.find("{")!=-1:
			continue
		ratingLine=ratingLine.split()
		ratingMovieName=" ".join(ratingLine[3:len(ratingLine)])
		rating=ratingLine[2]
	
	#Moving read pointer to handle problem of missing records
	while releaseMovieName<ratingMovieName:
		releaseDateLine=releaseDatesFile.readline().rstrip("\n")
		if releaseDateLine[0:3]=="---":
			break
		if releaseDateLine.find(":")==-1 or releaseDateLine.find("{")!=-1:
			continue
		i=releaseDateLine.rfind(":")
		releaseDate=releaseDateLine[i+1:len(releaseDateLine)]
		while releaseDateLine[i]!=" " and releaseDateLine[i]!="\t":
			i-=1
		releaseMovieName=releaseDateLine[0:i+1]
		releaseMovieName=releaseMovieName.replace("	","")
		releaseMovieName=releaseMovieName.rstrip(" ")
#Closing files
ratingsFile.close()
releaseDatesFile.close()
output.close()
