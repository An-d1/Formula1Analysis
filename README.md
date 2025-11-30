Formula 1 Race Analysis Dashboard

This project provides a streamlined analytical environment for exploring Formula 1 race data using the FastF1 API.
It includes Python scripts and a Streamlit dashboard that allow users to load any race (from 2018 onward) and visualize:

- Fastest laps and time deltas

- Driver position changes throughout the race

- Tyre compounds, stints, and degradation patterns

- Final race classification using official team colours

- The project focuses on efficient data retrieval, cleaning, manipulation, and clear visualization of key race metrics.

Requirements and Installation

To run the project, the following are required:

- Python 3.10 or later

- Required libraries listed in requirements.txt

Installation steps:

1. Clone the repository:

git clone https://github.com/An-d1/Formula1Analysis
cd Formula1Analysis

2. Install dependencies:
pip install -r requirements.txt

3. Run the Streamlit dashboard:
streamlit run scripts/app.py

FastF1 caching is automatically enabled when loading race sessions.

Author

Andis Bara
MSc student Data Science for Economics and Health
University of Milan