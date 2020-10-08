# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE public.songplays (
	songplyid numeric NOT NULL,
	start_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	user_id numeric NOT NULL,
	song_id varchar NULL,
	artist_id varchar NULL,
	session_id numeric NOT NULL,
	"location" varchar NOT NULL,
	user_agent varchar NOT NULL,
	"level" varchar(4) NOT NULL,
	CONSTRAINT songplays_pk PRIMARY KEY (songplyid),
	CONSTRAINT songplays_artist_fk FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
	CONSTRAINT songplays_songs_fk FOREIGN KEY (song_id) REFERENCES songs(song_id),
	CONSTRAINT songplays_time_fk FOREIGN KEY (start_time) REFERENCES "time"(start_time),
	CONSTRAINT songplays_users_fk FOREIGN KEY (user_id) REFERENCES users(user_id)
);
""")

user_table_create = ("""
CREATE TABLE public.users (
	user_id numeric NOT NULL,
	first_name varchar NOT NULL,
	last_name varchar NOT NULL,
	gender varchar(1) NOT NULL,
	"level" varchar(4) NULL,
	CONSTRAINT users_pk PRIMARY KEY (user_id)
);
""")

song_table_create = ("""
CREATE TABLE public.songs (
	song_id varchar NOT NULL,
	title varchar NOT NULL,
	artist_id varchar NOT NULL,
	"year" int4 NOT NULL,
	duration numeric NOT NULL,
	CONSTRAINT songs_pk PRIMARY KEY (song_id),
	CONSTRAINT songs_un UNIQUE (song_id, artist_id)
);

""")

artist_table_create = ("""
CREATE TABLE public.artists (
	artist_id varchar NOT NULL,
	"name" varchar NOT NULL,
	"location" varchar NOT NULL,
	latitude numeric NULL,
	longitude numeric NULL,
	CONSTRAINT artists_pk PRIMARY KEY (artist_id)
);
""")

time_table_create = ("""
CREATE TABLE public."time" (
	start_time timestamp NOT NULL,
	"hour" int4 NOT NULL,
	"day" int4 NOT NULL,
	week int4 NOT NULL,
	"month" int4 NOT NULL,
	"year" int4 NOT NULL,
	weekday int4 NOT NULL,
	CONSTRAINT time_pk PRIMARY KEY (start_time)
);
""")

# INSERT RECORDS
songplay_table_insert = ("""
INSERT INTO songplays(songplyid, start_time,user_id,song_id,artist_id,session_id,location,user_agent,level)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT ON CONSTRAINT songplays_pk DO NOTHING
""")

user_table_insert = ("""
INSERT INTO users(user_id, first_name, last_name, gender,level)
VALUES(%s,%s,%s,%s,%s) 
ON CONFLICT 
ON CONSTRAINT users_pk 
DO UPDATE SET first_name = EXCLUDED.first_name,last_name = EXCLUDED.last_name,gender=EXCLUDED.gender,level=EXCLUDED.level
""")

song_table_insert = ("""
INSERT INTO songs(song_id, title, artist_id, \"year\", duration)
VALUES(%s,%s,%s,%s,%s) 
ON CONFLICT ON CONSTRAINT songs_pk 
DO NOTHING
""")

artist_table_insert = ("""
INSERT INTO artists(artist_id,name,location,latitude,longitude) 
VALUES(%s,%s,%s,%s,%s) 
ON CONFLICT 
ON CONSTRAINT artists_pk 
DO NOTHING
""")

time_table_insert = ("""
INSERT INTO time(start_time, hour, day, week, month,year, weekday)
VALUES(%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT ON CONSTRAINT time_pk 
DO NOTHING
""")

drop_database = ("""
DROP DATABASE IF EXISTS sparkifydb
""")

recreate_database = ("""
CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0
""")
# FIND SONGS

song_select = ("""
SELECT s.song_id, s.artist_id 
FROM songs s 
INNER JOIN artists a 
ON s.artist_id = a.artist_id WHERE s.title=%s AND a.name=%s
""")

# QUERY LISTS

create_table_queries = [user_table_create, artist_table_create, time_table_create, song_table_create,
                        songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
