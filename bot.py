#!/usr/bin/env python
#
# A bot for giving ops to people based on username or IP

import irc.bot
import irc.strings
import ConfigParser

class Botje(irc.bot.SingleServerIRCBot):
    def __init__(self, channels, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, "FreeOpsForEverybody")
        self.channels = channels

    def on_welcome(self, c, e):
        for chan in self.channels:
            c.join(chan)

    def on_join(self, c, e):
        nick, address = e.source.split('!')
        user, ip = address.split('@')
        channel = e.target
        self.checkops(c, channel, nick, ip)

    def checkops(self, c, channel, nick, ip):

        print "Checking ops for "+nick+"@"+ip+" in "+ channel

        with open("modes.txt","r") as modefile:
            for line in modefile:
                if line.rstrip() == channel + " +v " + nick:
                    c.mode(channel, "+v "+nick)
                    print "gave +v"

                if line.rstrip() == channel + " +o " + nick:
                    c.mode(channel, "+o "+nick)
                    print "gave +o"

                if line.rstrip() == channel + " +v @" + ip:
                    c.mode(channel, "+v "+nick)
                    print "gave +v based on ip"

                if line.rstrip() == channel + " +v @" + ip:
                    c.mode(channel, "+o "+nick)
                    print "gave +o based on ip"


def main():
    c = ConfigParser.RawConfigParser()   
    c.read("config.ini")    

    server = c.get("connection","server")
    port = c.get("connection","port")
    nickname = c.get("connection","nickname")
    channels = c.get("connection","channels").split()

    bot = Botje(channels, nickname, server, port)
    bot.start()

if __name__ == "__main__":
    main()
