from abc import abstractmethod, ABC
from typing import Dict, List

from plex_api_client import PlexAPI
from plex_api_client.models import operations

from app.utils.format_movie_response import format_last_added_movie
from app.utils.request_plex import get_request


class PlexSDKAbstract(ABC):
    @abstractmethod
    def get_last_added_movie(self):
        pass

    @abstractmethod
    def get_all_libraries(self):
        pass

    @abstractmethod
    def retrieve_thumb_image(self, rating_key):
        pass

    @abstractmethod
    def retrieve_server_list(self):
        pass


class PlexSDK(PlexSDKAbstract):
    def __init__(self, s: PlexAPI):
        self.s = s
        self.access_token = self.s.sdk_configuration.security.access_token
        self.server_url = self.s.sdk_configuration.server_url

    def get_last_added_movie(self) -> Dict[str, str]:
        response = get_request(self.s.library.get_recently_added_library, request={
            "type": operations.QueryParamType.MOVIE,
            "content_directory_id": 2,
            "pinned_content_directory_id": [
                3, 5, 7, 13, 12, 1, 6, 14, 2, 10, 16, 17
            ],
            "section_id": 2,
            "include_meta": operations.QueryParamIncludeMeta.ENABLE
        })
        return format_last_added_movie(
            response,
            self.access_token,
            self.server_url,
            self.retrieve_server_list()
        )

    def get_all_libraries(self) -> List[Dict]:
        return get_request(self.s.library.get_all_libraries)

    def retrieve_thumb_image(self, rating_key: str) -> Dict:
        return get_request(self.s.media.get_thumb_image, request={
            "rating_key": rating_key,
            "width": 396,
            "height": 396,
            "min_size": 1,
            "upscale": 1,
            "x_plex_token": ""
        })

    def retrieve_server_list(self) -> Dict:
        return get_request(self.s.server.get_server_list)
