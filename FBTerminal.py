from os import system, chdir
from facepy import GraphAPI 
from subprocess import Popen, PIPE
from random import randint
from time import time
import sys
import StringIO
#Edit this string with the path to your Google Drive folder
gdrive = "\"C:\Users\Aneesh Durg\Google Drive\""
#To get your own key add the app TerminalAnywhere on FaceBook. Contact durg2@illinois.edu for details
APIkeyReader = open('apikey.txt', 'r')
APIkey = APIkeyReader.read()
APIkeyReader.close()
graph = GraphAPI(APIkey)
a = graph.get('me/feed')
last = a['data'][0]['message']
fileCreated = False
postedID = None
locked = True
key = "#"
start = time()
uptime = start
for i in xrange(5):
    key+=str(randint(0, 9))
print "Please post the following to unlock FBTerminal: "+key
while True:
    if locked:
        now = time()-start
        if now%10==0:
            a = graph.get('me/feed')
            cmd = a['data'][0]['message']
            if cmd == key:
                print 'unlocked'
                if postedID is not None:
                  graph.delete(postedID)
                locked = False
                posted = graph.post('me/feed', message='FBTerminal was successfully unlocked!')
                postedID = posted['id']
                continue
            elif cmd==':printKey':
             print key
            else:
                continue
        else:
            continue

    if fileCreated:
        system('del output.txt')
        fileCreated = False
    
    a = graph.get('me/feed')
    cmd = a['data'][0]['message']
    
    fileCreated = False    
    if cmd[0] == ':' and cmd!=last:
        if cmd[1:]=='exit':
            if postedID is not None:
                graph.delete(postedID)
            exit()
        elif cmd[1:]=='lockFBTerm':
            start = time()
            print 'locked'
            key = "#"
            for i in xrange(5):
                key+=str(randint(0, 9))
            print "Please post the following to unlock FBTerminal: "+key
            locked = True
            if postedID is not None:
                graph.delete(postedID)
                postedID = None
            posted = graph.post('me/feed', message="FBTerminal is locked!")
            postedID = posted['id']
            system("echo "+key+" > passkey.txt")
            system("copy passkey.txt "+gdrive)
            system("del passkey.txt")
        elif cmd[1:] == 'uptime':
            if postedID is not None:
                graph.delete(postedID)
            posted = graph.post('me/feed', message=str(time()-uptime))
            postedID = posted['id']
        elif cmd[1:3]=='ul' and len(cmd)>3 and cmd!=last:
            last = cmd
            #replace the following file path with the path to your google drive folder
            system("copy "+cmd[4:]+" "+gdrive)
        elif cmd[1:]=='start-py':
            if postedID is not None:
                graph.delete(postedID)
                postedID = None
            print "Starting python"
            last = cmd
            while True:
                if postedID is not None:
                    graph.delete(postedID)
                    postedID = None
                toPost = 'type :stop-py to exit\n'
                codeOut = StringIO.StringIO()
                codeErr = StringIO.StringIO()
                code = graph.get('me/feed')['data'][0]['message'] 
                if code==':stop-py':
                    break
                # capture output and errors
                sys.stdout = codeOut
                sys.stderr = codeErr    
                if 'import' not in code and 'exit()' not in code and code!=last:
                    exec code[1:]
                    # restore stdout and stderr
                    sys.stdout = sys.__stdout__
                    sys.stderr = sys.__stderr__
                
                    s = codeOut.getvalue()
                    if len(s)>0:
                        toPost+="output :"+s+"\n"

                    s = codeErr.getvalue()
                    if len(s)>0:
                        toPost+="errors: "+s
                    posted = graph.post('me/feed', message=toPost)
                    postedID = posted['id']
                last = code   
 
        #Windows only, sorry. Please check that Jrepl.bat is added to your PATH
        elif cmd[1:]=='start-jrepl':
            if postedID is not None:
                graph.delete(postedID)
            print "Starting Jrepl"
            last = cmd
            p = Popen(["jrepl"], shell=True, stdin=PIPE, stdout=PIPE)
            while True:
                toPost = 'type :stop-jrepl to exit\n'
                a = graph.get('me/feed')
                jcmd = a['data'][0]['message']
                if jcmd[0]==':' and jcmd == ':stop-jrepl':
                    p.stdin.write('exit'+'\n')
                    last = ':'+jcmd
                    print "Stopping Jrepl"
                    postedID = None
                    break
                elif jcmd!='' and jcmd!=last and jcmd[0]==':':
                    jcmd = jcmd[1:]
                    p.stdin.write(jcmd+'\n')
                    p.stdin.flush()
                    response = ''
                    while not "[" in response:
                        response = p.stdout.readline()
                    toPost+=response
                    while '----' not in response:
                        response = p.stdout.readline()
                        if response!='':
                            toPost+="\n"+response
                    print toPost
                    if postedID is not None:
                        graph.delete(postedID)
                    posted = graph.post('me/feed', message=toPost)
                    postedID = posted['id']
                last = jcmd
        else:
            if cmd[1:3]=='cd' and len(cmd)>3:
                chdir(cmd[4:])
                fileCreated = False
            else:
                # if cmd[0:5] == 'echo' or cmd[0:4] == 'dir':
                fileCreated = True
                if cmd[1:5] == 'echo':
                   # print cmd
                   pass
                if '>' in cmd:
                    fileCreated = False
                    system(cmd[1:])
                else:
                    system(cmd[1:]+'> output.txt')
                print cmd
            last = cmd
    if fileCreated:
        outputFile = open('output.txt', 'r')
        output = outputFile.read()
        outputFile.close()
        if len(output)!=0:
            print output
            if postedID is not None:
                graph.delete(postedID)
            posted = graph.post('me/feed', message=output)
            postedID = posted['id']
