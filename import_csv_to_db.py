import csv
from datetime import datetime
from app import db, Message  # Import your database model and Flask app

# Import Flask app instance directly
from app import app

# Initialize Flask app context
with app.app_context():
    # Read the CSV file
    csv_file_path = '/home/dan_mutisya/Downloads/GeneralistRails_Project_MessageData.csv'
    with open(csv_file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract data from the CSV row
            user_id = int(row['User ID'])  # Assuming user_id is an integer
            timestamp_str = row['Timestamp (UTC)']  # Assuming timestamp is in string format
            message_body = row['Message Body']

            # Convert timestamp string to datetime object
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

            # Create a new Message object and add it to the database session
            new_message = Message(user_id=user_id, timestamp=timestamp, message=message_body)
            db.session.add(new_message)

        # Commit the changes to the database
        db.session.commit()
