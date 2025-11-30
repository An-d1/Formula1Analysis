import fastf1
import matplotlib.pyplot as plt

def prepare_driver_data_for_plotting(session):
    """
    Extract and prepare car telemetry for the two fastest drivers in the session.

    This function identifies the two drivers with the fastest lap times,
    retrieves their telemetry (including speed and distance), extracts
    their team color, and formats labels for plotting. It also computes the
    minimum and maximum speed values observed across both drivers, which
    are useful for setting plot limits.

    Parameters
    ----------
    session : fastf1.core.Session
        A fully loaded FastF1 session containing lap data, results,
        and telemetry information.

    Returns
    -------
    the_fastest_of_two : str
        Full name of the fastest driver among the top two.
    the_second_driver : str
        Full name of the second-fastest driver.
    driver_data : dict
        A dictionary mapping each driver's abbreviation to a dictionary
        containing:
            - 'car' : pandas.DataFrame
                Telemetry with speed and distance columns.
            - 'color' : str
                The team color for plotting.
            - 'label' : str
                Plot label including driver name and lap time.
    vmins : list of float
        Minimum speed values observed for each of the two drivers.
    vmaxs : list of float
        Maximum speed values observed for each of the two drivers.
    """
    laps_clean = session.laps[session.laps['LapTime'].notna()]

    # gets only the data the 2 fastest driverss to later fetch their data 
    top2 = (laps_clean.groupby('Driver')['LapTime']
                    .min()
                    .sort_values()
                    .head(2))
    drivers = list(top2.index)  

    # prepare the dictionary for both drivers
    driver_data = {}
    vmins, vmaxs = [], [] #used for plot range of the minspeed and max speed

    for drv in drivers:
        lap = session.laps.pick_driver(drv).pick_fastest()
        car = lap.get_car_data().add_distance() #get car data and the distance
        color = fastf1.plotting.get_team_color(lap['Team'], session=session) 
        label = f"{drv}  ({str(lap['LapTime']).split()[-1]})"
        driver_data[drv] = {'car': car, 'color': color, 'label': label}
        vmins.append(car['Speed'].min())
        vmaxs.append(car['Speed'].max())

    the_fastest_of_two = session.results.loc[
    session.results['Abbreviation'] == drivers[0], 'FullName'
    ].iloc[0]

    the_second_driver = session.results.loc[
    session.results['Abbreviation'] == drivers[1], 'FullName'
    ].iloc[0]


    return (the_fastest_of_two, the_second_driver, driver_data, vmins, vmaxs)
    
def plot_2_fastest_laps_comparison_side_by_side(session):
    """
    Plot the speed profiles of the two fastest drivers' best laps side by side.

    This function generates a line plot comparing the speed of the two fastest
    drivers along the lap distance. Corner positions are marked with vertical
    dotted lines using the circuit information from the session. The plot shows
    where each driver is faster or slower and highlights braking, acceleration,
    and top-speed sections.

    Parameters
    ----------
    session : fastf1.core.Session
        A fully loaded FastF1 session containing laps, telemetry,
        and circuit information.

    Returns
    -------
    the_fastest_of_two : str
        Full name of the fastest driver.
    the_second_driver : str
        Full name of the second-fastest driver.
    fig : matplotlib.figure.Figure
        The Matplotlib figure object containing the comparison plot.
    """
    the_fastest_of_two, the_second_driver, driver_data, vmins, vmaxs = prepare_driver_data_for_plotting(session=session)

    # Corner info
    circuit_info = session.get_circuit_info()

    # plot
    fig, ax = plt.subplots(figsize=(10, 5))

    # plot both lines
    for drv, info in driver_data.items():
        car = info['car']
        ax.plot(car['Distance'], car['Speed'],
                color=info['color'], linewidth=1.8, label=info['label'])

    # Vertical dotted lines for corners
    v_min = min(vmins)
    v_max = max(vmaxs)
    ax.vlines(x=circuit_info.corners['Distance'],
            ymin=v_min-20, ymax=v_max+20,
            linestyles='dotted', colors='grey')


    # Labels, legend, limits
    ax.set_xlabel('Distance along track (m)')
    ax.set_ylabel('Speed in km/h')
    ax.legend(title='Driver (best lap)')
    ax.set_ylim([v_min - 40, v_max + 20])

    return (the_fastest_of_two, the_second_driver, fig)