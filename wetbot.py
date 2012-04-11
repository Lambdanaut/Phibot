import socket, copy, time

HOST = '205.185.117.197'
PORT = 843

class Bot:
  def __init__(self):
    self.COOLDOWN_TIME = 2.5
    self.BAD_WORDS = ["cunt","fuck","shit","nigger","faggot","boxxy","kongregate","steam"]

    self.last = {"cmd":"say"}

    self.sayCooldown = 0 
    self.lastTime = time.time()

    self.validKeys = ["cmd","frm","txt","note","arg1","arg2","arg3","arg4","arg5"]

  def find(self, username):
    '''
      If the user is logged in, finds the room they're in.
    '''
    self.send("&cmd=find&user=" + username)

  def join(self, room):
    '''
      Joins a room.
    '''
    self.send("&cmd=join&room=" + room)

  def login(self, username, password = None):
    '''
      Logs into wetgenes under the given username. A password is optional. 
    '''
    msgToSend = "&cmd=login&name=" + username
    if password: msgToSend += "&pass=" + password
    self.send(msgToSend)

  def logout(self):
    '''
      Logs out of the account.
      You'll likely be thrown into the "limbo" room after issuing this command. 
    '''
    self.send("&cmd=logout")

  def me(self, message):
    '''
      Sends a message to the chat of the form "YOUR USERNAME message"
      It can be used to do things like "Phibot jumped up and down and screamed for joy! "
    '''
    self.send("&cmd=act&txt=" + message)

  def rooms(self):
    '''
      Gets a list of all the available rooms and their properties. 
    '''
    self.send("&cmd=rooms")

  def say(self, message, ignoreCooldown=False, ignoreBadWords=False):
    '''
      Sends a message to the chat of the form "YOUR USERNAME: message"
      It's really just saying something to the chat room. 
    '''
    # Update cooldown to preven spam
    self.sayCooldown -= time.time() - self.lastTime
    self.lastTime = time.time()
    if (ignoreCooldown or self.sayCooldown <= 0) and (ignoreBadWords or all(map(lambda w: w not in message, self.BAD_WORDS ) ) ):
      self.send("&cmd=say&txt=" + message)
      self.sayCooldown = self.COOLDOWN_TIME 

  def userInfo(self, username):
    '''
      Gets some information about the user
    '''
    self.send("&cmd=note&note=info&info=user&name=" + username + "& amp;")

  def unscramble(self, word, wordlist):
    ''' 
      Given a scrambled word and a list of words, it gives a list of possible unscramblings of the word.
    '''
    word = word.lower()
    wordlist = map(lambda w: w.lower(), wordlist)
    wordLength = len(word)
    downsized = filter (lambda w: len(w) == wordLength, wordlist)
    sameLetters = []
    for w in downsized:
      toAdd = True
      for letter in word:
        if letter not in w: 
          toAdd = False
          break
      for letter in w:
        if letter not in word:
          toAdd = False
          break
      if toAdd: sameLetters.append(w)
    if sameLetters: return sameLetters
    else:           return None

  def connect(self, host, port):
    '''
      Connects to the server
    '''
    self.host = host
    self.port = port
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.connect((self.host, self.port))

  def guessType(self, message, originalGuess):
    ''' Takes a parsed message and returns a guess of the message's cmd. '''
    if "note" in message:
      if message["note"] in ["welcome","rename","name","notice","join","part","act"]:
        return "note"

    # I have no idea! 
    return originalGuess

  def parse(self, message):
    ''' Parses a message into a dict '''
    # Parse a compound message
    if message.count("\n\x00") > 1: 
      for msg in message.split("\n\x00"):
        self.parse(msg)
      return {}
    # Parse a singular message
    parsedMsg = {}
    key = value = ""
    inKey = False
    for char in message:
      if   char == "&" and not inKey:
        if key in self.validKeys: parsedMsg[key] = value
        key = value = ""
        inKey = True
      elif char == "=" and inKey:
        inKey = False
      elif inKey: key   += char
      else:       value += char

    # Add information from past messages to the current message. 
    updatedMsg = copy.deepcopy(parsedMsg)
    if "cmd" not in updatedMsg: updatedMsg["cmd"] = self.guessType(updatedMsg,self.last["cmd"])
    if updatedMsg["cmd"] in self.last:
      for key in self.validKeys:
        if key not in updatedMsg and key in self.last[updatedMsg["cmd"] ]: 
          updatedMsg[key] = self.last[updatedMsg["cmd"]][key]
    self.last[updatedMsg["cmd"] ] = updatedMsg

    return updatedMsg 

  def getUpdates(self):
    ''' Reads and parses the newest data from the server into list of informative dictionaries. '''
    return self.parse(self.read() )

  def read(self):
    ''' Reads data from the server. '''
    return self.s.recv(1024)
  
  def send(self, data):
    ''' Sends data to the server. '''
    self.s.sendall(data + "&\n\x00")

  def die(self):
    '''
      Logs out and closes the connection with the server
    '''
    self.logout()
    self.s.close()
