import asyncio
from playwright.async_api import async_playwright
from .models import Credential, PostSelection
from asgiref.sync import sync_to_async
import os

async def run_automation(credential_id):
    logs = []
    async with async_playwright() as playwright:
        try:
            # Fetch credential synchronously
            credential = await sync_to_async(Credential.objects.get)(id=credential_id)
            logs.append(f"Starting automation for {credential.email}")

            context = await playwright.chromium.launch_persistent_context(
                user_data_dir="user_data",
                headless=False,
                
            )
            page = context.pages[0] if context.pages else await context.new_page()

            logged_in = False
            try:
                await page.goto("https://www.facebook.com/", timeout=60000)
                await page.wait_for_selector("input[name='email']", timeout=5000)
                logs.append("Logging in...")
                await page.fill("input[name='email']", credential.email)
                await page.fill("input[name='pass']", credential.password)
                await page.click("button[name='login']")
                await page.wait_for_url("https://www.facebook.com/", timeout=180000)
                await asyncio.sleep(5)
                logged_in = True
                logs.append("Login successful. Session saved.")
            except Exception as e:
                logs.append(f"Already logged in or login error: {str(e)}")
                await page.screenshot(path="screenshot.png")

            # Fetch selections with related group and post data
            selections = await sync_to_async(
                lambda: list(
                    PostSelection.objects.filter(credential_id=credential_id, selected=True)
                    .select_related('group', 'post')
                )
            )()
            for index, selection in enumerate(selections):
                group_page = await context.new_page()
                group_url = selection.group.group_url
                group_name = selection.group.group_name
                post_title = selection.post.title
                post_description = selection.post.description
                post_hashtags = selection.post.hashtags
                post_image = selection.post.image

                await group_page.goto(group_url, timeout=120000)
                await group_page.wait_for_load_state('networkidle')
                logs.append(f"Opened group {index + 1}: {group_name} ({group_url})")

                write_xpath = "//div[@role='button']//span[contains(text(), 'Write something')]"
                post_xpath = "//div[@role='textbox' and @contenteditable='true' and contains(@aria-placeholder, 'Create a public post')]"

                await group_page.wait_for_selector(f"xpath={write_xpath}", timeout=150000)
                await group_page.click(f"xpath={write_xpath}")
                logs.append("Clicked 'Write something...'")

                await group_page.wait_for_selector(f"xpath={post_xpath}", timeout=100000)
                post_input = await group_page.query_selector(f"xpath={post_xpath}")
                await post_input.click()
                post_content = f"{post_title}\n\n{post_description}\n\n{post_hashtags}\n\n"
                await post_input.fill(post_content)
                logs.append("Post content filled.")

                if post_image:
                    
                    try:
                        image_path = post_image.path
                        if os.path.exists(image_path):
                            await group_page.set_input_files("input[type='file']", image_path)
                            await asyncio.sleep(5)
                            logs.append(f"Uploaded image: {image_path}")
                            await asyncio.sleep(5)
                        else:
                            logs.append(f" Image file not found at: {image_path}.")
                            post_content += f"\n\n [Image]({post_image.url})"
                    except Exception as e:
                        logs.append(f"Failed to upload image: {str(e)}")

                post_button_xpath = "//div[@role='button' and @aria-label='Post']"
                await group_page.wait_for_selector(f"xpath={post_button_xpath}", timeout=10000)
                await group_page.click(f"xpath={post_button_xpath}")
                logs.append(f"Post {index + 1} submitted!")
                await group_page.screenshot(path=f"screenshot_post_{index + 1}.png")

                if index != len(selections) - 1:
                    logs.append("Waiting 30 seconds before next post...")
                    await asyncio.sleep(30)

            await context.close()
            logs.append("Automation completed successfully.")
            return True, logs
        except Exception as e:
            logs.append(f"Automation failed: {str(e)}")
            return False, logs