import os
import json
import re

# Thư mục chứa các file JSON đầu vào
INPUT_FOLDER = ""
OUTPUT_FOLDER = ""

# Tạo thư mục output nếu chưa có
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Regex nhận diện điều khoản (hỗ trợ nhiều cách viết khác nhau)
CLAUSE_PATTERN = re.compile(r"^(điều\s*\d+[\.\-\: ]+[^\n]*)", re.IGNORECASE)

def process_json_file(file_path, output_path):
    """Xử lý một file JSON và gán nhãn dữ liệu"""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)  # Đọc nội dung JSON (dạng danh sách văn bản)

    labeled_data = []  # Danh sách chứa dữ liệu đã gán nhãn
    current_clause = None  # Biến lưu điều khoản hiện tại
    title_section = {"label": "Title", "text": ""}  # Lưu phần mở đầu
    collecting_title = True  # Cờ kiểm tra xem có đang thu thập phần mở đầu không

    for text in data:
        text = text.strip()  # Xóa khoảng trắng dư thừa
        text_lower = text.lower()

        # Thu thập toàn bộ nội dung từ đầu file cho tới khi gặp điều khoản đầu tiên
        if collecting_title and not CLAUSE_PATTERN.match(text):
            title_section["text"] += " " + text if title_section["text"] else text
        
        # Khi gặp điều khoản đầu tiên, lưu lại tiêu đề và bắt đầu ghi điều khoản
        elif collecting_title and CLAUSE_PATTERN.match(text):
            labeled_data.append(title_section)  # Lưu phần mở đầu vào danh sách
            title_section = None  # Đặt thành None để tránh tiếp tục thu thập
            collecting_title = False  # Dừng thu thập phần mở đầu

            # Tạo điều khoản mới với label là tiêu đề điều khoản
            current_clause = {"label": text, "text": ""}

        # Nếu gặp một điều khoản mới, lưu điều khoản trước đó rồi bắt đầu điều khoản mới
        elif CLAUSE_PATTERN.match(text):
            if current_clause:
                labeled_data.append(current_clause)  # Lưu điều khoản cũ trước khi tạo mới

            # Bắt đầu một điều khoản mới
            current_clause = {"label": text, "text": ""}

        # Nếu vẫn đang trong một điều khoản, tiếp tục nối nội dung
        elif current_clause:
            current_clause["text"] += " " + text

    # Lưu điều khoản cuối cùng vào danh sách (nếu có)
    if current_clause:
        labeled_data.append(current_clause)

    # Ghi dữ liệu đã gán nhãn ra file JSON mới
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(labeled_data, f, ensure_ascii=False, indent=4)

    print(f"✔ Đã xử lý: {file_path} -> {output_path}")

# Lặp qua tất cả các file JSON trong thư mục đầu vào
for filename in os.listdir(INPUT_FOLDER):
    if filename.endswith(".json"):  # Chỉ xử lý file JSON
        input_file_path = os.path.join(INPUT_FOLDER, filename)
        output_file_path = os.path.join(OUTPUT_FOLDER, filename)
        process_json_file(input_file_path, output_file_path)


