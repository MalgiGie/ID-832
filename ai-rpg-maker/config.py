import logging
import os
from datetime import datetime

MODEL = "gpt-4o-mini"

if "ROOT_DIRECTORY" not in os.environ:
    CURRENT_TIME = datetime.now().strftime("%Y-%m-%d_%H-%M")
    ROOT_DIRECTORY = os.path.join(os.getcwd(), "data", MODEL, CURRENT_TIME)
    os.makedirs(ROOT_DIRECTORY, exist_ok=True)
    os.environ["ROOT_DIRECTORY"] = ROOT_DIRECTORY
else:
    ROOT_DIRECTORY = os.environ["ROOT_DIRECTORY"]

CLASSES = ["MAG", "ŁUCZNIK", "WOJOWNIK"]

# TOKENS
HERO_TOKENS = 12000
BASIC_NPC_TOKENS = 5000
EPIC_NPC_TOKENS = 12000
QUESTS_TOKENS = 12000
WORLD_TOKENS = 7500
# TEMPERATURES
HERO_TEMPERATURE = 0.85
BASIC_NPC_TEMPERATURE=0.85
EPIC_TEMPERATURE=0.85
QUESTS_TEMPERATURE = 0.8
WORLD_TEMPERATURE = 0.85

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
