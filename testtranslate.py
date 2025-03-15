import pandas as pd
import time
import os
from deep_translator import GoogleTranslator

def translate_text(text, target_lang='vi'):
    try:
        translator = GoogleTranslator(source='en', target=target_lang)
        return translator.translate(text)
    except Exception as e:
        print(f"Lỗi khi dịch: {e}")
        return text

def translate_with_deep_translator(input_file, output_file):
    try:
        print(f"Đang mở tệp đầu vào: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        print(f"Tổng số dòng: {total_lines}")
        
        # Mở file để ghi
        print(f"Đang mở tệp đầu ra: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f_out:
            for idx, line in enumerate(lines, 1):
                translated_text = translate_text(line.strip())
                # Ghi ngay sau khi dịch xong mỗi dòng
                f_out.write(translated_text + '\n')
                f_out.flush()  # Đảm bảo dữ liệu được ghi ngay lập tức
                
                print(f"Dòng: {idx}/{total_lines}", end='\r')
                time.sleep(0.5)
            
        print("\nHoàn thành!")
                
    except Exception as e:
        print(f"Lỗi khi xử lý file: {e}")
        # Hiển thị thông tin chi tiết về lỗi để gỡ lỗi
        import traceback
        traceback.print_exc()

def find_csv_files():
    """Tìm vị trí các tệp CSV trong nhiều thư mục có thể."""
    possible_locations = [
        "data",                    # thư mục data trong thư mục hiện tại
        "./data",                  # tương tự
        "../data",                 # thư mục data ở cấp cao hơn
        "/app/data",               # thư mục data trong thư mục gốc Railway
        "app/data",                # thư mục app/data 
        "./app/data",              # tương tự
        os.path.dirname(__file__), # thư mục chứa script
        "."                        # thư mục hiện tại
    ]
    
    # In thư mục làm việc hiện tại
    cwd = os.getcwd()
    print(f"Thư mục làm việc hiện tại: {cwd}")
    
    # Liệt kê các tệp và thư mục trong thư mục hiện tại
    print("Nội dung thư mục hiện tại:", os.listdir(cwd))
    
    # Kiểm tra tất cả các vị trí có thể cho train.csv và test.csv
    for loc in possible_locations:
        train_path = os.path.join(loc, "train.csv")
        test_path = os.path.join(loc, "test.csv")
        
        train_exists = os.path.exists(train_path)
        test_exists = os.path.exists(test_path)
        
        if train_exists or test_exists:
            print(f"Tìm thấy tệp CSV tại vị trí: {loc}")
            if train_exists:
                print(f" - train.csv: {train_path}")
            if test_exists:
                print(f" - test.csv: {test_path}")
            return loc
    
    # Nếu chưa tìm thấy, hãy kiểm tra các thư mục con của thư mục hiện tại
    print("Tìm kiếm trong các thư mục con...")
    for root, dirs, files in os.walk(cwd):
        if 'train.csv' in files or 'test.csv' in files:
            print(f"Tìm thấy tệp CSV trong thư mục: {root}")
            return root
    
    print("Không tìm thấy tệp CSV ở bất kỳ vị trí nào!")
    return None

def process_all_files():
    """Xử lý cả file train và test"""
    # Tìm vị trí các tệp CSV
    base_dir = find_csv_files()
    
    if not base_dir:
        print("Không thể tìm thấy các tệp CSV. Đang sử dụng 'app/data' mặc định.")
        base_dir = "app/data"
    
    # File train
    train_input = os.path.join(base_dir, "train.csv")
    train_output = os.path.join(base_dir, "train_vietnamese.csv")
    
    # File test
    test_input = os.path.join(base_dir, "test.csv")
    test_output = os.path.join(base_dir, "test_vietnamese.csv")
    
    # Dịch file train
    print("===== BẮT ĐẦU DỊCH FILE TRAIN =====")
    if os.path.exists(train_input):
        translate_with_deep_translator(train_input, train_output)
    else:
        print(f"Không tìm thấy tệp train.csv tại {train_input}")
    
    # Dịch file test
    print("\n===== BẮT ĐẦU DỊCH FILE TEST =====")
    if os.path.exists(test_input):
        translate_with_deep_translator(test_input, test_output)
    else:
        print(f"Không tìm thấy tệp test.csv tại {test_input}")
    
    print("\n===== HOÀN THÀNH DỊCH TẤT CẢ CÁC FILE =====")

# Chạy hàm xử lý tất cả các file
if __name__ == "__main__":
    process_all_files()