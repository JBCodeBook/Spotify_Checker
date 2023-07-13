import json
from logger_config import logger
import os
from SpotifyEpisodeManager import SpotifyEpisodeManager
from lemmyBot import LemmyBot


def load_config(config_file_path):
    with open(config_file_path) as config_file:
        config = json.load(config_file)
    return config


def process_episodes(episode_manager, episodes, username, password):
    for episode in episodes['items']:
        episode_id = episode['id']
        episode_name = episode['name']
        episode_description = episode['description']
        episode_release_date = episode['release_date']
        episode_href = episode['href']
        episode_link = episode['external_urls']['spotify']

        if episode_manager.check_entry_exists(episode_id):
            logger.info(f"Entry with id '{episode_id}' already exists in the database.")
        else:

            try:
                logger.info(f"No entry with id '{episode_id}' found in the database.")

                lemmy_manager = LemmyBot(username, password)
                logger.info(f"{username} logging into lemmy")
                lemmy_manager.create_post(
                    community_id=3435,
                    name=episode_name,
                    url=episode_link
                )
                post_success = True

                if post_success:
                    episode_manager.insert_episode_data(
                        episode_id, episode_name, episode_description,
                        episode_release_date, episode_href, episode_link
                    )

            except Exception as e:
                logger.warning("Skipping database update due to post creation failure.")
                logger.error(f"Error logger in: {e}")


def main(config):
    client_id = config['spotify']['client_id']
    client_secret = config['spotify']['client_secret']
    redirect_uri = config['spotify']['Redirect_URI']
    username = config['lemmy']['username']
    password = config['lemmy']['password']
    database_path = os.path.expanduser('./Spotify.db')

    episode_manager = SpotifyEpisodeManager(
        database_path=database_path,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri
    )

    conn, cursor = episode_manager.connect_to_database(database_path)

    podcast_name = "Joe Rogan Experience"
    episodes = episode_manager.search_show_episodes(podcast_name)
    process_episodes(episode_manager, episodes, username, password)

    # Close the connection
    conn.close()


if __name__ == "__main__":
    config = load_config('config.json')
    main(config)
