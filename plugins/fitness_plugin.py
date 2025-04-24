from semantic_kernel.functions import kernel_function
import asyncio
from collections import defaultdict
from playwright.async_api import async_playwright
import re
import chainlit as cl

class FitnessPlugin:

    @kernel_function(
        name="get_supported_muscles",
        description="Return a list of supported muscle names for training video search."
    )
    async def get_supported_muscles(self) -> str:
        async with cl.Step(name=f"分析用户意图中...", type="function"):
            pass
        return """
            [
            "Chest", "Back", "Shoulders", "Biceps", "Triceps", 
            "Quadriceps", "Hamstrings", "Glutes", "Calves", "Abs", 
            "Forearms", "Neck", "Traps", "Obliques"
            ]
        """

    @kernel_function(
        name="get_exercises_by_muscle",
        description="Return a list of exercises (with video URLs) for a specific muscle and gender."
    )
    async def get_exercises_by_muscle(self, muscle: str, gender: str) -> str:
        async with cl.Step(name=f"正在进行爬虫获取资料...", type="function"):
            pass
        base_url = f"https://musclewiki.com/exercises/{gender.lower()}/{muscle.lower().replace(' ', '%20')}/"
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
                    "notes": " ",
                    "tips": " "
                })

        return str({
            "muscle": muscle,
            "exercises": exercises
        })

    async def scrape_video_urls(self, url: str) -> list[str]:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,
                args=[
                    "--window-position=100,100",   # 弹窗位置（左上角）
                    "--window-size=1200,800"       # 弹窗大小
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
