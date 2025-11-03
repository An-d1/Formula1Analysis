import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from timple.timedelta import strftimedelta

import fastf1
import fastf1.plotting
from fastf1.core import Laps

def plot_sessions_tyre_compounds_and_stints(session):
    laps = session.laps.pick_quicklaps() #Getting only the valid laps for each driver as they are the most relevant, (excluding ones like under security car or entering and exiting pits)

    laps_data = laps[['Driver', 'LapTime', 'Compound', 'Stint']].copy()
    laps_data['LapTime'] = laps_data['LapTime'].dt.total_seconds() # convert laptimes in seconds

    #just a dictionary with string as key value pairs to be passed to the scatterplot marker prop
    marker_map = {'HARD': 'o', 'MEDIUM': '+', 'SOFT': '^'} 
    laps_data['TyreMarker'] = laps_data['Compound'].map(marker_map) #marks every occurence of compunds into the value pair specified on the dictionary above

    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(10, 5))

    for compound, marker in marker_map.items():
        subset = laps_data[laps_data['Compound'] == compound] # filter based on the current compound on the loop 
        sc = ax.scatter(
            subset['Driver'], 
            subset['LapTime'],
            c=subset['Stint'],  # color by stint number
            cmap='plasma',  
            marker=marker, # shape by tyre compound
            alpha=1,
            label=compound
        )

    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("Stint Number")

    ax.set_xlabel("Driver")
    ax.set_ylabel("Lap Time (s)")
    ax.set_title("Lap Times by Driver, Tyre Compound, and Stint")

    ax.legend(title="Tyre Compound")

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

