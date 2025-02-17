import json
import os

from googleapiclient.discovery import build


class Video:
    """Класс для ютуб-видео"""
    api_key: str = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        try:
            self.video = self.get_service().videos().list(part='snippet,statistics,contentDetails',
                                                          id=video_id
                                                          ).execute()
            self.video_id: str = self.video['items'][0]['id']
            self.title: str = self.video['items'][0]['snippet']['title']
            self.url: str = "https://youtu.be/" + self.video_id
            self.view_count: int = self.video['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video['items'][0]['statistics']['likeCount']
        except IndexError:
            self.video_id = video_id
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return self.title

    def print_info(self) -> None:
        """Выводит в консоль информацию о видео ."""
        print(json.dumps(self.video, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
