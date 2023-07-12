import requests
from logger_config import logger


class LemmyBot:
    def __init__(self, username, password):
        self.lemmy_instance_url = "https://lemmy.world"
        self.session = requests.Session()
        self.jwt = None
        self.login(username, password)
        self.logger = logger

    def login(self, username, password):
        login_url = f"{self.lemmy_instance_url}/api/v3/user/login"
        login_data = {"username_or_email": username, "password": password}

        try:
            response = self.session.post(login_url, json=login_data)
            response.raise_for_status()
            login_response = response.json()
            self.jwt = login_response.get("jwt")

            if self.jwt:
                logger.info(f"{username} log in successful.")
            else:
                logger.warning(f"{username} failed to log in. Invalid credentials or server error.")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error logger in: {e}")

        except ValueError as e:
            logger.error(f"Error parsing response: {e}")

    def create_post(self, community_id, name, body=None, honeypot=None, language_id=None, nsfw=None,
                    url=None):

        create_post_url = f"{self.lemmy_instance_url}/api/v3/post"
        create_post_data = {
            "auth": self.jwt,
            "community_id": community_id,
            "name": name,
            "body": body,
            "honeypot": honeypot,
            "language_id": language_id,
            "nsfw": nsfw,
            "url": url
        }

        response = None  # Initialize response variable

        try:
            response = self.session.post(create_post_url, json=create_post_data)
            print(create_post_data)
            response.raise_for_status()
            logger.info("Post created successfully.")

        except requests.exceptions.RequestException as e:
            logger.warning("Failed to create post.")
            if response is not None:
                logger.warning(f"Response: {response.text}")
            raise

    def search_lem(self, q, auth=None, community_id=None, community_name=None, creator_id=None, limit=None,
                   listing_type=None, page=None, sort=None, type_=None):

        search_url = f"{self.lemmy_instance_url}/api/v3/search"

        # Construct the request payload
        payload = {
            "q": q,
            "auth": auth,
            "community_id": community_id,
            "community_name": community_name,
            "creator_id": creator_id,
            "limit": limit,
            "listing_type": listing_type,
            "page": page,
            "sort": sort,
            "type_": type_
        }

        try:
            response = self.session.get(search_url, params=payload)
            response.raise_for_status()
            search_results = response.json()

            if response.status_code == 200:
                logger.info("Search successful.")
                logger.info(search_results)

            else:
                logger.warning("Failed to perform search.")
                logger.warning(f"Response: {response.text}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error performing search: {e}")

    def get_community(self, auth=None, id=None, name=None):

        search_url = f"{self.lemmy_instance_url}/api/v3/community"

        # Construct the request payload
        payload = {
            "auth": auth,
            "id": id,
            "name": name
        }

        try:
            response = self.session.get(search_url, params=payload)
            response.raise_for_status()
            search_results = response.json()

            if response.status_code == 200:
                logger.info("Search successful.")
                logger.info(search_results)

            else:
                logger.warning("Failed to get community.")
                logger.warning(f"Response: {response.text}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error performing getCommunity:{e}")
