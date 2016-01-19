import argparse
import socket
import sys
import csv

"""
Simple example pokerbot, written in python.

This is an example of a bare bones pokerbot. It only sets up the socket
necessary to connect with the engine and then always returns the same action.
It is meant as an example of how a pokerbot should communicate with the engine.
"""
THRESHOLD=10.0
class opposer():
    def __init__(self,name):
        self.name=name
        #attributes

class Game():
    def  __init__(self, opponent):
        self.opponent=opposer(opponent)
        self.current_equity=0
        self.cardmap={"2":1,"3":2,"4":3,"5":4,"6":5,"7":8,"8":9,"9":10,"10":11,"J":12,"Q":13,"K":14,"A":0}
        self.equity_dic={}
        self.potsize=0
        self.numBoardCards=0
        self.BoardCards=None
        self.lastActions=None
        self.legalActions=None
        self.timebank=0
        self.button=False
        self.handId=0
        self.holeCards=None
        self.myBank=0
        self.otherBank=0
       # with open('equity.csv', 'rb') as f:
        #    reader=csv.reader(f)
         #   for row in reader:
         #               self.equity_dic[row[1]]=row[3]

    def play_handler(self,packet):
        if packet[0]=="GETACTION":
            self.play(packet)
        elif packet[0]=="KEYVALUE":
            pass
        elif packet[0]=="REQUESTKEYVALUES":
            s.send("FINISH\n")
        elif packet[0]=="NEWHAND":
            self.handId=packet[1]
            self.button=packet[2]
            self.holeCards=packet[3:7]
            self.myBank=packet[7]
            self.otherBank=packet[8]
            self.timebank=packet[9]
            #self.current_equity=self.equity_dic[" ".join(packet[3:6])]
        else:# handover
            pass
#GETACTION potSize numBoardCards [boardCards] numLastActions [lastActions] numLegalActions [legalActions] timebank
    def play(self,packet):
        place=1
        self.potsize=packet[place]
        place+=1
        self.numBoardCards=int(packet[place])
        place+=1
        self.BoardCards=packet[place:self.numBoardCards+place]
        place+=self.numBoardCards
        numLastActions=int(packet[place])
        place+=1
        self.lastActions=packet[place:place+numLastActions]
        place+=numLastActions
        numLegalActions=int(packet[place])
        place+=1
        self.legalActions=packet[place:place+numLegalActions]
        place+=numLegalActions
        self.timebank=packet[place]
        
      



class Player:
    def run(self, input_socket):
        # Get a file-object for reading packets from the socket.
        # Using this ensures that you get exactly one packet per read.
        f_in = input_socket.makefile()
        data = f_in.readline().strip()
        game=Game(data.split()[2])#initilize game against a certian player
        while True:
            # Block until the engine sends us a packet.
            data = f_in.readline().strip()
            # If data is None, connection has closed.
            if not data:
                print "Gameover, engine disconnected."
                break
            words = data.split()
            game.play_handler(words)
            

            # When appropriate, reply to the engine with a legal action.
            # The engine will ignore all spurious responses.
            # The engine will also check/fold for you if you return an
            # illegal action.
            # When sending responses, terminate each response with a newline
            # character (\n) or your bot will hang!
            #word = data.split()[0]
           # if word == "GETACTION":
                # Currently CHECK on every move. You'll want to change this.
           #     s.send("CHECK\n")
            #elif word == "REQUESTKEYVALUES":
                # At the end, the engine will allow your bot save key/value pairs.
                # Send FINISH to indicate you're done.
              #  s.send("FINISH\n")
        # Clean up the socket.
        s.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A Pokerbot.', add_help=False, prog='pokerbot')
    parser.add_argument('-h', dest='host', type=str, default='localhost', help='Host to connect to, defaults to localhost')
    parser.add_argument('port', metavar='PORT', type=int, help='Port on host to connect to')
    args = parser.parse_args()

    # Create a socket connection to the engine.
    print 'Connecting to %s:%d' % (args.host, args.port)
    try:
        s = socket.create_connection((args.host, args.port))
    except socket.error as e:
        print 'Error connecting! Aborting'
        exit()

    bot = Player()
    bot.run(s)
