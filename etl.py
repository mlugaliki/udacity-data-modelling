import glob
import json
import os
import time
import traceback
from datetime import datetime

import pandas as pd

from database_connection import get_connection
from sql_queries import *


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, typ='series')

    # insert song record
    song_data = (df['song_id'], df['title'], df['artist_id'], df['year'], df['duration'])
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = (
        df['artist_id'], df['artist_name'], df['artist_location'], df['artist_latitude'], df['artist_longitude'])
    cur.execute(artist_table_insert, artist_data)


def get_user_data_df(df):
    for i, rw in df.iterrows():
        user_data = [[rw.userId, rw.firstName, rw.lastName, rw.gender, rw.level]]
        column_labels = ['userId', 'firstName', 'lastName', 'gender', 'level']
        user_df = pd.DataFrame(data=user_data, columns=column_labels)
        return user_df


def process_log_file(cur, filepath):
    try:
        with open(filepath) as fp:
            for line in fp:
                # filter by NextSong action
                df = pd.DataFrame(json.loads(line), index=[0])
                if df.loc[df['page'] == 'NextSong'].empty:
                    continue

                # convert timestamp column to datetime
                ts = df['ts']
                pattern = '%Y-%m-%d %H:%M:%S'
                t = time.strftime(pattern, time.localtime(ts / 1000))
                ts = datetime.strptime(t, pattern)
                hour = ts.hour
                month = ts.month
                weekday = ts.weekday() + 1
                year, week_num, day_of_week = ts.isocalendar()
                time_data = [[t, hour, day_of_week, week_num, month, year, weekday]]
                column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']

                time_df = pd.DataFrame(data=time_data, columns=column_labels)
                for i, row in time_df.iterrows():
                    cur.execute(time_table_insert, list(row))

                # load user table
                user_df = get_user_data_df(df)
                # insert user records
                for i, row in user_df.iterrows():
                    cur.execute(user_table_insert, list(row))

                # insert songplay records
                for index, row in df.iterrows():
                    # get songid and artistid from song and artist tables
                    cur.execute(song_select, (row.song, row.artist, row.length))
                    results = cur.fetchone()
                    if results:
                        songid, artistid = results
                    else:
                        songid, artistid = None, None

                    # insert songplay record
                    songplay_data = [row.ts, t, row.userId, songid, artistid, row.sessionId, row.location,
                                     row.userAgent, row.level]
                    cur.execute(songplay_table_insert, songplay_data)
    except Exception as e:
        traceback.print_exc()


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = get_connection()
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
