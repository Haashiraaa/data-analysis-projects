```markdown
# Weather Data Visualizer

A small Python script that reads a CSV file of weather observations and visualizes daily high and low temperatures with Matplotlib.

This README documents the current version of the project (no refactor). It describes how the existing `weather_data.py` expects the CSV to be laid out and how to run the script.

## Features (current version)
- Parses a CSV file using Python's `csv` module.
- Extracts dates, daily high and low temperatures, and station name (index-based).
- Plots highs and lows with Matplotlib and fills the area between them.
- Prompts the user to either view the plot interactively or save it to an image file.
- Uses `icecream` (`ic`) for optional debug prints and a `saver.save_plot` helper for saving.

## Clone the repository
Clone via HTTPS:
```
git clone https://github.com/Haashiraaa/weather-data-visualizer.git<br>
cd weather-data-visualizer
```

Clone via SSH:
```
git clone git@github.com:Haashiraaa/weather-data-visualizer.git<br>
cd weather-data-visualizer
```

To check out the exact commit referenced in this README (optional):
```
git fetch --all<br>
git checkout 0cccda1dc4f4928b25e1cd2594b265da14f59285
```
(or clone normally and use `git checkout <commit-sha>` after `cd`-ing into the repo.)

## Requirements
- Python 3.8+
- matplotlib
- icecream
- (local) `saver.py` module in the repo that provides `save_plot(fig, filename)`

Install the main packages with pip:
```
pip install matplotlib icecream
```


```
```

## Expected CSV format (as used by the current script)
The script currently uses index-based column access. Make sure your CSV matches these expectations:

- Column index 2: DATE in format `YYYY-MM-DD` (this is parsed with `datetime.strptime(..., '%Y-%m-%d')`)
- Column index 4: High temperature (integer)
- Column index 5: Low temperature (integer)
- Column index 1: Station name (string — used to build the plot title)

Example (header and one example row; adjust to your real file):
```
id,STATION,DATE,extra,TMAX,TMIN
123,MY_STATION,2024-01-01,.,72,45
```

The repository example file name used by the script is `4150697.csv` (hard-coded in `weather_data.py`). Either rename your CSV file to that name or update the file path in the script.

## How to run
1. Ensure you've cloned the repository and are in its root directory.
2. Place your CSV file (matching the expected format above) in the same directory as `weather_data.py` or update the file path in the script.
3. Ensure `saver.py` is present and provides a `save_plot(fig, filename)` function (the script imports it).
4. Run:
```
python weather_data.py
```
5. The script will prompt:
```
Would you like to view or save the plot? (v/s):
```
- Type `v` to open an interactive Matplotlib window showing the plot.
- Type `s` to call `save_plot(fig, "weather_data.png")` (ensure `saver.py` handles the file save).

## Debugging
- `DEBUG` is a boolean in `weather_data.py`. When `DEBUG = True`, the script enables `icecream` debug output to print skipped/missing-data details.
- By default `DEBUG = False` and debug prints are disabled.

## Known caveats (current version)
- The CSV path is hard-coded to `4150697.csv`. The script will raise an error if the file is not present.
- Index-based column access (`row[2]`, `row[4]`, `row[5]`, `row[1]`) is fragile — if your CSV columns reorder the script will break.
- Station name extraction uses a `set` of observed station names and then picks the first entry. If multiple station names appear, the selected name may be arbitrary (sets are unordered).
- The script runs at import time (no `main()` guard). That’s fine for direct execution but makes reuse/importing less convenient.
- The saving functionality depends on a `saver.py` module — ensure it exists and works in your environment.


## Contact / Author
Repository owner: @Haashiraaa
```
