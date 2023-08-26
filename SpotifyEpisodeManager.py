import spotipy
import sqlite3
from spotipy.oauth2 import SpotifyClientCredentials
from logger_config import logger


class SpotifyEpisodeManager:
    def __init__(self, client_id, client_secret, database_path):
        self.sp = self.authenticate_spotify(client_id, client_secret)
        self.conn, self.cursor = self.connect_to_database(database_path)
        self.logger = logger

    def connect_to_database(self, database_path):
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        return conn, cursor
    def authenticate_spotify(self, client_id, client_secret):
        try:
            client_credentials_manager = SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            return sp
        except KeyError:
            raise ValueError("Invalid or missing Spotify credentials in the configuration")

    def search_show_episodes(self, podcast_name):
        results = self.sp.search(q=podcast_name, market='US', type='show')
        show = results['shows']['items'][0]
        show_id = show['id']

        episodes = self.sp.show_episodes(show_id=show_id, market='US', limit=1, offset=0)
        return episodes

    def check_entry_exists(self, episode_id):
        self.cursor.execute("SELECT id FROM episodes WHERE id = ?", (episode_id,))
        existing_entry = self.cursor.fetchone()
        return existing_entry is not None

    def insert_episode_data(self, episode_id, episode_name, episode_description, episode_release_date, episode_href,
                            episode_link):
        try:
            self.cursor.execute('''
                    INSERT INTO episodes (id, name, description, release_date, href, link)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (episode_id, episode_name, episode_description, episode_release_date, episode_href, episode_link))

            self.logger.info(f"{episode_id} Successfully inserted in the database.")
        except Exception as e:
            self.logger.error(f"Error inserting episode {episode_id} into the database: {e}")

    def fetch_all_episodes(self):
        with self.conn:
            self.cursor.execute("SELECT * FROM episodes;")
            rows = self.cursor.fetchall()

        return rows

    def fetch_latest_episode(self):
        self.cursor.execute("SELECT * FROM episodes;")
        row = self.cursor.fetchone()
        return row

    def post_new_episode(self):
        print("Posting episode to lemmy")

    def __del__(self):
        self.conn.commit()
        self.conn.close()
