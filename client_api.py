import requests, urllib3
from config import Config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class UnauthorizedApiCall(Exception):
    pass


class ClientTmdbApi:
    url = "https://api.themoviedb.org/3/"
    cookie_tag = "Set-Cookie"
    session = requests.Session()
    session.headers["Accept"] = "application/json"
    session.headers["Authorization"] = Config.TMDB_API_CREDENTIALS

    def _request(self, api_method, json=None):
        if json is None:
            response = self.session.get(self.url + api_method, verify=False)
        else:
            response = self.session.post(self.url + api_method, json=json, verify=False)
            if response.status_code == 401:
                raise UnauthorizedApiCall()
        # required to avoid new session creation on every request
        if not self.session.headers.get(self.cookie_tag):
            self.session.headers[self.cookie_tag] = response.headers.get(
                self.cookie_tag
            )
        return response.json()

    def get_person_object(
        self, id_person=40239, object_name="movie_credits", language="cz-CZ"
    ):
        return self._request(
            "{}/{}/{}?language={}".format(
                "person", str(id_person), object_name, language
            )
        )

    def get_object_details(self, id_movie, object_name="movie"):
        return self._request("{}/{}".format(object_name, str(id_movie)))
