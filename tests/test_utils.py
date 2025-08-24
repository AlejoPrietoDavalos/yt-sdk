from yt_sdk.utils import youtube_id_from_url

def test_youtube_id_from_url_for_real_cases():
    # Casos válidos
    assert youtube_id_from_url(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    assert youtube_id_from_url(url="http://youtube.com/watch?v=abcdEFG1234") == "abcdEFG1234"
    assert youtube_id_from_url(url="https://www.youtube.com/embed/abcdEFG1234") == "abcdEFG1234"
    assert youtube_id_from_url(url="https://www.youtube.com/v/abcdEFG1234") == "abcdEFG1234"
    assert youtube_id_from_url(url="https://www.youtube.com/watch?v=abcdEFG1234&t=42s") == "abcdEFG1234"

    # Casos inválidos
    assert youtube_id_from_url(url="https://www.google.com/watch?v=dQw4w9WgXcQ") is None
    assert youtube_id_from_url(url="https://youtube.com/") is None
    assert youtube_id_from_url(url="https://www.youtube.com/watch?v=short") is None
    assert youtube_id_from_url(url="") is None
    assert youtube_id_from_url(url="https://www.youtube.com/watch?v=") is None
    assert youtube_id_from_url(url="https://www.youtube.com/watch?v=dQw4w9WgXcQextra") is None
