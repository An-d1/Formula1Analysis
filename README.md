Formula 1 Race Analysis Dashboard

This project provides a complete analytical framework for exploring Formula 1 race data using the FastF1 API.
It includes Python modules, Jupyter notebooks, scientific computations, and an interactive Streamlit dashboard that allows users to explore any Formula 1 race from 2018 onward.

The project focuses on data retrieval, cleaning, manipulation, statistical analysis, and professional data visualization.

1. Features

- Dynamic race session loading based on year and Grand Prix.

- Analysis of fastest laps and time deltas between drivers.

- Visualization of driver position evolution throughout a race.

- Tyre compound and stint-based performance analysis.

- Final race classification using official team colours.

- Interactive dashboard built with Streamlit.

- Modular and scalable code structure suitable for further extensions.

2. Installation

- Clone the repository:

git clone https://github.com/An-d1/Formula1Analysis
cd Formula1Analysis

- Install dependencies:

pip install -r requirements.txt

- FastF1 caching is automatically enabled upon executing any data-loading function.

3. Running the Dashboard

- To launch the Streamlit application:

streamlit run scripts/app.py

The dashboard allows users to:

- Select a season.

- Select a race from the chosen season.

- Trigger several analyses, including:

- Fastest lap comparison.

- Tyre degradation and stint analysis.

- Driver position evolution across laps.

- Final race classification.

- Comparison of the two fastest drivers.

All plots and interpretations are generated dynamically.

5. Analytical Components
5.1 Fastest Lap Comparison

- Identification of each driver's fastest lap.

- Computation of deltas relative to the session’s fastest lap.

- Visualization of lap-time differences using timedelta-aware plotting.

5.2 Position Evolution Across the Race

- Lap-by-lap tracking of driver positions.

- Visualization of race dynamics such as overtakes and pit stops.

5.3 Tyre Strategy and Degradation

- Analysis of compound usage and stint durations.

- Lap time versus tyre age modelling.

- Degradation curve visualisation.

5.4 Final Race Classification

- Summary of finishing positions.

- Use of official team colours for visual clarity.

5.5 Best-Lap Comparison Between Two Drivers

- Direct comparison of their fastest laps.

6. Data Source

- Data is retrieved through the FastF1 Python API, which provides:

- Official Formula 1 lap timing data.

- Telemetry and sector information (when available).

- Tyre compound and stint metadata.

- Session-level metadata across recent seasons.

- FastF1 documentation: https://theoehrly.github.io/Fast-F1/

7. Author:
Andis Bara
MSc Data Science for Economics and Health
University of Milan