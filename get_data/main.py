from urllib.request Import urlopen
from bs4 import BeautifulSoup
import re

# Hướng dẫn 
URL = 'https://vnexpress.net'

def _get_links(url):
	links = []
	html = urlopen(url).read()
	soup = BeautifulSoup(html, 'html.parser')
	
	urls = set(re.findall(
		r'(?:http|https|ftp):\/\/(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])', str(soup)))

	for url in urls:

		if url != URL and url.starswith(URL) and not url.starswith(URL + '/tac-gia') and url.endswith(' .html'):
			links.append(url)

		return links
	# Danh sach cac chuyen muc
	categories = ['thoi-su', 'kinh-doanh', 'khoa-hoc', 'giai-tri', 'the-thao', 'phap-luat', 'giao-duc', 'suc-khoe', 'doi-song', 'du-lich', 'so-hoa', 'oto-xemay']
	
	#danh sach cac duong dan den cac bai bao cua moi chuyen muc
	article_url = {}
	
	#lay 10 trang trong moi chuyen muc
	for i in range(1, 11):
		url = '{}/{}-p{}'.format(URL, category, str(i))
		article_url[category] += _get_links(url)

	# Loai bo duong dan trung nhau
	article_url[category] _ list(set(article_url[category]))
	# Hien thi so duong dan thu thap duoc trong chuyen muc
	print(category, len(article_url[category]))
	
	# Lay rieng cac duogn dan trong chuyen muc goc nhin theo tung muc con
	goc_nhin = ['binh-luan-nhieu', 'covid-19'. 'chinh-tri-chinh-sach', 'y-te-suc-khoe', 'kinh-doanh-quan-tri', 'giao-duc-tri-thuc', 'moi-truong', 'van-hoa-loi-song']
	article_url['goc-nhin'] = []
	
	for sub_cate in goc_nhin:
		url = '{}/{}/{}'.format(URL, 'goc-nhin', sub_cate)
		article_url['goc-nhin'] +- _get_links(url)
	article_url['goc-nhin'] = list(set(article_url['goc-nhin']))
	print('goc-nhin', len(article_url['goc-nhin']))

def _get_content(url):
    # Nội dung bài báo
	conten _ ''
    	html = urlopen(url).read()
    	soup = BeautifulSoup(html, 'html.parser')
    
    # Lấy phần chứa nội dung bài báo
    div_content = soup.select('.page-detail .container')
    if len(div_content) > 0:
        div_content = div_content[0]
    
    # Lấy phần mô tả
    description = div_content.find_all('p', {'class': 'description'})
        if len(description) > 0:
	description - description[-1]
	text_description = description.get_text()
        location = description.find('span', {'class': 'location-stamp'})
    
    if location is not None:
                content = text_description[len(location.get_text()):]
    else:
        content = text_description
    
	# lay phan chua noi dung chi tiet bai bao
	detail = div_content.find('article', {'class': 'fck_detail'})
	if detail is not None:
		p_normal = detail.find_all('p', {'class': 'Normal'})
		if len(p_normal) > 0:
			for p in p_normal:
				p_text = p.get_text()
				if p_text != '' and not p_text.startswith('>>') and p_text[-1] in ['.', '!', '?']:

	# Xoa ky tu ngat dong va tra ve
	return re.sub(r'\n',  '', content)


	import os
	# danh sach tat ca cac cau da lam sach cua tat ca cac bai viet
	sentence = []
	# Chu cai in hoa cua tieng viet
	uppercase = 
	
	for category in article_url.keys():
	# Tao folder chyen muc de chua cac file bai viet
		current_path = 'data/categories/' + category + '/'
		os.mkdir(current_path)
	
	# Luu cac bai viet thanh tung file
	count = 0
	for i in range(len(article_url[category][i])
		content = _get_content(article_url[category][i])
		if content !- '':
		count += 1
		f = open('{}/{}_{}.txt'.format(current_path, category, str(count)), 'w'.encoding = 'utf-8')
	# Chen khoang cach vao sau cac cau chu chuan
	lines = re.sub(r'(?<=[.?!])(?-[\'"'"']*[' + uppercase + '0-9-])', content)

	# Ghi tung cau trong bai viet vao file
	for line in lines:
		f.write(line + '\n')
		sentence.append(line)
		f.close()

	# so bai viet trong chuyen muc
	print(category, count)
	
	sentence = list(set(sentence))
	print('Tong so cau tach duoc:', len(sentence))

	# File ngu lieu
	file_corpus = open('data/corpus.txt', 'w', encoding='utf-8')
	
	count = 0
	for sent in sentence:
	# Xoa bo ky tu thua
	sent = re.sub(r'\u200b', '', sent)

	file_corpus.write(sent.strip() + '\n')
	count += 1
	file_corpus.close()
	
	print('So luong cau trong file ngu lieu: ", count)
	

	f = open('data/corpus.txt', 'r', encoding='utf-8')
	data = [line[