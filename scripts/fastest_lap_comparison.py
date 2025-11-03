import sys
sys.path.append('../scripts')   # allows pysthon to find scripts/ folder

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

import fastf1
import fastf1.plotting
from fastf1.core import Laps

# I use this file to calculate the delta time of all drivers compared to the fastest one for either qualification session or for hte race session

# Enable Matplotlib patches for plotting timedelta values
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None)

# this method doesn't care about the fastf1.session as it will be provided when needed as a parameter by the cusotm method on fetch_data
# it gets all the drivers laps on the session and simply loops through them to get each ones fastest lap 
def get_all_drivers_fastest_lap(session):
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

    return fastest_laps # I return the list with all the fastest_laps for each driver

def calculate_drivers_delta_time_compared_to_pole(session):
    fastest_laps = get_all_drivers_fastest_lap(session) #getting the list from the method created above

    pole_lap = fastest_laps.pick_fastest() # returns the fastest driver, so we can calculate the difference for the others
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime'] #calculates each drivers delta based on the fastest driver +..
    
    return (pole_lap, fastest_laps)

# This method can also be used to compare all the drivers fastes lap times 
def plot_the_final_time_ranking(session):
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
        ax.text(delta + pd.Timedelta(seconds=0.02), #offsets the label so they dotn overlap
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

    plt.show()