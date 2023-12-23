import json
import os
import datetime
# from datetime import datetime

import isodate
from googleapiclient.discovery import build


class PlayList:
    """Класс для ютуб-плейлиста"""
    api_key: str = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, playlist_id: str) -> None:
        self.__playlist_videos = self.get_service().playlistItems().list(playlistId=playlist_id,
                                                                         part='snippet,contentDetails',
                                                                         maxResults=50,
                                                                         ).execute()
        self.__playlist_id = self.__playlist_videos['items'][0]['snippet']['playlistId']
        self.__playlists = self.get_service().playlists().list(
            channelId=self.__playlist_videos['items'][0]['snippet']['videoOwnerChannelId'],
            part='contentDetails,snippet',
            maxResults=50,
        ).execute()
        for i in range(len(self.__playlists)):
            if self.__playlists['items'][i + 1]['id'] == self.__playlist_id:
                self.title = self.__playlists['items'][i + 1]['snippet']['title']
        self.url: str = "https://www.youtube.com/playlist?list=" + self.__playlist_id

    @property
    def total_duration(self):
        """возвращает объект класса datetime.timedelta с суммарной длительность плейлиста"""
        total_duration = datetime.timedelta()
        for i in range(len(self.__playlist_videos)):
            video_id = self.__playlist_videos['items'][i]['snippet']['resourceId']['videoId']
            video = self.get_service().videos().list(part='contentDetails',
                                                     id=video_id
                                                     ).execute()
            duration_from_yt = video['items'][0]['contentDetails']['duration']
            duration_form = isodate.parse_duration(duration_from_yt)
            total_duration += duration_form
        return total_duration

    def show_best_video(self):
        """Возвращает ссылку на видео с наибольшим количеством лайков"""
        video_id_list = []
        video_likes_list = []
        max_likes_index = None
        for i in range(len(self.__playlist_videos)):
            # Создается лист с ID видео в плейлисте
            video_id = self.__playlist_videos['items'][i]['snippet']['resourceId']['videoId']
            video_id_list.append(video_id)
            # Создается лист с количеством лайков видео в плейлисте
            video = self.get_service().videos().list(part='snippet,statistics',
                                                     id=video_id
                                                     ).execute()
            video_likes_count = video['items'][0]['statistics']['likeCount']
            video_likes_list.append(video_likes_count)

        # Сравнивается количество лайков видео
        for i in range(len(video_likes_list) - 1):
            if video_likes_list[i] > video_likes_list[i + 1]:
                max_likes_index = i
            else:
                max_likes_index = i+1
        return "https://youtu.be/" + str(video_id_list[max_likes_index])

    def print_info(self) -> None:
        """Выводит в консоль информацию о плейлисте."""
        print(json.dumps(self.__playlist_videos, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)
