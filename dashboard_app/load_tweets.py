import os
import zipfile
import tempfile
import csv
from dateutil import parser

from dashboard_app.models import Tweet
from django.conf import settings


def load_tweets_from_csv_zip():
    zip_path = os.path.join(settings.BASE_DIR, r'dashboard_app\data\tweets_dataset_archive.zip')
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Find the CSV file inside the extracted directory
        csv_file = None
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.endswith('.csv'):
                    csv_file = os.path.join(root, file)
                    break

        if csv_file:
            # Load the data from the CSV file
            with open(csv_file, 'r') as f:
                csv_reader = csv.reader(f)
                next(csv_reader)  # Skip the header row

                tweets = []
                # Iterate over rows and create Tweet objects
                for row in csv_reader:
                    tweet_id = row[1]
                    twitter_handle = row[4]
                    # posting_date = row[2]
                    posting_date = parser.parse(row[2]).strftime('%Y-%m-%d %H:%M:%S')
                    message = row[5]

                    tweet = Tweet(
                        tweet_id=tweet_id,
                        twitter_handle=twitter_handle,
                        posting_date=posting_date,
                        message=message
                    )
                    #tweets.append(tweet)
                    tweet.save()
                #Tweet.objects.bulk_create(tweets)

            # Delete the CSV file
            os.remove(csv_file)
        else:
            print("No CSV file found in the zip archive.")
