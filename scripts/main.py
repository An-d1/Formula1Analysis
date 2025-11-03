from fetch_data import load_session
import fastest_lap_comparison as fastest_lap_comparison

import fastf1

# Quali plot starts here / But these methods can also be used to compare all the drivers fastest lap
session = load_session(2020, "Russia", "R")

fastest_lap_comparison.get_all_drivers_fastest_lap(session=session)
fastest_lap_comparison.calculate_drivers_delta_time_compared_to_pole(session=session)
fastest_lap_comparison.plot_the_final_quali_ranking(session=session)
# quali ends here

