import fastf1
import matplotlib.pyplot as plt

def positions_changed_plot(session):
    """
    Plot the evolution of each driver's position over the course of a race.

    This function generates a line plot where each driver is represented
    by a line styled according to FastF1's driver color and line style.
    The plot shows how each driver's race position changed lap by lap,
    making it easy to visualize overtakes, consistency, and trends in
    race performance.

    Parameters
    ----------
    session : fastf1.core.Session
        A fully loaded FastF1 race session containing lap-by-lap
        position data for all drivers.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The Matplotlib figure containing the position-change plot,
        suitable for display or for use in Streamlit.
    """
    
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.grid(False)

    #styling and title
    ax.set_title("Positions changed during the race")

    # for each driver i get the first 3 letters by using the first lap, and then i get their color and plot their position over the number of laps
    for drv in session.drivers:
        drv_laps = session.laps.pick_drivers(drv)

        abbrevation = drv_laps['Driver'].iloc[0]
        style = fastf1.plotting.get_driver_style(identifier=abbrevation, #this returns a dictionary with the drivers color and line
                                                style=['color', 'linestyle'],
                                                session=session)

        ax.plot(drv_laps['LapNumber'], drv_laps['Position'],
                label=abbrevation, **style)
        
    # Invert the axis and set labels
    ax.set_ylim([20.5, 0.5]) # also 20.5 and 0.5 so it has some padding
    ax.set_yticks([1, 5, 10, 15, 20])
    ax.set_xlabel('Lap')
    ax.set_ylabel('Position')

    # Legend outside the box
    ax.legend(bbox_to_anchor=(1.0, 1.02))
    plt.tight_layout()

    return fig