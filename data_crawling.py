import requests
from bs4 import BeautifulSoup
import json
import re

# URL trang web cần crawl
URL = "https://thuvienphapluat.vn/van-ban/Bat-dong-san/Thong-tu-11-2021-TT-BTNMT-Dinh-muc-kinh-te-ky-thuat-lap-quy-hoach-ke-hoach-su-dung-dat-483793.aspx"

# Hàm gửi request và lấy HTML
def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error {response.status_code}: Unable to fetch page")
        return None

# Hàm làm sạch văn bản: loại bỏ \r, \n, \t và các khoảng trắng thừa, chuyển thành chữ thường
def clean_text(text):
    text = re.sub(r'[\r\n\t]+', ' ', text)  # Loại bỏ \r, \n, \t thay bằng khoảng trắng
    text = re.sub(r'\s+', ' ', text).strip()  # Xóa khoảng trắng thừa
    return text.lower()  # 🔹 Chuyển thành chữ thường

# Hàm phân tích nội dung VBPL và lọc <p> theo vị trí
def parse_phapluat_page(html, start_index=0, end_index=None):
    soup = BeautifulSoup(html, "html.parser")

    # Tìm phần nội dung chính của văn bản pháp luật
    content_div = soup.find("div", {"id": "ctl00_Content_ThongTinVB_divNoiDung"})
    if not content_div:
        print("Không tìm thấy nội dung bài viết")
        return None

    #  Lấy tất cả các thẻ <p> trong phạm vi mong muốn
    all_paragraphs = content_div.find_all("p")
    filtered_paragraphs = all_paragraphs[start_index:end_index]  # Lọc theo vị trí

    #  Lưu nội dung <p> vào danh sách, loại bỏ ký tự không mong muốn và chuyển thành chữ thường
    extracted_content = [clean_text(p.get_text()) for p in filtered_paragraphs if p.get_text(strip=True)]

    return extracted_content

# Hàm lưu dữ liệu vào file JSON
def save_to_json(data, filename="TT47_1.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Chạy quá trình crawl với lọc vị trí <p>
html_content = get_html(URL)
if html_content:
    structured_data = parse_phapluat_page(html_content, start_index=4, end_index=None)  #  Điều chỉnh phạm vi
    save_to_json(structured_data)
    
