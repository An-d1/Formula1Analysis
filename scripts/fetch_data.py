import fastf1
from pathlib import Path 

def setup_fastf1_cache():
    """
    Configure and enable the FastF1 cache for the project.

    This function automatically determines the root directory of the
    project based on the location of the current script, then enables
    the FastF1 cache inside `external_data/fastf1`. FastF1 will use
    this directory to store downloaded session data locally, improving
    performance and allowing offline re-use.

    Returns
    -------
    None
    """
   # Gets path to this file
    script_path = Path(__file__).resolve()
    
    # gets the project root (parent of scripts)
    project_root = script_path.parent.parent
    
    # define cache path from the root
    cache_dir = project_root / "external_data" / "fastf1"
    
    # enable the cache to store the data locally
    fastf1.Cache.enable_cache(cache_dir)

def load_session(year: int, gp: str, session_type: str): 
    """
    Load a Formula 1 session using FastF1.

    This function enables the cache (if not already enabled), retrieves
    the requested session (race, qualifying, practice, etc.), loads all
    available data, and returns the fully initialized FastF1 session
    object.

    Parameters
    ----------
    year : int
        The year of the event (e.g., 2024).
    gp : str
        The Grand Prix name as recognized by FastF1 
        (e.g., "Monza", "Austria", "Bahrain").
    session_type : str
        Session code such as:
        - "R" for Race
        - "Q" for Qualifying
        - "FP1", "FP2", "FP3" for free practice

    Returns
    -------
    session : fastf1.core.Session
        The fully loaded FastF1 session containing laps, telemetry,
        results, weather data, and other session metadata.
    """
    setup_fastf1_cache()
    session = fastf1.get_session(year, gp, session_type)
    session.load()
    return session



    
