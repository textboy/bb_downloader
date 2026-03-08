import eel
import yt_dlp
import os
import threading

# 初始化 web 目录
eel.init('web')

@eel.expose
def download_tasks(urls):
    for url in urls:
        if url.strip():
            # 开启新线程下载，防止 UI 卡死
            threading.Thread(target=run_yt_dlp, args=(url.strip(),)).start()

def run_yt_dlp(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookies_from_browser': 'chrome',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        eel.notify_js(f"下载完成: {url}")
    except Exception as e:
        eel.notify_js(f"下载失败: {str(e)}")

# 启动程序（窗口模式）
eel.start('index.html', size=(500, 700))
