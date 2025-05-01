from semantic_kernel.functions import kernel_function
import chainlit as cl
import json
from pytube import Search

class MentalCarePlugin:
    def youtube_search(self, search_terms):
        s = Search(search_terms)
        s.results
        urls = []
        for v in s.results:
            urls.append("https://www.youtube.com/watch?v=" + v.video_id)
        return urls[:3]
    
    @kernel_function(
        name="get_peaceful_music",
        description="Return a list of music for stressed people."
    )
    async def get_peaceful_music(self, search_query: str) -> str:
        async with cl.Step(name="Fetching peaceful music...", type="function"):
            pass
        results = self.youtube_search("spiritual and peaceful music")
        resources = [
            {"title": "Spotify Peaceful Music", "url": "https://open.spotify.com/album/2HSzOYRKirzlOZuGnuH80n"}
        ]
        return json.dumps({
            "results": results,
            "resources": resources
        })
    
    @kernel_function(
        name="get_gym_music",
        description="Return a list of music for gym."
    )
    async def get_gym_music(self, search_query: str) -> str:
        async with cl.Step(name="Fetching gym music...", type="function"):
            pass
        results = self.youtube_search("energetic and pump music for gym")
        resources = [
            {"title": "Spotify Gym Music", "url": "https://open.spotify.com/album/1UvM5bMUPoNldI7vI3lc1M"}
        ]
        return json.dumps({
            "results": results,
            "resources": resources
        })
    
    @kernel_function(
        name="get_healing_music",
        description="Return a list of music for depressed people."
    )
    async def get_healing_music(self, search_query: str) -> str:
        async with cl.Step(name="Fetching healing music...", type="function"):
            pass
        results = self.youtube_search("healing music for depression")
        resources = [
            {"title": "Spotify Healing Music", "url": "https://open.spotify.com/playlist/54QkjJbQzhkOcNoLUA5PAy"}
        ]
        return json.dumps({
            "results": results,
            "resources": resources
        })