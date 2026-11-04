import sqlite3 
import os
from datetime import datetime 

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(PROJECT_ROOT, "playlist_tracker.db")
schema_path = os.path.join(PROJECT_ROOT, "schema.sql")


def connect_db(db_path):

    conn = sqlite3.connect(db_path) 
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def init_database(db_path, schema_path):

    conn = connect_db(db_path) 


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



def save(playlistId, vids:dict):

    # 1. Connect to DB, turn on FKs, use try/except struct [/]
    # 2. Get the current time as a string (datetime module) [/]
    # 3. Insert row for the playlist  [/]
    # 4. Loop over vids(dict) with one statement for video and one for playlist_videoper video []
    # 5. Commit [/]

    conn = connect_db(db_path)

    try: 

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


        scrp1 = """

        insert into playlist(id, last_fetched)
        values(?, ?)
        on conflict (id) do update set last_fetched = excluded.last_fetched;

        """
        conn.execute(scrp1, (playlistId, now))


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

def view_db():

    conn = connect_db(db_path)

    try:

        last_fetched = dict(conn.execute("select id, last_fetched from playlist;").fetchall())

        missing_counts = dict(conn.execute("select playlist_id, count(gone_missing) from playlist_video group by playlist_id;").fetchall()) 


        video_counts = dict(conn.execute("select playlist_id, count(*) from playlist_video group by playlist_id;").fetchall())

        # print(f"\n\n Video Count: {row[0]}") 


        cursor = conn.execute(""" select video_id, video.title, playlist_id, last_seen, gone_missing

from video join playlist_video on video.id = playlist_video.video_id

order by playlist_id, gone_missing desc;

                
                """)

        rows = cursor.fetchall() 

        last_pl_id = None
        last_missing = None

        for video_id, title, playlist_id, last_seen, gone_missing in rows: 

            if playlist_id != last_pl_id:

                last_pl_id = playlist_id
                last_missing = None 
                print() 
                print(f"=== Playlist {playlist_id} === ({video_counts[playlist_id]} videos, {missing_counts[playlist_id]} missing, checked {last_fetched[playlist_id][:10] if last_fetched[playlist_id] is not None else 'never'})")

            is_missing = gone_missing is not None 

            if is_missing != last_missing:

                print("\tMISSING" if is_missing else "\tAVAILABLE")
                last_missing = is_missing
            if is_missing:

                print(f"✗ {title}\tgone since {gone_missing}")
            else:

                print(f"✓ {title}\tlast seen {last_seen}")

                     
    except sqlite3.Error as e:

        print(f"Error: {e}")

       
    finally:

        conn.close() 

if __name__ == "__main__":
    
    init_database(db_path, schema_path)
    


