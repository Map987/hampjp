import os
import re
import requests
from bs4 import BeautifulSoup

# 网站URL
url = 'https://www.hakuhodody-map.jp/animation/'

# 下载图片的函数
def download_image(image_url, save_folder, txt_file):
    response = requests.get(image_url)
    if response.status_code == 200:
        file_name = os.path.join(save_folder, image_url.split('/')[-1])
        with open(file_name, 'wb') as f:
            f.write(response.content)
        file_size = os.path.getsize(file_name)
        file_size = file_size / (1024 * 1024)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(txt_file, 'a') as tf:
            tf.write(f"{image_url} | {file_size:.1f} MB | {current_time}\n")
        print(f"Downloaded {image_url} to {file_name} | Size: {file_size:.1f} MB")
        return file_name, file_size, current_time
    else:
        print(f"Failed to download {image_url}")
        return None, None, None

# 处理下载原图URL的函数
def process_image_url(image_url):
    # 删除 -scaled 和 -数字x数字
    pattern = r'(-scaled|-[\d]+x[\d]+)(?![\w-])'
    processed_url = re.sub(pattern, '', image_url)
    return processed_url

# 保存图片的文件夹
save_folder = 'downloaded_images'
txt_file = 'downloaded_images.txt'

if not os.path.exists(save_folder):
    os.makedirs(save_folder)

if not os.path.exists(txt_file):
    with open(txt_file, 'w') as tf:
        tf.write("Image URL | File Size | Download Time\n")

# 下载网页内容
response = requests.get(url)
html_content = response.text

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 查找所有指定的a标签
a_tags = soup.find_all('a', href=re.compile(r'https://www\.hakuhodody-map\.jp/lineup/map-\d+'))

# 遍历所有a标签
for a_tag in a_tags:
    # 获取图片链接
    img_tag = a_tag.find('img')
    if img_tag:
        img_url = img_tag.get('src')
        # 处理图片链接
        processed_url = process_image_url(img_url)
        # 下载图片
        download_image(processed_url, save_folder, txt_file)
