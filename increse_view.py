import urllib2


## Work in Progress


id = "2841784";

#url = "http://mediaservices.myspace.com/services/media/video.asmx/IncrementVideoPlays?videoID="+id+"&token=29254735542157_ec2&versionID=1";
url = "https://www.youtube.com/watch?v=DHkbhQC1hDc"

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
usock = opener.open(url)
url = usock.geturl()
data = usock.read()

print data

usock.close()