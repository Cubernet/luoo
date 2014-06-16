#coding=utf-8
import urllib2,re,os,urllib,sys,string,threading,Queue,socket

#期刊链接 http://www.luoo.net/music/001
#
#歌曲详情js代码
#    var volPlaylist = [{"id":"11848","title":"\u522b\u8ba9\u6211\u5b64\u5355","artist":"\u731b\u864e\u5de7\u514b\u529b","album":"\u591c\u5de5\u5382","mp3":"http:\/\/luoo.800edu.net\/low\/luoo\/radio603\/01.mp3","poster":"http:\/\/img.luoo.net\/pics\/albums\/6540\/cover.jpg_580x580.jpg","poster_small":"http:\/\/img.luoo.net\/pics\/albums\/6540\/cover.jpg_60x60.jpg"},{"id":"11849","title":"\u7231\u6211\u4f60\u4f1a\u6b7b","artist":"\u8463\u4e8b\u957f","album":"\u4f17\u795e\u62a4\u53f0\u6e7e","mp3":"http:\/\/luoo.800edu.net\/low\/luoo\/radio603\/02.mp3","poster":"http:\/\/img.luoo.net\/pics\/albums\/6541\/cover.jpg_580x580.jpg","poster_small":"http:\/\/img.luoo.net\/pics\/albums\/6541\/cover.jpg_60x60.jpg"},{"id":"11850","title":"\u900f\u660e\u7684\u591c","artist":"\u660f\u9e26","album":"\u5bd3\u8a00\u5f0f\u7684\u6df1\u9ed1\u8272\u98ce\u666f","mp3":"http:\/\/luoo.800edu.net\/low\/luoo\/radio603\/03.mp3","poster":"http:\/\/img.luoo.net\/pics\/albums\/6542\/cover.jpg_580x580.jpg","poster_small":"http:\/\/img.luoo.net\/pics\/albums\/6542\/cover.jpg_60x60.jpg"},{"id":"11851","title":"\u900f\u660e\u6742\u5fd7Forever","artist":"\u900f\u660e\u6742\u5fd7","album":"\u900f\u660e\u6742\u5fd7Forever","mp3":"http:\/\/luoo.800edu.net\/low\/luoo\/radio603\/04.mp3","poster":"http:\/\/img.luoo.net\/pics\/albums\/6194\/cover.jpg_580x580.jpg","poster_small":"http:\/\/img.luoo.net\/pics\/albums\/6194\/cover.jpg_60x60.jpg"},{"id":"11852","title":"Second Time","artist":"\u5305\u5b50\u864e","album":"\u6240\u5728","mp3":"http:\/\/luoo.800edu.net\/low\/luoo\/radio603\/05.mp3","poster":"http:\/\/img.luoo.net\/pics\/albums\/6543\/cover.jpg_580x580.jpg","poster_small":"http:\/\/img.luoo.net\/pics\/albums\/6543\/cover.jpg_60x60.jpg"},{"id":"11853","title":"\u7b2c\u4e00\u4e2a\u613f\u671b","artist":"\u574f\u5973\u513f","album":"\u5c0f\u592a\u9633","mp3":"http:\/\/luoo.800edu.net\/low\/luoo\/radio603\/06.mp3","poster":"http:\/\/img.luoo.net\/pics\/albums\/6544\/cover.jpg_580x580.jpg","poster_small":"http:\/\/img.luoo.net\/pics\/albums\/6544\/cover.jpg_60x60.jpg"},{"id":"11854","title":"\u79c1\u4eba\u6e38\u6cf3\u6c60","artist":"\u4f4e\u660e\u5ea6\u65f6\u671f","album":"\u5455\u5410","mp3":"http:\/\/luoo.800edu.net\/low\/luoo\/radio603\/07.mp3","poster":"http:\/\/img.luoo.net\/pics\/albums\/6545\/cover.jpg_580x580.jpg","poster_small":"http:\/\/img.luoo.net\/pics\/albums\/6545\/cover.jpg_60x60.jpg"},{"id":"11855","title":"Shadow Killer","artist":"\u9a6c\u514b\u767d","album":"HANDS","mp3":"http:\/\/luoo.800edu.net\/low\/luoo\/radio603\/08.mp3","poster":"http:\/\/img.luoo.net\/pics\/albums\/6546\/cover.jpg_580x580.jpg","poster_small":"http:\/\/img.luoo.net\/pics\/albums\/6546\/cover.jpg_60x60.jpg"},{"id":"11856","title":"\u76f8\u9022","artist":"929","album":"\u76f8\u9022","mp3":"http:\/\/luoo.800edu.net\/low\/luoo\/radio603\/09.mp3","poster":"http:\/\/img.luoo.net\/pics\/albums\/6547\/cover.jpg_580x580.jpg","poster_small":"http:\/\/img.luoo.net\/pics\/albums\/6547\/cover.jpg_60x60.jpg"},{"id":"11857","title":"\u4e16\u754c\u5c3d\u5934","artist":"1976","album":"\u4e0d\u5408\u65f6\u5b9c","mp3":"http:\/\/luoo.800edu.net\/low\/luoo\/radio603\/10.mp3","poster":"http:\/\/img.luoo.net\/pics\/albums\/6548\/cover.jpg_580x580.jpg","poster_small":"http:\/\/img.luoo.net\/pics\/albums\/6548\/cover.jpg_60x60.jpg"}];
#

#三位数生成方法
def getNum(num):
    if num >99 :
        return str(num)
    elif num > 9 and num < 100 :
        return '0' + str(num)
    else:
        return '00' + str(num)

