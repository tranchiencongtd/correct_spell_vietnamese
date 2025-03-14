from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os

# Duong dan
URL = 'https://vnexpress.net'

def get_links(url):
	links = []
	html = urlopen(url).read().decode('utf-8')
	soup = BeautifulSoup(html, 'html.parser')

	urls = set(re.findall(r'href=["\'](https?://[^"\']+\.html)["\']', str(soup)))

	for url in urls:
		if url != URL and url.startswith(URL) and not url.startswith(URL + '/tac-gia') and url.endswith('.html'):
			links.append(url)
			print(url)

	return links

def get_link_by_catgories():
	# Danh sách các chuyên mục
	# categories = ['thoi-su', 'kinh-doanh', 'cong-nghe', 'khoa-hoc', 'suc-khoe',
	# 			  'the-thao', 'giai-tri', 'phap-luat', 'giao-duc', 'doi-song', 'du-lich', 'tam-su']

	categories = ['thoi-su']

	# Danh sách các đường dẫn bài báo
	article_urls = {category: [] for category in categories}

	# Lấy link từ từng chuyên mục
	for category in categories:
		for i in range(1, 2):  # Lấy 10 trang trong mỗi chuyên mục
			url = f'{URL}/{category}-p{i}'
			article_urls[category] += get_links(url)

		# Loại bỏ đường dẫn trùng nhau
		article_urls[category] = list(set(article_urls[category]))

		# Hiển thị số lượng đường dẫn thu thập được
		print('Số lượng đường dẫn đã thu thập:')
		print(category, len(article_urls[category]))
	return article_urls

def get_article_content(url):
	try:
		content = ''
		html = urlopen(url).read()
		soup = BeautifulSoup(html, 'html.parser')

		# Lấy phần chứa nội dung bài báo
		div_content = soup.select('.page-detail .container')
		if not div_content:
			return "Không tìm thấy nội dung bài báo."

		div_content = div_content[0]

		# Lấy phần mô tả
		# description = div_content.find_all('p', {'class': 'description'})
		# if description:
		# 	description = description[-1]
		# 	text_description = description.get_text(strip=True)
		# 	location = description.find('span', {'class': 'location-stamp'})
		#
		# 	if location:
		# 		content = text_description[len(location.get_text()):]
		# 	else:
		# 		content = text_description

		# Lấy phần chi tiết bài báo
		detail = div_content.find('article', {'class': 'fck_detail'})
		if detail:
			p_normal = detail.find_all('p', {'class': 'Normal'})
			for p in p_normal:
				p_text = p.get_text(strip=True)
				if p_text and not p_text.startswith('>>') and p_text[-1] in ['.', '!', '?']:
					content += " " + p_text

		# Xóa ký tự ngắt dòng và trả về nội dung
		return content

	except Exception as e:
		print(f"Lỗi khi lấy nội dung từ {url}: {e}")
		return None

def split_sentences(text):
    """
    Tách nội dung bài viết thành các câu dựa trên dấu câu (., ?, !).
    Xử lý trường hợp viết tắt để tránh cắt câu sai.
    """
    # Xử lý một số trường hợp viết tắt để tránh bị tách sai
    text = re.sub(r'(?<!\w)(TP)\.(?=\w)', r'\1-', text)  # TP.HCM -> TP-HCM
    text = re.sub(r'(?<!\w)(v)\.(v)\.(?=\W)', r'\1-\2', text)  # v.v. -> v-v

    # Tách câu dựa trên dấu chấm (.), chấm hỏi (?), chấm than (!)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Khôi phục lại các dấu chấm bị thay thế
    sentences = [s.replace('TP-', 'TP.').replace('v-v', 'v.v.') for s in sentences]

    return [s.strip() for s in sentences if s.strip()]  # Loại bỏ khoảng trắng dư thừa

def save_cleaned_articles():
	article_urls = get_link_by_catgories()
	# # Chữ cái in hoa tiếng Việt
	# uppercase = "AÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬBCCDĐEÈÉẺẼẸÊỀẾỂỄỆFGHIÌÍỈĨỊJKLMMNOÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢPQRSTUÙÚỦŨỤƯỪỨỬỮỰVWXYỲÝỶỸỴZ"
	#
	# # Danh sách tất cả các câu đã làm sạch của tất cả các bài viết
	sentences = []

	for category in article_urls.keys():
		# Tạo folder chuyên mục để chứa các file bài viết
		current_path = f'data/categories/{category}/'
		os.makedirs(current_path, exist_ok=True)

		# Lưu các bài viết thành từng file
		count = 0
		for i in range(len(article_urls[category])):
			content = get_article_content(article_urls[category][i])

			if content != '':
				count += 1
				file_path = f"{current_path}/{category}_{count}.txt"

				# Tách bài viết thành từng câu
				lines = split_sentences(content)

				# Ghi từng câu trong bài viết vào file và lưu vào danh sách câu
				with open(file_path, 'w', encoding='utf-8') as f:
					for line in lines:
						f.write(line + '\n')
						sentences.append(line)

		# Số bài viết trong chuyên mục
		print(f'Số bài viết của {category} số lượng: {count}')

	# Loại bỏ các câu trùng lặp
	sentences = list(set(sentences))
	print('Tổng số câu tách được:', len(sentences))

	# File ngữ liệu
	file_corpus = open('data/corpus.txt', 'w', encoding='utf-8')

	count = 0  # Biến đếm số câu

	for sent in sentences:
		# Xóa ký tự thừa (ký tự zero-width)
		sent = re.sub(r'\s+', ' ', sent)

		# Ghi câu vào file (loại bỏ khoảng trắng thừa)
		file_corpus.write(sent.strip() + '\n')
		count += 1  # Tăng biến đếm

	# Đóng file sau khi hoàn tất
	file_corpus.close()

	# In số lượng câu trong file ngữ liệu
	print(f"Số lượng câu trong file dữ liêu: {count}")

if __name__ == '__main__':
	save_cleaned_articles()

