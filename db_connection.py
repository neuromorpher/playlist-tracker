import sqlite3 
import os 
from datetime import datetime 

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(PROJECT_ROOT, "playlist_tracker.db")
schema_path = os.path.join(PROJECT_ROOT, "schema.sql")


def init_database(db_path, schema_path):


    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")


    try:

        with open(schema_path, 'r') as f:

            schema_sql = f.read()

            conn.executescript(schema_sql)
            print("Schema executed successfully.")

    except sqlite3.Error as e:

        print(f"Error: {e}")

    finally:

        conn.commit()
        conn.close()


init_database(db_path, schema_path)


def save(playlistId, vids:dict):

    # 1. Connect to DB, turn on FKs, use try/except struct [/]
    # 2. Get the current time as a string (datetime module) [/]
    # 3. Insert row for the playlist  [/]
    # 4. Loop over vids(dict) with one statement for video and one for playlist_videoper video []
    # 5. Commit [/]

    conn = sqlite3.connect(db_path) 
    conn.execute("PRAGMA foreign_keys = ON")

    try: 

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


        scrp1 = """

        insert into playlist(id)
        values(?)
        on conflict (id) do nothing; 

        """
        conn.execute(scrp1, (playlistId, ))


        for videoId, title in vids.items():

            if title in ["Private video", "Deleted video"]:

                scrp2 = """

                insert into video(id) 
                values(?)
                on conflict (id) do nothing;

                """

                conn.execute(scrp2, (videoId,)) 

                scrp2b = """

                insert into playlist_video(playlist_id, video_id, gone_missing)

                values(?,?,?)

                on conflict (playlist_id, video_id) do update set gone_missing = excluded.gone_missing where gone_missing is null;
                """

                conn.execute(scrp2b, (playlistId, videoId, now))

            else:

                scrp3 = """

                        insert into video(id, title)
                        values(?,?)
                        on conflict (id) do update set title = excluded.title;
                        """


                conn.execute(scrp3, (videoId, title)) 

                scrp4 = """

                insert into playlist_video(playlist_id, video_id, last_seen)
                values(?,?,?)
                on conflict (playlist_id, video_id) do update set last_seen = excluded.last_seen;


                """

                conn.execute(scrp4, (playlistId, videoId, now)) 





        conn.commit()


    except sqlite3.Error as e:

        print(f"Error: {e}")


    finally:

        conn.close() 




