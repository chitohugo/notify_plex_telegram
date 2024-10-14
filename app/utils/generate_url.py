def generate_image_url(image_path: str, access_token: str, server_url: str) -> str:
    if not image_path or not access_token or not server_url:
        raise ValueError("Image path, access token, and server URL are required")

    base_url = f"{server_url}{image_path}"
    return f"{base_url}?X-Plex-Token={access_token}"


def generate_movie_url(key: str, server_url: str, retrieve_server_list) -> str:
    if not key or not server_url:
        raise ValueError("Key and server URL are required")

    try:
        server_id = retrieve_server_list.object.media_container.server[0].machine_identifier
    except (AttributeError, IndexError):
        raise ValueError("Unable to retrieve server information from the provided list")

    return f"{server_url}/web/index.html#!/server/{server_id}/details?key={key}"
