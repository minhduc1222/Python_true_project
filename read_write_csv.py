import csv

LIBRARY_CSV_FILE = "library_video_list.csv"

def read_csv(file_name):
    data_dict = {}
    with open(file_name, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Assuming 'id' is a unique identifier for each row
            data_dict[row['id']] = row
    return data_dict

def write_to_csv(data, filename, include_play_count=False):
    # Open the CSV file in write mode
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        header = ['id', 'name', 'director', 'video_length', 'rating']

        if include_play_count:
            header.append('play_count')
        # Write the header row
        writer.writerow(header)
        
        # Write each entry in the dictionary
        for video_id, details in data.items():
            row = [video_id, details['name'], details['director'], details['video_length'], details['rating']]
            if include_play_count:
                row.append(details['play_count'])
            writer.writerow(row)

if __name__ == '__main__':
    data = read_csv(LIBRARY_CSV_FILE)
    print(data)
    # Example usage
    # data['09'] = {'id': '09', 'name': 'fads', 'director': 'asdf', 'video_length': '30', 'rating': '3.0', 'play_count': '0'}
    # write_to_csv(data, LIBRARY_CSV_FILE)
