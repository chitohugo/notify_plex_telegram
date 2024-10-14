from app.utils.generate_url import generate_image_url, generate_movie_url

def format_last_added_movie(movie, access_token: str, server_url: str, retrieve_server_list) -> dict:
    try:
        last_added = movie.object.media_container.metadata[0]
    except (IndexError, AttributeError):
        return {"error": "No media found in 'metadata'."}

    title = last_added.title
    year = int(last_added.year)
    studio = last_added.studio
    summary = last_added.summary
    thumb_image = last_added.thumb
    art = last_added.art
    rating_key = int(last_added.rating_key)

    response = {
        "title": title,
        "type": last_added.type,
        "year": year,
        "studio": studio,
        "description": summary,
        "library_section_uuid": last_added.library_section_uuid,
        "thumb_image": thumb_image,
        "thumb_image_url": generate_image_url(
            image_path=last_added.thumb,
            access_token=access_token,
            server_url=server_url
        ),
        "art": art,
        "media": format_media(last_added.media),
        "rating_key": rating_key,
        "movie_url": generate_movie_url(
            key=last_added.key,
            server_url=server_url,
            retrieve_server_list=retrieve_server_list
        )
    }

    return response

def format_media(media_list) -> list:
    media_info = []
    for media in media_list:
        video_resolution = int(media.video_resolution)
        bitrate = int(media.bitrate)
        duration = int(media.duration)

        media_data = {
            "video_resolution": video_resolution,
            "audio_codec": media.audio_codec,
            "bitrate": bitrate,
            "duration": duration,
            "parts": [
                {
                    "file": part.file,
                    "size": int(part.size),
                    "container": part.container
                }
                for part in media.part
            ],
        }
        media_info.append(media_data)

    return media_info
