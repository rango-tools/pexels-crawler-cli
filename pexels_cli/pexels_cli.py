__author__ = "Amirhossein Douzendeh Zenoozi"
__license__ = "MIT"
__version__ = "0.1.0"
__proxy__ = False
__doc__ = """
Pexels CLI Crawler
Usage:
    pexels search [--show-browser] [--load-time=<seconds>] [--page-count=<count>] <keyword>
    pexels -h | --help
    pexels -v | --version
------------------------------------------------------------------
Options:
    --folder-name               Destination Folder name, Default: downloads
    --show-browser              Showing Browser if You Need, Default: False
    --load-time=<seconds>       Infinite Scroll Time Out, Default: 5
    --page-count=<count>        Page Counter, Default: 0 (All Pages)
    -h --help                   Show this screen.
    -v --version                Show version.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from random import randint, random
from colorama import Fore, Style
from docopt import docopt
from time import sleep

import urllib
import urllib.request as req
import urllib.parse as parse

import os
import requests
import shutil
import time
import re
import sqlite3
import json


class PexelsCrawler:
    def __init__(self, **kwargs):
        # Browser UserAgent
        userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        # DataBase Connection Config
        self.dataBaseConnection = sqlite3.connect('pexels.db')
        self.folderName = kwargs.get('folderName', 'downloads')
        self.showBrowser = kwargs.get('showBrowser', True)
        self.ScrollTimeout = kwargs.get('ScrollTimeout', 5)
        self.ScrollCounte = kwargs.get('ScrollCounte', 0)
        
        # Create New Folder Base on Keyword Search
        self.currentPath = os.path.abspath(os.getcwd())
        self.downloadPath = os.path.join( self.currentPath, self.folderName)
        if not os.path.exists( self.downloadPath ):
            os.makedirs( self.downloadPath )
        
        try:
            self.dataBaseConnection.execute('''CREATE TABLE pexels
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                link_slug TEXT NOT NULL);''')
        except sqlite3.Error as error:
            print(error)
            pass

        # Selenium Driver Options
        self.driverOption = webdriver.ChromeOptions()
        self.driverOption.add_argument('log-level=3')
        self.driverOption.add_argument(f'user-agent={userAgent}')

        if( not self.showBrowser ):
            self.driverOption.add_argument('headless')

        self.driver = webdriver.Chrome( options = self.driverOption )

    def infiniteScroll(self, timeout, counte):
        scrollPauseTime = timeout

        # Get scroll height
        lastHeight = self.driver.execute_script("return document.body.scrollHeight")
        loopIndex = 0

        while ( loopIndex <= counte ):
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep( scrollPauseTime )
            # Calculate new scroll height and compare with last scroll height
            newHeight = self.driver.execute_script("return document.body.scrollHeight")
            if newHeight == lastHeight:
                # If heights are the same it will exit the function
                break
            lastHeight = newHeight
            
            # Make Infinite Loop
            if ( counte != 0 ):
                loopIndex += 1

    def saveImage( self, imageUrl, targetName ):
        try:
            sleep( random() * 5 )
            opener = req.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0')]
            req.install_opener(opener)
            splitedUrl = imageUrl.split("/")
            splitedUrl[-1] = parse.quote( splitedUrl[-1] )
            imageUrl = '/'.join(splitedUrl)
            req.urlretrieve( imageUrl, targetName )
        except urllib.error.HTTPError as err:
            print('\n')
            print('========================')
            print(f'Error Code: {err.getcode()}')
            print(f'Target URL: {imageUrl}' )
            print('========================')
            print('\n')
            return False
        except UnicodeEncodeError as unierror:
            print( imageUrl )
            print('\n')
            print('========================')
            print(f'Error Type: URL Parse Error')
            print(f'Target URL: {imageUrl}' )
            print('========================')
            print('\n')
            return False
        except ConnectionResetError as ConnectionError:
            print('\n')
            print('========================')
            print(f'Error Type: Connection Error')
            print(f'Target URL: {imageUrl}' )
            print('========================')
            print('\n')
            return False
        
        return True

    def getImageByTags( self, keyword ):
        processedKeyword = keyword.lower().replace(' ', '%20')
        folderName = keyword.lower().replace(' ', '-')
        searchUrl = f'https://pexels.com/search/{processedKeyword}/'
        self.driver.get( searchUrl )
        self.infiniteScroll( self.ScrollTimeout, self.ScrollCounte )
        
        # Create Download Folder if no Exist
        if not os.path.exists( f'{self.downloadPath}/{folderName}' ):
            os.makedirs( f'{self.downloadPath}/{folderName}' )

        imagesList = self.driver.find_elements_by_css_selector('div.search__grid .photos article.photo-item a.photo-item__link > img')
        for index, image in enumerate( imagesList ):
            processedLinkSlug = image.find_element_by_xpath("..").get_attribute('href').split('/')[-2]
            
            # Check Image is Processed or Not
            if ( self.isImageProcessed( processedLinkSlug ) ):
                cleanImageUrl = image.get_attribute('data-big-src').split('?')[0]
                
                # Insert Item to DB After Download
                if self.saveImage( cleanImageUrl, f'{self.downloadPath}/{folderName}/{folderName}-{ str(index + 1) }.jpeg' ):
                    self.insertItemtoDatabase( processedLinkSlug )

    def isImageProcessed( self, linkSlug ):
        database_record = self.dataBaseConnection.execute("""SELECT link_slug FROM pexels WHERE link_slug = (?) LIMIT 1""", (linkSlug,)).fetchone()
        return not database_record

    def insertItemtoDatabase( self, linkSlug ):
        try:
            self.dataBaseConnection.execute("""INSERT INTO pexels (link_slug) VALUES (?)""", (linkSlug,))
            self.dataBaseConnection.commit()
        except sqlite3.Error as error:
            print(error)
            pass

    def closeDriver( self ):
        self.dataBaseConnection.close()
        self.driver.close()
        self.driver.quit()

def main():
    arguments = docopt(__doc__, version='v1.0')
    folderName = str( arguments['--folder-name '] ) if arguments['--folder-name '] else 'downloads'
    ScrollTimeout = int( arguments['--load-time'] ) if arguments['--load-time'] else 5
    ScrollCounte = int( arguments['--page-count'] ) if arguments['--page-count'] else 0
    showBrowser = arguments['--show-browser']
    keyword = arguments['<keyword>']


    Pexels = PexelsCrawler( showBrowser=showBrowser, ScrollTimeout=ScrollTimeout, ScrollCounte=ScrollCounte, folderName=folderName )

    if ( arguments['search'] ):
        Pexels.getImageByTags( keyword=keyword )
    else:
        print(Fore.RED + "You Should Enter The Search Keyword!")
        print(Style.RESET_ALL)
    
    Pexels.closeDriver()


# if __name__ == "__main__":
    # main()