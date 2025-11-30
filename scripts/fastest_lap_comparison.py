import sys
sys.path.append('../scripts')   # allows pysthon to find scripts/ folder

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

import fastf1
import fastf1.plotting
from fastf1.core import Laps

# I use this file to calculate the delta time of all drivers compared to the fastest one 
# for either qualification session or for the race session

# Enable Matplotlib patches for plotting timedelta values
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None)

def get_driver_consistency(session):
    """
    Calculates the standard deviation of lap times for each driver using NumPy.
    A lower Standard Deviation (std) means the driver was more consistent.
    
    Parameters
    ----------
    session : fastf1.core.Session
        The loaded session data.
        
    Returns
    -------
    consistency_df : pandas.DataFrame
        Dataframe containing Driver and their lap time Standard Deviation (Consistency).
    """
    drivers = pd.unique(session.laps['Driver'])
    consistency_data = []

    for drv in drivers:
        # Gets only accurate racing laps (excluding pit-stop laps and Safety Car)
        driver_laps = session.laps.pick_drivers(drv).pick_quicklaps().pick_accurate()
        
        if len(driver_laps) > 2:
            lap_times_sec = driver_laps['LapTime'].dt.total_seconds()
            
            # using numpy to calculate standard deviation
            consistency_score = np.std(lap_times_sec)
            
            consistency_data.append({
                'Driver': drv,
                'Consistency (Std Dev) [s]': round(consistency_score, 3)
            })

    return pd.DataFrame(consistency_data).sort_values(by='Consistency (Std Dev) [s]')

# this method doesn't care about the fastf1.session as it will be provided when needed as a parameter by the cusotm method on fetch_data
def get_all_drivers_fastest_lap(session):
    """
    Return the fastest lap for each driver in a given FastF1 session.

    The function extracts all drivers present in the session, selects
    their fastest lap individually, and returns a FastF1 `Laps` object
    containing one lap per driver, sorted by lap time.

    Parameters
    ----------
    session : fastf1.core.Session
        The loaded FastF1 session (race, qualifying, practice etc.)
        containing telemetry and lap data.

    Returns
    -------
    fastest_laps : fastf1.core.Laps
        A `Laps` object where each row corresponds to the fastest lap
        of a driver, sorted in ascending order of lap time.
    """
    drivers = pd.unique(session.laps['Driver'])
    print(drivers)

    list_fastest_laps = list()

    # loop to get each drivers fastest lap and append them to the list
    for drv in drivers:
        current_drivers_fastest_lap = session.laps.pick_drivers(drv).pick_fastest()
        if current_drivers_fastest_lap is not None: # to check if the lap time is not 'NaT' which is the equivalend of NaN in pandas time seris
            list_fastest_laps.append(current_drivers_fastest_lap)
    
    # reconstructs the list into a proper fastf1 pandas data frame and sorts the values in descending order by laptime, dropping the oringinal indexes
    fastest_laps = Laps(list_fastest_laps) \
    .sort_values(by='LapTime') \
    .reset_index(drop=True)    

    return fastest_laps 

def calculate_drivers_delta_time_compared_to_pole(session):
    """
    Compute the lap-time delta of each driver's fastest lap relative
    to the overall fastest lap ("pole lap") of the session.

    Parameters
    ----------
    session : fastf1.core.Session
        The loaded FastF1 session containing all laps.

    Returns
    -------
    pole_lap : pandas.Series
        The fastest lap in the session (the reference lap).
    fastest_laps : fastf1.core.Laps
        A `Laps` object where each driver's fastest lap is included,
        with an additional column `LapTimeDelta` storing the time
        difference to `pole_lap`.
    """
    fastest_laps = get_all_drivers_fastest_lap(session) #getting the list from the method created above

    pole_lap = fastest_laps.pick_fastest() # returns the fastest driver, so we can calculate the difference for the others
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime'] #calculates each drivers delta based on the fastest driver +..
    
    return (pole_lap, fastest_laps)

# This method can also be used to compare all the drivers fastes lap times 
def plot_the_final_time_ranking(session):
    """
    Plot a horizontal bar chart showing each driver's fastest lap
    delta relative to the session's fastest lap.

    The plot uses team colors, displays delta times in seconds next
    to each bar, and includes a legend listing all teams. This
    function is intended for use in the Streamlit dashboard.

    Parameters
    ----------
    session : fastf1.core.Session
        The FastF1 session from which lap times and team information
        are extracted.

    Returns
    -------
    fastest_driver : str
        The full name of the fastest driver in the session.
    fig : matplotlib.figure.Figure
        The generated Matplotlib figure containing the ranking plot.
    """
    #Just creates a list of team colors for the e plot
    team_colors = list()

    pole_lap, fastest_laps = calculate_drivers_delta_time_compared_to_pole(session=session) # now i get the same fastest_laps list, but from the second method 

    for index, lap in fastest_laps.iterlaps():
        color = fastf1.plotting.get_team_color(lap['Team'], session=session)
        team_colors.append(color)

    #as it contains the properly modified one

    fig, ax = plt.subplots(figsize=(10, 5), facecolor='black')
    ax.set_facecolor('#111111')

    ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'],
            color=team_colors, edgecolor='grey')
    ax.set_yticks(fastest_laps.index)
    ax.set_yticklabels(fastest_laps['Driver'], color='White')

    ax.set_title(f" {session.event['EventDate'].year} {session.event['EventName']} {session.name} \n Fastest Time: {pole_lap.Driver} -- {str(fastest_laps['LapTime'].iloc[0]).split()[-1]}", #split is used to remove the '0 days part..'
                color='white', 
                pad=15)
    ax.set_xlabel("Lap Time Delta (seconds)", color='white')

    # To add seconds on the side of each drivers time for more readibility
    for i, delta in enumerate(fastest_laps['LapTimeDelta']):
        ax.text(delta + pd.Timedelta(seconds=0.02), #offsets the label so they dont overlap
                i,
                f"+{delta.total_seconds():.3f}s",
                va='center',
                color='white',
                fontsize=8)

    # iverts to show fastest at the top
    ax.invert_yaxis()

    # draw vertical lines behind the bars
    ax.grid(which='major', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.3, alpha=0.3)

    # draw the lines in between major lines
    ax.minorticks_on()

    # Keep grid behind bars
    ax.set_axisbelow(True)

    # create one legend entry per team
    unique_teams = fastest_laps['Team'].unique()
    legend_patches = []

    for team in unique_teams:
        color = fastf1.plotting.get_team_color(team,session=session)
        patch = mpatches.Patch(color=color, label=team)
        legend_patches.append(patch)

    # add legend to plot
    legend = ax.legend(handles=legend_patches,
          loc='upper right',
          frameon=False,
          labelcolor='white',
          title='Teams',
          fontsize=8,)

    # Simply to set the legend title white and fontsize
    legend.get_title().set_color('white') 
    legend.get_title().set_fontsize(10)

    full_name = session.results.loc[
    session.results['Abbreviation'] == pole_lap['Driver'], 'FullName'
    ].iloc[0]

    fastest_driver = full_name #this is only used to be returned to the front for written analysis
    return (fastest_driver, fig)