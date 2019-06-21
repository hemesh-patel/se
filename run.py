# This will be the pipeline as such.
# Need to create a process were we collect data and put into a 'raw_data' directory
# Directory will need creating, so will a directory  called 'clean_data' to be ingested into postgres
# Task to load data into postgres
# Task to run sql statements and output csv. Create a directory called 'output_data'

from utils import collect_raw_data as cl
from utils import create_directory as dir
from utils import extract_data as clean
from utils import write_read_postgres as db

# Making directories
raw_dir_name = 'raw_data'
clean_dir_name = 'clean_data'

dir.make_dir(raw_dir_name)
dir.make_dir(clean_dir_name)

# Importing the data

xml_url = "https://s3.amazonaws.com/static.secretescapes.com/data-interview/weekly"
raw_sales_file_name = 'raw_current_sale.xml'

csv_url = 'https://s3.amazonaws.com/static.secretescapes.com/data-interview/bookings'
raw_booking_file_name = 'raw_bookings_data.csv'

cl.collect_data(xml_url, raw_dir_name, raw_sales_file_name)
cl.collect_data(csv_url, raw_dir_name, raw_booking_file_name)

# Cleaning the data

clean_sales_data_file_name = 'sales_data.csv'
raw_sales_path = clean.full_path_to_data(raw_dir_name, raw_sales_file_name)  # collect full path to sales xml file
raw_sales_data = clean.root_in_memory(raw_sales_path)  # read the data
clean.clean_sales_data(raw_sales_data, clean_dir_name, clean_sales_data_file_name)  # output clean data

clean_booking_data_file_name = 'booking_data.csv'
raw_booking_path = clean.full_path_to_data(raw_dir_name, raw_booking_file_name)
clean.clean_booking_data(raw_booking_path, clean_dir_name, clean_booking_data_file_name)

# Setting up connection
conn = db.postgres_connection('postgres', 'postgres')
cur = conn.cursor()

# Read sql statement into python variable
sql_sales_path = clean.full_path_to_data('sql_statements', 'sales_dump.sql')
sales_sql = open(sql_sales_path, 'r').read()

sql_booking_path = clean.full_path_to_data('sql_statements', 'booking_dump.sql')
booking_sql = open(sql_booking_path, 'r').read()

# Path to data which is to be loaded in to DB
sales_data_path = clean.full_path_to_data(clean_dir_name, clean_sales_data_file_name)
booking_data_path = clean.full_path_to_data(clean_dir_name, clean_booking_data_file_name)

# Create tables DB
db.create_table(cur, conn, sales_sql)
db.create_table(cur, conn, booking_sql)

# Dump data to DB
sales_table_name = (sales_sql.split(' ')[2])
booking_table_name = (booking_sql.split(' ')[2])

db.dump_to_db(cur, conn, sales_data_path, '|', sales_table_name)
db.dump_to_db(cur, conn, booking_data_path, '|', booking_table_name)

