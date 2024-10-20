import argparse
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from zenmodel import Processor, BrainContext
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

class XHSScraperProcessor(Processor):
    def __init__(self, number: int = 3, comments: int = 20, replies: int = 50):
        self.number = number
        self.comments = comments
        self.replies = replies
        self.chrome_options = Options()
        self.chrome_options.add_argument("user-data-dir=./User_Data")
        self.driver = None
        self.long_wait = None
        self.wait = None

    def process(self, ctx: BrainContext):
        query = ctx.get_memory("query")
        if not query:
            print("错误：未找到搜索查询")
            return

        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.long_wait = WebDriverWait(self.driver, 60)
        self.wait = WebDriverWait(self.driver, 10)

        try:
            notes_data = self.scrape_xhs(query)
            ctx.set_memory("xhs_data", notes_data)
        finally:
            if self.driver:
                self.driver.quit()

    def scrape_xhs(self, search_content):
        self.driver.get("https://www.xiaohongshu.com/explore")
        print("已打开小红书主页")
        
        print("请扫码登录...")
        search_box = self.long_wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="搜索小红书"]')))
        print("页面已刷新，开始搜索")

        search_box.send_keys(search_content)
        print(f"输入搜索内容: {search_content}")
        search_box.send_keys(Keys.RETURN)
        print("已提交搜索")

        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//section[@class="note-item"]')))
        print("搜索结果加载完成")

        notes_data = []
        notes = self.driver.find_elements(By.XPATH, '//section[@class="note-item"]')[:self.number]
        print(f"找到 {len(notes)} 条笔记")
        print("-" * 20)
    
        for note in notes:
            note_info = self.process_note(note)
            if note_info:
                notes_data.append(note_info)
            print("-" * 20)

        return notes_data

    def process_note(self, note):
        try:
            last_title = note.find_element(By.XPATH, '//div[@class="note-content"]//div[@class="desc"]').text[:10]
        except (NoSuchElementException, StaleElementReferenceException) as e:
            last_title = ""

        note.click()
        try:
            self.wait.until(lambda driver: note.find_element(By.XPATH, '//div[@class="note-content"]//div[@class="desc"]').text[:10] != last_title)
            title = note.find_element(By.XPATH, '//div[@class="note-content"]//div[@class="title"]').text
            author = note.find_element(By.XPATH, '//div[@class="author-container"]//span[@class="username"]').text
            content = note.find_element(By.XPATH, '//div[@class="note-content"]//div[@class="desc"]').text
            like_count = self.driver.find_element(By.CSS_SELECTOR, '#noteContainer > div.interaction-container > div.interactions.engage-bar > div > div > div.input-box > div.interact-container > div > div.left > span.like-wrapper.like-active > span.count').text
        except Exception:
            return None

        print("标题:", title)
        print("作者:", author)
        print("内容:", content)
        print("点赞数量:", like_count)

        note_info = {
            "title": title,
            "author": author,
            "content": content,
            "like_count": like_count,
            "comments": self.process_comments()
        }

        self.driver.back()
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//section[@class="note-item"]')))

        return note_info

    def process_comments(self):
        comments_info = []
        try:
            expanded_comments = 0
            while expanded_comments < self.comments:
                load_more_buttons = self.driver.find_elements(By.XPATH, '//div[contains(text(), "展开")]')
                if not load_more_buttons:
                    break
                for button in load_more_buttons:
                    if expanded_comments >= self.comments:
                        break
                    button.click()
                    expanded_comments += 1
                    self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="parent-comment"]')))
        except Exception as e:
            print("没有更多回复需要展开或找不到展开按钮:", e)

        parent_comments = self.driver.find_elements(By.XPATH, '//div[@class="parent-comment"]')[:self.comments]

        for parent_comment in parent_comments:
            comment_info = self.process_single_comment(parent_comment)
            if comment_info:
                comments_info.append(comment_info)

        return comments_info

    def process_single_comment(self, parent_comment):
        try:
            comment_text = parent_comment.find_element(By.XPATH, './/div[@class="comment-item"]//span[@class="note-text"]').text
            print('评论:', comment_text)

            comment_info = {
                "comment": comment_text,
                "replies": []
            }

            replies = parent_comment.find_elements(By.XPATH, './/div[@class="reply-container"]//span[@class="note-text"]')[:self.replies]
            for reply in replies:
                reply_text = reply.text
                print('回复:', reply_text)
                comment_info["replies"].append(reply_text)

            return comment_info
        except Exception as e:
            print('无法获取评论或回复:', e)
            return None