#期刊页面链接生成方法
def getUrl(num):
    url = 'http://www.luoo.net/music/'
    return url + getNum(num)

def readsrc(src):
    try:
        url = urllib2.urlopen(src)
        content = url.read()
        return content
    except:
        print 'readsrc error'
        return None

#专题主题名获取方法
def getName(content):
    p = re.compile(r'<h1 class="fm-title">(.*?)</h1>',re.M)
    r = p.findall(content)
    if r:
        return r
    else:
        return None

#歌曲详情js代码提取方法
def getSongs(content):
    p = re.compile(r'"title":"(?P<title>.*?)","artist":"(?P<artist>.*?)","album":"(?P<album>.*?)","mp3":"(?P<mp3>.*?)"',re.M)
    r = p.finditer(content)
    if r:
#    	for i in r:
#	   		i.groupdict()['mp3'] = re.sub(r'\\',r'',i.groupdict()['mp3'])
        return r
    else:
        return None

#显示进度回调函数
def callbackfunc(blocknum, blocksize, totalsize):
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    print "%.2f%%"% percent 

#下载歌曲
def downloadSong(url,filepath,foldername,songname):

    try:
        urllib.urlretrieve(url,filepath+foldername+'/'+songname+'.mp3')
    except IOError:
        print 'restart download ' + filepath+foldername+'/'+songname+'.mp3'
        downloadSong(url,filepath,foldername,songname)

    return None


class downloadThread(threading.Thread):  
    def __init__(self,que):  
        threading.Thread.__init__(self)  
        #self.que=que  
    def run(self):  
        while True:  
            if not que.empty():  

                songinfo = que.get() 
                url = songinfo['url']
                filepath = songinfo['filepath']
                foldername = songinfo['foldername']
                songname = songinfo['songname']
                print '-----%s------'%(self.name)+'start download ' + filepath+foldername+'/'+songname+'.mp3'
                downloadSong(url,filepath,foldername,songname)
                print '-----%s------'%(self.name)+'finish download ' + filepath+foldername+'/'+songname+'.mp3'
                
            else:  
                break 
        print '-----%s------'%(self.name)+'done------------------------------------------------------------'


def download(que,filepath, vol = '0',rank = '0' ):

    if(filepath == None):
        print 'Please input filepath.'
        sys.exit()
    i = string.atoi(vol)
    rankNum = string.atoi(rank)


    if i == 0:
        isVol = False
    else:
        isVol = True

    if rankNum == 0:
        isRank = False
    else:
        isRank = True

    while(True):
        url = getUrl(i)
        if url == None:
            break
        content = readsrc(url)
        if content == None:
            continue
        foldername = 'VOL '+ getNum(i) + ' ' + getName(content)[0]
        if not os.path.exists(filepath+'/'+foldername):
        	os.makedirs(filepath+'/'+foldername)
        songs = getSongs(content)
        if songs == None:
            continue
        fornum = 1
        i = i + 1

        for song in songs:
            if(fornum != rankNum and isRank):   
                fornum = fornum +1
                continue
            p = re.compile(r'\\')
            mp3url = p.sub(r'',song.groupdict()['mp3'])
            songname = "u'''%s'''"%(song.groupdict()['title'])
            songname = eval(songname)
            songinfo = {'url':mp3url,'filepath':filepath,'foldername':foldername,'songname':songname.encode('utf-8')}

            que.put(songinfo)

            fornum = fornum +1
       
        if(isVol and i == 250):
            break

    threadNum = 3
    for q in range(threadNum):  
        d=downloadThread(que)  
        d.start()


if __name__=='__main__': 

    global que
    que = Queue.Queue()

    socket.setdefaulttimeout(15) 

    if len(sys.argv) < 2:
        print 'No action specified. Using --help for more help.'
        sys.exit()

    if sys.argv[1].startswith('--'):  
        option = sys.argv[1][2:]  
        if option == 'version':  
            print 'Version 1.2'  
        elif option == 'help':  
            print '''
            -----------------------------------------------------------

            This program downloads music from www.luo.net . 
            Options include: 
              --version : Prints the version number 
              --help    : Display this help
              --a       : Download all music from the first vol
              -v[<vol number>]      : Download the specified vol
              -r[<rank of music>]   : Download the specified music
              -p[<filepath>]        : The filepath where to save music

            -----------------------------------------------------------
              '''  
        elif option == 'a':
            if sys.argv[2] == '-p' and len(sys.argv) == 4:
                download(que,sys.argv[3])
            else:
            	print len(sys.argv)
                print 'Please input the filepath where to save music.'
        else:  
            print 'Unknown option.'  
        sys.exit() 

    elif sys.argv[1].startswith('-'):
        option = sys.argv[1][1:]
        if option == 'v':
            if len(sys.argv) == 5 and sys.argv[3] == '-p':
                vol = sys.argv[2]
                filepath = sys.argv[4]
                download(que,filepath,vol)
            elif len(sys.argv) == 7 and sys.argv[3][1:] == 'r' and sys.argv[5] == '-p':
                vol = sys.argv[2]
                rank = sys.argv[4]
                filepath = sys.argv[6]
                download(que,filepath,vol,rank)
            else:
                print 'No action specified. Using --help for more help.'
        elif option == 'r':
            print 'Please set -v for the vol first. Using --help for more help.'

        else:
            print 'No action specified. Using --help for more help.'
            sys.exit() 


    #'/Volumes/MacintoshHD/音乐/luoo/'





