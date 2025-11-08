import logging
import os
from datetime import datetime

MODEL = "gpt-5"

os.environ["ROOT_DIRECTORY"] = "2025-11-08_19-11"

if "ROOT_DIRECTORY" not in os.environ:
    CURRENT_TIME = datetime.now().strftime("%Y-%m-%d_%H-%M")
    ROOT_DIRECTORY = os.path.join(os.getcwd(), "data", MODEL, CURRENT_TIME)
    os.makedirs(ROOT_DIRECTORY, exist_ok=True)
    os.environ["ROOT_DIRECTORY"] = ROOT_DIRECTORY
else:
    ROOT_DIRECTORY = os.environ["ROOT_DIRECTORY"]

CLASSES = ["MAG", "ŁUCZNIK", "WOJOWNIK"]

# TOKENS
HERO_TOKENS = 16000
BASIC_NPC_TOKENS = 20000
EPIC_NPC_TOKENS = 35000
QUESTS_TOKENS = 30000
WORLD_TOKENS = 128000
# TEMPERATURES
HERO_TEMPERATURE = 1
BASIC_NPC_TEMPERATURE=1
EPIC_TEMPERATURE=1
QUESTS_TEMPERATURE = 1
WORLD_TEMPERATURE = 1

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
