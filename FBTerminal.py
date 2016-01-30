from os import system, chdir
from facepy import GraphAPI 
from subprocess import Popen, PIPE
from random import randint
graph = GraphAPI('CAAYGdFK3zvYBAHCZBpzVbXrztWklY8a63W8qEDZB2eIndk7ZAsh4AtL2EbVtZCIgduuKum1adO91qKanraX9wjX7fbscOAohZCpBlu7lsjdwZAff5HtfWWcUbpl6BxhPGQGOfhmRoU6FNNbycq61KduS9xFzKO6uLYYAsMRloOocSeC7KTGKMV5PvGYvoEzibwMUu0qfp45AZDZD')
a = graph.get('me/feed')
last = a['data'][0]['message']
fileCreated = False
postedID = None
locked = True
key = "#"
for i in xrange(5):
    key+=str(randint(0, 9))
print "Please post the following to unlock FBTerminal: "+key
while True:
    if locked:
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
