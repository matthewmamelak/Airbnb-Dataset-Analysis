import gzip
import shutil

# Path to the gzipped file and the output CSV file name
gzipped_file_path = '/Users/matthewmamelak/PycharmProjects/ADA-FinalProject/calendar3.csv.gz'  # Adjust this to the correct path of your .gz file
output_csv_file_path = '/Users/matthewmamelak/PycharmProjects/ADA-FinalProject/calender3.csv'

# Unzipping the file and saving it as a CSV
with gzip.open(gzipped_file_path, 'rb') as f_in:
    with open(output_csv_file_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

print(f"File saved as {output_csv_file_path}")