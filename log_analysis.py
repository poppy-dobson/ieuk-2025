import pandas as pd
import csv

# Hi! This is my contribution for the Engineering 'Sector Skills Project' of the IEUK Virtual Internship Experience 2025
# My experience is in data analysis/data science (I do BSc Data Science)
# ..so I used Python and data analysis techniques to approach this task :)

# Info for IEUK submission & peer-review:
# To run this, you need python (I am using 3.13.2), with pandas and matplotlib installed

class LogFileAnalysis:
  def __init__(self, path):
    self.log_file_path = path
    self._load_data()

  def _load_data(self): # loads in the log file from the filepath given to the constructor
    self.log_file = []
    with open(self.log_file_path) as log:
      reader = csv.reader(log, delimiter=' ')
      for row in reader:
        self.log_file.append(row)

    self.log_df = pd.DataFrame(self.log_file, columns=['IP', '', 'Country', '', 'Datetime', 'Request', 'Code', '', '', 'User Agent', 'Object Size'])
    self._clean_data()

  def _clean_data(self): # cleans the dataframe, by dropping unnecessary columns, converting datatypes, and splitting columns into useful components
    self.log_df.drop(columns=[''], inplace=True)

    # datetimes
    temp_datetime = self.log_df['Datetime']
    temp_datetime = temp_datetime.str.strip('[]')
    temp_datetime = temp_datetime.str.split(':', n=1)
    temp_datetime = temp_datetime.str.join(' ')
    temp_datetime = pd.to_datetime(temp_datetime, format='%d/%m/%Y %H:%M:%S')

    temp_datetime_df = pd.DataFrame(temp_datetime)
    temp_datetime_df['Date'] = temp_datetime_df['Datetime'].dt.date
    temp_datetime_df['Year'] = temp_datetime_df['Datetime'].dt.year # year and month aren't useful for this particular log file, but could be for larger ones
    temp_datetime_df['Month'] = temp_datetime_df['Datetime'].dt.month
    temp_datetime_df['Day'] = temp_datetime_df['Datetime'].dt.day
    temp_datetime_df['Hour'] = temp_datetime_df['Datetime'].dt.hour
    temp_datetime_df['Minute'] = temp_datetime_df['Datetime'].dt.minute

    temp_datetime_df['Date Hour'] = temp_datetime_df['Date'].astype('str') + ":" + (temp_datetime_df['Hour'].astype('str')).str.rjust(2, "0")

    for col in temp_datetime_df.columns:
      self.log_df[col] = temp_datetime_df[col]

    # HTTP requests
    self.log_df['Code Class'] = self.log_df['Code'].astype('str').apply(lambda x: x[0])

    temp_request = self.log_df['Request']
    
    temp_request = temp_request.str.split(' ', n=2)
    temp_request_df = pd.DataFrame(temp_request.to_list(), columns=['Req Code', 'Page', 'other'])
    temp_request_df.drop(columns=['other'], inplace=True)

    for col in temp_request_df.columns:
      self.log_df[col] = temp_request_df[col]

    self.log_df['Page Main'] = self.log_df['Page'].str.strip('/').str.split('/').apply(lambda x: x[0])

    # extra cleaning
    self.log_df['Object Size'] = self.log_df['Object Size'].astype('int32')
    
    for text_col in self.log_df.select_dtypes(include='object').columns:
      self.log_df[text_col] = self.log_df[text_col].astype('str').str.strip()

  def print_full_report(self): # generates summaries and prints overall useful stats for a few of the features
    self.print_summary_statistics()

    # analysis of IPs
    self.analyse_ip_addresses()

    # date time
    self.analyse_datetime()

    # location
    self.analyse_location()

    # pages
    self.analyse_web_pages()

    # user agents
    self.analyse_user_agents()

  def print_summary_statistics(self):
    print("SUMMARY OF LOG FILE:")
    print(f"total number of logs submitted: {len(self.log_df)}")

    print()
    print(f"first log: {self.log_df['Datetime'].min()}")
    print(f"last log: {self.log_df['Datetime'].max()}")

    print()
    print(f"no. unique IP addresses: {self.log_df['IP'].nunique()}")

    print()
    print(f"no. unique country codes: {self.log_df['Country'].nunique()}")

    print()
    print(f"no. valid requests (2xx): {self.log_df['Code Class'].value_counts().loc['2']}")


  def analyse_ip_addresses(self):
    print("\nIP ADDRESSES:")
    ip_addresses = self.log_df['IP']
    self.ip_counts = ip_addresses.value_counts()
    n = 25
    print(f"top {n} IP addresses found (number of requests made):")
    print(self.ip_counts.head(n).to_string())

    day_range = (self.log_df['Datetime'].dt.date.max() - self.log_df['Datetime'].dt.date.min()).days + 1
    
    self.ip_alarming = self.ip_counts[self.ip_counts > (100 * day_range)]
    print()
    print("IP addresses with a suspicious number of requests (over 100 per day on average):")
    if len(self.ip_alarming) > 0: print(self.ip_alarming.to_string())
    else: print("there are no IP addresses that are largely concerning")


  def analyse_datetime(self):
    print("\nDATES & TIMES")

    dates = self.log_df['Date']
    self.date_counts = dates.value_counts().sort_index()
    print("number of requests on each day, ordered by date:")
    print(self.date_counts.to_string())

    hours = self.log_df['Hour']
    self.hour_counts = hours.value_counts().sort_index()
    print()
    print("number of requests by hour of day")
    print(self.hour_counts.to_string())
    top_hour_counts = self.hour_counts.sort_values(ascending=False).head(5)
    print(f"the top hours of day to prepare for traffic for are: {[i for i in top_hour_counts.index]}")

    date_hour = self.log_df['Date Hour']
    self.date_hour_counts = date_hour.value_counts().sort_index()
    print()
    print("number of requests by day AND hour")
    print(self.date_hour_counts.to_string())
    top_date_hour_counts = self.date_hour_counts[self.date_hour_counts > self.date_hour_counts.quantile(0.9)]
    print("the peak moments of traffic were:")
    print(top_date_hour_counts.to_string())


  def analyse_location(self):
    print("\nLOCATION")

    country_codes = self.log_df['Country']
    self.top_country_codes = country_codes.value_counts()
    print("top country codes:")
    print(self.top_country_codes.to_string())
    

  def analyse_web_pages(self):
    print("\nPAGES VISITED")

    main_pages = self.log_df['Page Main']
    self.main_pages_count = main_pages.value_counts()
    print("top areas of the site visited:")
    print(self.main_pages_count.head(10).to_string())
    
    pages = self.log_df['Page']
    self.pages_count = pages.value_counts()
    print()
    print("top specific pages visited:")
    print(self.pages_count.head(25).to_string())


  def analyse_user_agents(self):
    print("\nUSER AGENTS")

    user_agents = self.log_df['User Agent']
    self.user_agent_counts = user_agents.value_counts()
    print("top user agent headers found")
    print(self.user_agent_counts.head(20).to_string())
    print()
    print("least frequent user agent headers found")
    print(self.user_agent_counts.tail(15).to_string())
    print("inspect this list for any that seem suspicious")

##### main #####
if __name__ == '__main__':
  file = 'sample-log.log' # change this to whatever the log file's name/path is from your current directory
  project = LogFileAnalysis(file)
  project.print_full_report()