# -*- coding: utf-8 -*- 

import sys
import os
from utilities import twotoone, toOpenSubtitles_two, log
from pn_utilities import OSDBServer
import xbmc
import urllib
import threading

_ = sys.modules[ "__main__" ].__language__      


def search_subtitles( file_original_path, title, tvshow, year, season, episode, set_temp, rar, lang1, lang2, lang3, stack ): #standard input     
  ok = False
  msg = ""
  osdb_server = OSDBServer()
  osdb_server.create()    
  subtitles_list = []
  file_size = ""
  hashTry = ""
  language1 = twotoone(toOpenSubtitles_two(lang1))
  language2 = twotoone(toOpenSubtitles_two(lang2))
  language3 = twotoone(toOpenSubtitles_two(lang3))  
  if set_temp : 
    hash_search = False
    file_size = "000000000"
    hashTry = "000000000000"
  else:
    try:
      file_size, SubHash   = xbmc.subHashAndFileSize(file_original_path)
      log( __name__ ,"xbmc module hash and size")
      hash_search = True
    except:  
      file_size = ""
      SubHash = ""
      hash_search = False
  
  if file_size != "" and SubHash != "":
    log( __name__ ,"File Size [%s]" % file_size )
    log( __name__ ,"File Hash [%s]" % SubHash)
  if hash_search :
    log( __name__ ,"Search for [%s] by hash" % (os.path.basename( file_original_path ),))
    subtitles_list, session_id = osdb_server.searchsubtitles_pod( SubHash ,language1, language2, language3, stack)
  if not subtitles_list:
    log( __name__ ,"Search for [%s] by name" % (os.path.basename( file_original_path ),))
    subtitles_list = osdb_server.searchsubtitlesbyname_pod( title, tvshow, season, episode, language1, language2, language3, year, stack )
  return subtitles_list, "", "" #standard output

def download_subtitles (subtitles_list, pos, zip_subs, tmp_sub_dir, sub_folder, session_id): #standard input
  pod_url_parse = urllib.urlopen(subtitles_list[pos][ "link" ]).read()
  url = "http://www.podnapisi.net/ppodnapisi/download/i/%s" % (pod_url_parse.split("/ppodnapisi/download/i/")[1].split('" title="')[0])  
  local_file = open(zip_subs, "w" + "b")
  f = urllib.urlopen(url)
  local_file.write(f.read())
  local_file.close()
  
  language = subtitles_list[pos][ "language_name" ]
  return True,language, "" #standard output
    