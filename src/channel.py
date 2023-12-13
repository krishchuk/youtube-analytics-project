import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/manifest-ocean-407215-51b1854c7f81.json"
    api_key: str = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.__channel_id = channel_id
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    def to_json(self, new_file):
        data = [{
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }]
        with open(new_file, 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)


# ch = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
# print(f'id:\n{ch.channel_id}')
# print(f'title:\n{ch.title}')
# print(f'description:\n{ch.description}')
# print(f'url:\n{ch.url}')
# print(f'subscriberCount:\n{ch.subscriber_count}')
# print(f'videoCount:\n{ch.video_count}')
# print(f'viewCount:\n{ch.view_count}')
