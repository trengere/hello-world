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
endTime = 0

def finishedYet():
    global endTime
    if int(window.player.getCurrentTime())<endTime:
        timer.set_timeout(finishedYet,1000)
    else:
        timer.set_timeout(startVideo,200)
        
def startVideo():
    global vids, endTime
    if not vids:
        window.player.stopVideo()
        return
    vidId, start, endTime = vids.pop(0)
    window.player.loadVideoById(vidId, start)
    window.player.setPlaybackQuality("hd720")
    window.player.playVideo()
    timer.set_timeout(finishedYet,1000)
    

timer.set_timeout(startVideo, 500)
