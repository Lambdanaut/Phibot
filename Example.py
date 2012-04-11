import wetbot
import datetime, random, urllib
try: 
  import BeautifulSoup
  parseURLs = True
except ImportError: 
  parseURLs = False

# The Username of the bot
BOT_NAME   = "Phibot"

# Optional Password
BOT_PASS   = ""

# The bot's "nickname". All commands to the bot will be prefaced with this. 
# For example, if BOT_NICK is "frog", commands to the bot would look like "frog say LOL" or "frog die"
BOT_NICK   = "phi"

# The Owner's username. The bot will only listen to commands from the BOT_MASTER.
BOT_MASTER = "DarkScythe"

# The room the bot will join when it starts up. 
HOME_ROOM  = "darkscythe"

# A list of users that the bot holds in high regards
FRIENDS = ["DarkScythe","fish"]

# A list of dorks that the bot thinks are huge stinkers
IDIOTS = ["Hiduko","baby_wolf","Bitch"]

# Commands
SAY        = BOT_NICK + " say "
DO         = BOT_NICK + " do "
DIE        = BOT_NICK + " die"
JOIN       = BOT_NICK + " join "
FOLLOW     = BOT_NICK + " follow "
MIMIC      = BOT_NICK + " mimic "
TEND       = BOT_NICK + " tend"
UNSCRAMBLE = BOT_NICK + " unscramble"
STOP       = BOT_NICK + " stop"
HELP       = BOT_NICK + " help"

# Personalized Messages
DIE_MSG          = "I'm blowin' this posicle stand. "
STOP_MSG         = "I'm ceasing all coolio activity. "
TEND_MSG         = "I'll tend to the room, sir! "
UNSCRAMBLE_MSG   = "I'll unscramble all the scrambled challenges I see. "
GREETINGS_LIST   = ["Salutations ", "G'day ", "Howdy ", "Haldo ", "Hello ", "Hi ", "Hey there "]
KEYWORD_RESPONSE = "It's spelled \"DarkScythe\", idiot. "

# A list of words that the bot will respond to by saying KEYWORD_RESPONSE
KEYWORD_LIST = ["dorkscythe","darksythe","dark sythe","darkscithe"]

# The help message that describes all the bot's commands
HELP_MSG = BOT_NAME + "'s Commands\n  " + SAY + "MESSAGE : Makes " + BOT_NAME + " say MESSAGE in the chat. \n  " + DO  + "MESSAGE : Makes " + BOT_NAME + " do MESSAGE in the chat. It's the equivalent of /me\n  " + DIE + " : Makes " + BOT_NAME + " logout of wetgenes and shutdown. \n  " + FOLLOW + "USERNAME : Makes " + BOT_NAME + " join whatever room USERNAME in in, and follow him around from room to room.\n  " + MIMIC + "USERNAME: Makes " + BOT_NAME + " copy everything a user says. Combined with follow, this can be quite annoying. \n  " + TEND + " : Makes " + BOT_NAME + " tend to the current room and greet guests.  \n  " + STOP + " : Makes " + BOT_NAME + " stop doing whatever he's doing, whether it be following, tending to a room, or mimicking. \n  " + HELP + " : Displays this help message ! \nPhibot and the wetbot Python library are copyright Josh Thomas. All Rights Reserved. "

# Unscrambler Wordlist File
WORDLIST_FILE = "wordlist"

# Where to store chat logs
LOG_FILE = "log"

# Hints
WORD_SCRAMBLE = "I am thinking of a word that can be made from the letters "

# Extra Functions
def startsWith(string, start):
  for char in range(0, len(start) ):
    try: 
      if start[char] != string[char]: return False
    except IndexError: return False
  return True

def takeWhile(function, string):
  newString = ""
  for char in string:
    if function(char):
      newString += char
    else: return newString
  return newString

if not BOT_PASS:
  BOT_PASS = None

# Connect, Login, and Join your HOME_ROOM
bot = wetbot.Bot()
print (" (*) Initialized " + BOT_NAME)
bot.connect(wetbot.HOST, wetbot.PORT)
print (" (*) Connected to the wetgenes server ")
bot.login(BOT_NAME, password=BOT_PASS)
print (" (*) Logged into wetgenes as " + BOT_NAME)
bot.join(HOME_ROOM)
print (" (*) Joined the HOME_ROOM \"" + HOME_ROOM + "\" ")
bot.say(BOT_NAME + " reporting for duty! ")
print (" (*) Sent welcome message ")

if not parseURLs:
  print (" ( ) The Beautiful Soup library wasn't found and so URL parsing is disabled. ")

# Try to open a wordlist for guessing words
try: wordlist = map (lambda w: w.split("\n")[0] , open(WORDLIST_FILE, 'r').readlines() )
except IOError: 
  print (" ( ) The WORDLIST_FILE \"" + WORDLIST_FILE + "\" could not be found. Word guessing is disabled. ")
  wordlist = None

