import logging
import os
import uuid
from datetime import datetime

MODEL = "gpt-5"


if "ROOT_DIRECTORY" not in os.environ:
    unique_id = str(uuid.uuid4())
    ROOT_DIRECTORY = os.path.join(os.getcwd(), "data", MODEL, unique_id)
    os.makedirs(ROOT_DIRECTORY, exist_ok=True)
    os.environ["ROOT_DIRECTORY"] = ROOT_DIRECTORY
else:
    ROOT_DIRECTORY = os.environ["ROOT_DIRECTORY"]

CLASSES = ["MAG", "ARCHER", "WARRIOR", "PALADIN", "ROGUE"]
#CLASSES = ["MAG", "ŁUCZNIK", "WOJOWNIK", "PALADYN", "SZELMA"]

HERO_TOKENS = 32768
BASIC_NPC_TOKENS = 32768
EPIC_NPC_TOKENS = 32768
QUESTS_TOKENS = 32768
WORLD_TOKENS = 32768

# TEMPERATURES
HERO_TEMPERATURE = 1
BASIC_NPC_TEMPERATURE= 1
EPIC_TEMPERATURE= 1
QUESTS_TEMPERATURE = 1
WORLD_TEMPERATURE = 1

LANGUAGE = "EN"

PG_MOTD = r"""

,-.----.                                              
\    /  \    ,----..                                  
|   :    \  /   /   \                                 
|   |  .\ :|   :     :                                
.   :  |: |.   |  ;. /                                
|   |   \ :.   ; /--`                                 
|   : .   /;   | ;  __                                
;   | |`-' |   : |.' .'                               
|   | ;    .   | '_.' :                               
:   ' |    '   ; : \  |                               
:   : :    '   | '/  .'                               
|   | :    |   :    /                                 
`---'.|     \   \ .'                          ,----,. 
  `---`      `---`                          ,'   ,' | 
      ,----,     ,----..        ,----,    ,'   .'   | 
    .'   .' \   /   /   \     .'   .' \ ,----.'    .' 
  ,----,'    | /   .     :  ,----,'    ||    |   .'   
  |    :  .  ;.   /   ;.  \ |    :  .  ;:    :  |--,  
  ;    |.'  /.   ;   /  ` ; ;    |.'  / :    |  ;.' \ 
  `----'/  ; ;   |  ; \ ; | `----'/  ;  |    |      | 
    /  ;  /  |   :  | ; | '   /  ;  /   `----'.'\   ; 
   ;  /  /-, .   |  ' ' ' :  ;  /  /-,    __  \  .  | 
  /  /  /.`| '   ;  \; /  | /  /  /.`|  /   /\/  /  : 
./__;      :  \   \  ',  /./__;      : / ,,/  ',-   . 
|   :    .'    ;   :    / |   :    .'  \ ''\       ;  
;   | .'        \   \ .'  ;   | .'      \   \    .'   
`---'            `---`    `---'          `--`-,-'     

"""

def log_config_vars():
    for name, value in globals().items():
        if name.isupper():
            logging.info(f"{name} = {value}")
