from semantic_kernel.functions import kernel_function
import asyncio
from collections import defaultdict
from playwright.async_api import async_playwright
import json
import re
import chainlit as cl

class FitnessPlugin:

    @kernel_function(
        name="get_supported_muscles",
        description="Return a list of supported muscle names for training video search."
    )
    async def get_supported_muscles(self) -> str:
        async with cl.Step(name="Analyzing user intent...", type="function"):
            pass
        return json.dumps([
            "Chest", "Back", "Shoulders", "Biceps", "Triceps", 
            "Quadriceps", "Hamstrings", "Glutes", "Calves", "Abs", 
            "Forearms", "Neck", "Traps", "Obliques"
        ])

    @kernel_function(
        name="get_exercises_by_muscle",
        description="Return a list of exercises (with video URLs) for a specific muscle and gender."
    )
    async def get_exercises_by_muscle(self, muscle: str, gender: str) -> str:
        async with cl.Step(name="Searching for resources of " + muscle, type="function"):
            pass
        base_url = f"https://musclewiki.com/exercises/{gender.lower()}/{muscle.lower()}/"
        urls = await self.scrape_video_urls(base_url)

        video_dict = defaultdict(dict)
        for url in urls:
            clean_url = url.split("#")[0]
            filename = clean_url.split("/")[-1].split(".mp4")[0]
            match = re.match(r"[\w]+-[\w]+-(.*)-(side|front)(_[\w]+)?$", filename)
            if match:
                name_key_raw, view, _ = match.groups()
                name_key = name_key_raw.lower()
                readable_name = name_key.replace("-", " ").title()
                if view == "side":
                    video_dict[name_key]["sideUrl"] = clean_url
                    video_dict[name_key]["name"] = readable_name
                elif view == "front":
                    video_dict[name_key]["frontUrl"] = clean_url
                    video_dict[name_key]["name"] = readable_name

        exercises = []
        for name_key, data in video_dict.items():
            if "sideUrl" in data and "frontUrl" in data:
                exercises.append({
                    "name": data["name"],
                    "sideUrl": data["sideUrl"],
                    "frontUrl": data["frontUrl"],
                    "notes": " ",  # Placeholder, can be filled later
                    "tips": " "
                })

        return json.dumps({
            "muscle": muscle,
            "exercises": exercises
        })

    async def scrape_video_urls(self, url: str) -> list[str]:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--window-position=100,100",
                    "--window-size=1200,800"
                ]
            )
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            await page.wait_for_load_state("networkidle")

            seen_sources = set()
            scroll_step = 500
            max_scrolls = 8
            no_new_count = 0
            max_no_new = 2

            for _ in range(max_scrolls):
                video_elems = await page.query_selector_all("video")
                new_found = 0

                for video in video_elems:
                    source = await video.query_selector("source")
                    if source:
                        src = await source.get_attribute("src")
                        if src and src not in seen_sources:
                            seen_sources.add(src)
                            new_found += 1

                if new_found == 0:
                    no_new_count += 1
                    if no_new_count >= max_no_new:
                        break
                else:
                    no_new_count = 0

                await page.evaluate(f"window.scrollBy(0, {scroll_step})")
                await asyncio.sleep(0.3)

            await browser.close()
            return list(seen_sources)

    @kernel_function(
        name="get_video_note_block_format",
        description="Return the JSON output format for rendering exercise videos with notes and tips."
    )
    async def get_video_note_block_format(self) -> str:
        async with cl.Step(name="Summarizing exercise notes format...", type="function"):
            pass
        return json.dumps({
            "render": [
                {
                    "type": "video_block",
                    "title": "<exercise name>",
                    "props": {
                        "sideUrl": "<side view video URL>",
                        "frontUrl": "<front view video URL>"
                    }
                },
                {
                    "type": "text_block",
                    "title": "<content_title>",
                    "props": {
                        "content": "<content>"
                    }
                }
            ]
        })
