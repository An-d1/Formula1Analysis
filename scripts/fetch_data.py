import fastf1
from pathlib import Path 

def setup_fastf1_cache():
   # Gets path to this file
    script_path = Path(__file__).resolve()
    
    # gets the project root (parent of scripts)
    project_root = script_path.parent.parent
    
    # define cache path from the root
    cache_dir = project_root / "external_data" / "fastf1"
    
    # enable the cache to store the data locally
    fastf1.Cache.enable_cache(cache_dir)

def load_session(year: int, gp: str, session_type: str = "R"): #session type set to race by default 'R'
    #dynamically fetch and load an f1 session from fastf1

    setup_fastf1_cache()
    session = fastf1.get_session(year, gp, session_type)
    session.load()
    return session



    
