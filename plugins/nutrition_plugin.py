import asyncio
import json
from typing import List
from playwright.async_api import async_playwright
from semantic_kernel.functions import kernel_function
import chainlit as cl

class NutritionPlugin:

    @kernel_function(
        name="fetch_recipe_urls_by_keyword",
        description="Search for recipe URLs from allrecipes.com using a keyword."
    )
    async def fetch_recipe_urls_by_keyword(self, keyword: str) -> List[str]:
        url = f"https://www.allrecipes.com/search?q={keyword}"
        print(f"🔍 Searching recipes for keyword: {keyword}")
        recipe_urls = []

        async with cl.Step(name=f"Fetching recipes for: {keyword}", type="function"):
            pass

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)
            await page.wait_for_load_state("domcontentloaded")

            # Scroll to trigger lazy loading
            for _ in range(7):
                await page.evaluate("window.scrollBy(0, 500)")
                await asyncio.sleep(0.5)

            anchors = await page.query_selector_all("a.mntl-card-list-card--extendable")
            for a in anchors:
                href = await a.get_attribute("href")
                if href and "/recipe/" in href:
                    recipe_urls.append(href)

            await browser.close()

        print(f"✅ Found {len(recipe_urls)} recipes.")
        return list(set(recipe_urls))

    @kernel_function(
        name="extract_recipe_from_url",
        description="Extract a structured recipe in render block format from a single recipe URL."
    )
    async def extract_recipe_from_url(self, url: str) -> str:
        async with cl.Step(name=f"Web Searching Start..", type="function"):
            pass
        print(f"📥 Extracting recipe from: {url}")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)
            await page.wait_for_load_state("domcontentloaded")

            # Scroll to trigger lazy loading
            for _ in range(20):
                await page.evaluate("window.scrollBy(0, 1000)")
                await asyncio.sleep(0.2)

            render = []

            # Extract title
            title = "Untitled Recipe"
            for selector in ["h1.article-heading", "h1.headline.heading-content", "h1.headline"]:
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    title = await page.text_content(selector)
                    if title:
                        title = title.strip()
                        break
                except:
                    continue

            render.append({
                "type": "text_block",
                "title": title,
                "props": {
                    "content": "A delicious recipe fetched from the web. Great for meal ideas!"
                }
            })

            # Extract ingredients
            ingredients = []
            items = await page.query_selector_all("li.mm-recipes-structured-ingredients__list-item")
            for item in items:
                txt = await item.text_content()
                if txt:
                    ingredients.append(txt.strip())

            if ingredients:
                render.append({
                    "type": "text_block",
                    "title": "Ingredients",
                    "props": {
                        "content": "\n".join(f"- {i}" for i in ingredients)
                    }
                })

            # Extract preparation steps with images
            step_blocks = await page.query_selector_all("li.comp.mntl-sc-block-startgroup")
            for idx, li in enumerate(step_blocks):
                step_note = ""
                step_img = None

                img = await li.query_selector("img")
                if img:
                    step_img = await img.get_attribute("src")

                p = await li.query_selector("p")
                if p:
                    step_note = (await p.text_content()).strip()

                if step_note or step_img:
                    render.append({
                        "type": "image_note_block",
                        "title": f"Step {idx+1}",
                        "props": {
                            "imageUrl": step_img or "",
                            "note": step_note
                        }
                    })

            # Extract nutrition information
            nutrition_lines = []
            rows = await page.query_selector_all("table.mm-recipes-nutrition-facts-summary__table tr")
            for row in rows:
                cells = await row.query_selector_all("td")
                if len(cells) == 2:
                    val = await cells[0].text_content()
                    label = await cells[1].text_content()
                    if val and label:
                        nutrition_lines.append(f"{label.strip()}: {val.strip()}")

            if nutrition_lines:
                render.append({
                    "type": "text_block",
                    "title": "Nutrition Facts",
                    "props": {
                        "content": "\n".join(nutrition_lines)
                    }
                })

            # Remove invalid blocks: empty props or all fields empty
            render = [
                block for block in render
                if block.get("props") and any(block["props"].get(k) for k in block["props"])
            ]

            await browser.close()
            return json.dumps({"render": render}, indent=2)
