PHIBOT                                                                                                 
======


Description
-----------

**wetbot.py** contains a class that abstracts away interacting with the Wetgenes chat. Import wetbot to write a bot of your very own. 

**Example.py** is Phibot, a documented example of a bot using the wetbot module. What you're probably going to want to do is edit this file. All of the more important variables like the bot's name and how it responds to commands are at the top of the code, while the rest of the code contains the functionality. 


Instructions
------------

If you're using Windows or a Mac you can get Phibot running using [Python 2.x.x](http://python.org/download/). It's very important that you download one of the 2.x.x versions, *not* the 3.x.x version! 

Once python is installed, double click on **Example.py** and run it. Make sure **Example.py** and **wetbot.py** are in the same directory or you're going to get some errors! 


If you're using Linux, just run 
 > git clone git@github.com:Lambdanaut/Phibot.git

 > cd Phibot

 > python2 Example.py

AND YOU'RE SET!

enjoy. 


Word Unscrambler
----------------

By default the word unscrambler is disabled in **Example.py**, but it can be re-enabled by downloading a list of words with the filename **wordlist** and putting it in the same folder as **Example.py**. A good place to find wordlists is [Kevin's wordlist page](http://wordlist.sourceforge.net/). It's important to note that the longer the wordlist, the harder the bot has to work to unscramble the word. 


URL Parsing
-----------

If you have the Beautiful Soup library installed, **Example.py** will visit the links posted in the chat and say the page's title to the room. You can download and install Beautiful Soup [here](http://www.crummy.com/software/BeautifulSoup/).
