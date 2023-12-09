# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict

def reformat_dates(old_dates):
    
    reformatted_dates = [datetime.strptime(date, '%Y-%m-%d').strftime('%d %b %Y') for date in old_dates]
    return reformatted_dates

def date_range(start, n):
  
    start_date = datetime.strptime(start, '%Y-%m-%d')
    date_objects = [start_date + timedelta(days=i) for i in range(n)]
    return date_objects

def add_date_range(values, start_date):
   
    date_objects = date_range(start_date, len(values))
    result = list(zip(date_objects, values))
    return result

def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    late_fees_dict = defaultdict(float)

    with open(infile, 'r') as file:
        reader = DictReader(file)
        for row in reader:
            due_date_str = row['date_due']
            return_date_str = row['date_returned']

            try:
                due_date = datetime.strptime(due_date_str, '%m/%d/%Y')
                return_date = datetime.strptime(return_date_str, '%m/%d/%y')
            except ValueError as e:
                print(f"Error parsing dates. due_date_str: {due_date_str}, return_date_str: {return_date_str}")
                raise e

            if return_date > due_date:
                days_late = (return_date - due_date).days
                late_fee = days_late * 0.25
                late_fees_dict[row['patron_id']] += late_fee

    with open(outfile, 'w', newline='') as file:
        writer = DictWriter(file, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()
        for patron_id, late_fee in late_fees_dict.items():
            writer.writerow({'patron_id': patron_id, 'late_fees': "{:.2f}".format(late_fee))


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())

