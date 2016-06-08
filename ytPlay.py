from browser import window
from browser import timer

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

def unpackVids(vidStr):
    return [lineToList(v) for v in vidStr.split('\n')if v.strip()]

vids = []

def startVideo():
    global vids
    print('inside startVideo....')
    if not vids:
        window.player.stopVideo()
        return
    vidId, start, end = vids.pop(0)
    window.player.loadVideoById(vidId, start)
    window.player.setPlaybackQuality("hd720")
    window.player.playVideo()

    timer.set_timeout(startVideo, (end-start)*1000 + 600)
    print(window.player.getAvailableQualityLevels())

