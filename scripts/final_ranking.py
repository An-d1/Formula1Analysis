import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import fastf1
import fastf1.plotting

fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None)

def plot_the_final_ranking(session):
    results = session.results.copy()

    # turns numeric position for sorting, and looks for not valid data like DNF(did not finish) and converts them to NaN
    results['PosNum'] = pd.to_numeric(results['Position'], errors='coerce')

    # sorts by classified position; put NaNs at the end
    results = results.sort_values(['PosNum', 'Abbreviation'], na_position='last').reset_index(drop=True)

    drivers = results['Abbreviation']
    teams = results['TeamName'].fillna('Unknown')

    # positions for display: show P# for classified, otherwise the raw label (e.g., DNF/DSQ/NC)
    pos_display = results.apply(
        lambda r: f"P{int(r['PosNum'])}" if pd.notna(r['PosNum']) else (str(r['Position']) or "NC"),
        axis=1
    )

    colors = [fastf1.plotting.get_team_color(team, session=session) for team in teams]

    fig, ax = plt.subplots(figsize=(8, 5))

    # draw equal-length bars, one per driver, in sorted order
    y = range(len(drivers))
    ax.barh(y, [1]*len(drivers), color=colors)

    # label the y-axis with driver abbreviations
    ax.set_yticks(y)
    ax.set_yticklabels(drivers)

    # invert so P1 is at the top
    ax.invert_yaxis()

    # clean axes
    ax.set_xticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_xlim(0, 1.5)
    ax.set_title(f"{session.event['EventName']} {session.event['EventDate'].year} {session.name} Results:", 
                 fontsize=13, fontweight='bold')

    # position labels at the right side
    for i, lbl in enumerate(pos_display):
        ax.text(1.05, i, lbl, va='center', fontsize=10)

    # legend (one entry per team)
    legend_patches = []
    for team in teams.unique():
        color = fastf1.plotting.get_team_color(team, session=session)
        legend_patches.append(mpatches.Patch(color=color, label=team))

    ax.legend(handles=legend_patches,
              loc='upper right',
              frameon=False,
              title='Teams',
              title_fontsize=10,
              fontsize=8)

    ax.set_frame_on(False)
    plt.tight_layout()
    return fig
