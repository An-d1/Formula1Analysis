import sys
sys.path.append('../scripts')   # allows pysthon to find scripts/ folder

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from timple.timedelta import strftimedelta

import fastf1
import fastf1.plotting
from fastf1.core import Laps

# Enable Matplotlib patches for plotting timedelta values
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None)

def plot_the_final_ranking(session):
    laps = session.laps.pick_quicklaps() #Getting only the quickest laps for each driver as they are the most relevant, (excluding ones like under security car or entering and exiting pits)
    results = session.results.copy()

    drivers = results['Abbreviation']
    teams = results['TeamName']
    positions = results['Position'].astype(int)

    colors = [fastf1.plotting.get_team_color(team, session=session) for team in teams]

    fig, ax = plt.subplots(figsize=(8, 5))

    # horizontal bars, all bars same length since this servbes to only show the final position
    ax.barh(drivers, [1]*len(drivers), color=colors)

    # invert y axis so P1 is on top
    ax.invert_yaxis()

    # remove x axis and unnecessary ticks
    ax.set_xticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_xlim(0, 1.5)
    ax.set_title(f"{session.event['EventName']} {session.event['EventDate'].year} {session.name} Results:", fontsize=13, fontweight='bold')

    # add position labels next to each driver
    for i, pos in enumerate(positions):
        ax.text(1.05, i, f"P{pos}", va='center', fontsize=10)

    # create one legend entry per team
    unique_teams = teams.unique() # need to get the fastest_laps from the other method
    legend_patches = []

    for team in unique_teams:
        color = fastf1.plotting.get_team_color(team,session=session)
        patch = mpatches.Patch(color=color, label=team)
        legend_patches.append(patch)

    # add legend to plot
    ax.legend(handles=legend_patches,
            loc='upper right',
            frameon=False,
            labelcolor='black',
            title='Teams',
            title_fontsize=10,
            fontsize=8)
    # clean style
    ax.set_frame_on(False)
    plt.tight_layout()
    plt.show()