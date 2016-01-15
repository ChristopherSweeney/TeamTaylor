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
class opposer():
    def __init__(self,name):
        self.name=name
        #attributes

class Game():
    def  __init__(self, opponent):
        self.opponent=opposer(opponent)
        self.current_equity=0
        self.equity_dic={}
        self.potsize=0
        self.numBoardCards
        self.BoardCards=None
        self.lastActions=None
        self.legalActions=None
        self.timebank=0
        with open('equity.csv', 'rb') as f:
            reader=csv.reader(f)
            for row in reader:
                self.equity_dic[row[1]]=row[2]


    def play_handler(self,packet):
        if packet[0]=="GETACTION":
            self.play(packet)
        elif packet[0]=="KEYVALUE":
            pass
        elif packet[0]=="REQUESTKEYVALUES":
            s.send("FINISH\n")
        elif packet[0]=="NEWHAND":
            pass
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
        self.BoardCards=packet[place:numBoardCards+place]
        place+=numBoardCards
        numLastActions=int(packet[place])
        place+=1
        self.lastActions=packet[place:place+numLastActions]
        place+=numLastActions
        numLegalActions=int(packet[place])
        place+=1
        self.legalActions=packet[place:place+numLegalActions]
        place+=numLegalActions
        self.timebank=packet[place]
        if self.numBoardCards==0:
            preflop()
        elif self.numBoardCards==3:
            flop()
        elif self.numBoardCards==4:
            turn()
        else:
            river()

        if ("Ah" or "Ac" or "Ad" or "As") in self.BoardCards:
             s.send("CHECK\n")
        else:
            s.send("FOLD\n")
        def preflop():
            pass
        def flop:
            pass
        def turn:
            pass
        def river:
            pass



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
