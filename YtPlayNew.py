from browser import window
from browser import timer
from videos import vidStr

def lineToList(streng):
    viId, interval = streng.strip().split()
    res = []
    for v in interval.split('-'):
        if '.' in v:
            if v.count('.') == 1:
                minut, sek = [int(t) for t in v.strip().split('.')]
                res.append(sek + 60*minut)
            else:
                hour, minut, sek = [int(t) for t in v.strip().split('.')]
                res.append(sek + 60*minut + 3600*hour)
        else:
            res.append(int(v))
    start, end = res
    return (viId, start, end)

vids = [lineToList(v) for v in vidStr.split('\n')if v.strip()]
vidId, start, endTime = '', 0, 0
index = -1
nextVid = True

def finishedYet():
    global start, endTime, nextVid
    tid = int(window.player.getCurrentTime())
    if tid<start:
    	nextVid=False
    	timer.set_timeout(startVideo,200)
    elif tid>=endTime:
    	nextVid=True
    	timer.set_timeout(startVideo,200)
    else:
        timer.set_timeout(finishedYet,1000)

def findNextVid(tid):
	global vids, vidId, start, endTime, index, nextVid
	tmpVidId, tmpStart, tmpEndTime = vids[index]
	while tmpVidId == vidId and tmpEndTime <=tid:
		index +=1
		tmpVidId, tmpStart, tmpEndTime = vids[index]
	return index

def findPreviousVid(tid):
	global vids, vidId, start, endTime, index, nextVid
	tmpVidId, tmpStart, tmpEndTime = vids[index]
	while tmpVidId == vidId and tmpStart >tid:
		index -=1
		tmpVidId, tmpStart, tmpEndTime = vids[index]
	return index

    
def startVideo():
    global vids, vidId, start, endTime, index, nextVid
    index += 1 if nextVid else -1
    if not vids or len(vids)<=index or index < 0:
        window.player.stopVideo()
        return
    tid = int(window.player.getCurrentTime())
    tmpVidId, tmpStart, tmpEndTime = vids[index]
    if tmpVidId != vidId:
    	vidId, start, endTime = tmpVidId, tmpStart, tmpEndTime
    else:

    	index = findNextVid(tid) if nextVid else findPreviousVid(tid)
    	vidId, start, endTime = vids[index]
    window.player.loadVideoById(vidId, start)
    window.player.setPlaybackQuality("hd720")
    window.player.playVideo()
    timer.set_timeout(finishedYet,1000)

timer.set_timeout(startVideo, 500)
