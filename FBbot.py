from os import system
from facepy import GraphAPI 
from subprocess import Popen, PIPE
graph = GraphAPI('CAACEdEose0cBABPz84CtEyvFlZAn5OGZBWwqtufzALwaeIr8EIZA5YBUAnu5PZAuGHvvqZB9EWQxrZBBqF7vHS5xwNRLhfocsL0ZCNWebt6zLBf86TVnUOWUQxvEBPCd1fL4OUr6HzYrEHPrShHbnrcHZCBPPG4dS1fweDRi1hn0OHsQCD5KMcJFZAdPRuf9WV3eZAyxlmg27VwgZDZD')
last = ''
fileCreated = False
while True:
    if fileCreated:
        system('del output.txt')
        fileCreated = False
    a = graph.get('me/feed')
    cmd = a['data'][0]['message']
    time = a['data'][0]['created_time']
    fileCreated = False    
    if cmd[0] == ':' and cmd!=last:
        if cmd[1:]=='start-jrepl':
            print "Starting Jrepl"
            last = cmd[1:]
            p = Popen(["jrepl"], shell=True, stdin=PIPE, stdout=PIPE)
            while True:
                toPost = 'type :stop-jrepl to exit'
                a = graph.get('me/feed')
                jcmd = a['data'][0]['message'][1:]
                if jcmd == 'stop-jrepl':
                    p.stdin.write('exit'+'\n')
                    last = ':'+jcmd
                    print "Stopping Jrepl"
                    break
                elif jcmd!='' and jcmd!=last:
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
                    #graph.post('me/feed', message=toPost)
                last = jcmd
        else:
            # if cmd[0:5] == 'echo' or cmd[0:4] == 'dir':
            fileCreated = True
            if cmd[1:5] == 'echo':
                print cmd
            system(cmd[1:]+'> output.txt')
            print cmd
            last = cmd
    if fileCreated:
        outputFile = open('output.txt', 'r')
        output = outputFile.read()
        outputFile.close()
        if len(output)!=0:
            graph.post('me/feed', message=output)

