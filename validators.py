from datetime import datetime

# Define 'datestring' function below which validates the input date value
# The input date value must be of the string format "YYYY-MM-DD".
# If the input string is in expected format, convert it into datetime object and return else
# else raise Value Error 'A Date in format, "%Y-%m-%d", is expected. '
def datestring(value):
  try:
    date_obj = datetime.strptime(value, '%Y-%m-%d')
    return date_obj
  except ValueError:
    print('A Date in format, "%Y-%m-%d", is expected. ')

#datestring("1999-100-02")
