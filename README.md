# ieuk-2025
My submission for the IEUK 2025 (run by Bright Network) Engineering Sector Skills project.

### The Task

This project was to analyse a web traffic log file, and identify the issues the site may have been facing.

The log file provided to us had lines such as the following:

`173.80.18.254 - NO - [01/07/2025:06:00:04] "POST / HTTP/1.1" 200 1234 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" 124`

### Code

`log_analysis.py` takes in the log file (named `sample-log.log`), turns it into a pandas dataframe and prints a simple analysis report

`log_viz_and_further_analysis.ipynb` expands on this, doing further analysis of the data and some visualisation to help explain any trends

I used Python 3.13.