# Try to open a log for saving the chat
try: 
  logFile = open(LOG_FILE, 'a')
  date = datetime.date.today()
  logFile.write("DATE: " + str(date.month) + " - " + str(date.day) + " - " + str(date.year) + "\n")
except IOError: 
  print (" ( ) The LOG_FILE \"" + WORDLIST_FILE + "\" couldn't be opened. Chat logging is disabled. ")
  logFile = None

following = None
mimicking = None
unscramble = False
tendRoom  = False
# Enters a READ & ACT loop
while True:
  # Reads from the server
  message = bot.getUpdates()
  
  # Decides on an action
  if "cmd" in message:
    if message["cmd"] == "say":
      if "frm" in message and "txt" in message:
        txt = message["txt"].strip()
        userMessage = message["frm"] + ": " + txt
        print (userMessage)
        if logFile: logFile.write(userMessage + "\n")

        # Parse URLs for their Title
        if parseURLs:
          urlSpot = txt.find("http://")
          if urlSpot != -1:
            url = takeWhile(lambda char: char != " ", txt[urlSpot:])
            try: 
              title = BeautifulSoup.BeautifulSoup(urllib.urlopen(url) ).title
              if title: bot.say( title.string )
            except: pass

        # Reply to a direct address
        for greeting in GREETINGS_LIST:
          if txt.lower().find(greeting.lower() + BOT_NAME.lower() ) != -1:
            bot.say("How are you doing, " + message["frm"] + "? ")
            break

        # Respond to keywords
        for misspelling in KEYWORD_LIST:
          if txt.lower().find(misspelling) != -1:
            bot.say( KEYWORD_RESPONSE )

        # BOT_MASTER Commands
        if message["frm"].lower() == BOT_MASTER.lower():
          # Say something
          if   startsWith(txt, SAY):
            bot.say( txt[len(SAY):] )
          # Do something
          elif startsWith(txt, DO):
            bot.me( txt[len(DO):] )
          # Quit Wetgenes
          elif startsWith(txt, DIE):
            bot.say( DIE_MSG )
            logFile.close()
            bot.die()
          # Join a room
          elif startsWith(txt, JOIN):
            bot.join( txt[len(JOIN):] )
          # Follow a user between rooms
          elif startsWith(txt, FOLLOW):
            following = txt[len(FOLLOW):].lower()
            bot.say("I'll start following " + following + " right away! ")
          # Mimick everything a user says
          elif startsWith(txt, MIMIC):
            mimicking = txt[len(MIMIC):].lower()
          # Unscramble words given by bots
          elif startsWith(txt, UNSCRAMBLE):
            unscramble = True
            bot.say( UNSCRAMBLE_MSG )
          # Tend to a room
          elif startsWith(txt, TEND):
            tendRoom = True
            bot.say( TEND_MSG )
          # Stops all active monitoring, including following and mimicking users.
          elif startsWith(txt, STOP):
            following = mimicking = None
            tendRoom = unscramble = False
            bot.say( STOP_MSG )
          # Lists a help menu to the console
          elif startsWith(txt, HELP):
            print( HELP_MSG )

        # Mimic a user
        if mimicking:
          if message["frm"].lower() == mimicking:
            bot.say(txt)

        # Unscramble a Word for Cookies
        if wordlist and unscramble:
          if startsWith(txt, WORD_SCRAMBLE):
            word = ""
            for char in txt[len(WORD_SCRAMBLE):]:
              if char != " ":
                word += char
              else: break
            unscrambled = bot.unscramble(word, wordlist)
            if unscrambled:
              for word in unscrambled[:3]:
                bot.say(word, ignoreCooldown=True)

    elif message["cmd"] == "note":
      # Tending to the Room
      if tendRoom:
        if message["note"] == "join":
          if message["arg1"].lower() in map(lambda f: f.lower(), FRIENDS):
            bot.say("Hey there " + message["arg1"] + ", you impressive and cool guy you. ")
          elif message["arg1"].lower() in map(lambda f: f.lower(), IDIOTS):
            bot.say( "Hey " + message["arg1"] + "! You disgust me and your presence is a repugnance on society. Kill yourself!  "  )
          else:
            bot.say( GREETINGS_LIST[random.randint(0,len(GREETINGS_LIST) - 1 ) ] + message["arg1"] + "! " , ignoreCooldown=True)

    if following:
      bot.find(following)
      location = bot.getUpdates()
      if "cmd" in location:
        if location["cmd"] == "note" and "arg1" in location:
          preMessage = (following + " is in room ").lower()
          room = location["arg1"][len(preMessage):].lower()
          if startsWith(location["arg1"].lower(), preMessage ):
            bot.join(room) 
