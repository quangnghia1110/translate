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
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        print(f"Tổng số dòng: {total_lines}")
        
        # Mở file để ghi với mode 'a' (append)
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

def process_all_files():
    """Xử lý cả file train và test"""
    # Sử dụng đường dẫn tương đối thay vì tuyệt đối
    # Giả sử các file dữ liệu nằm trong thư mục 'data' cùng cấp với script này
    base_dir = os.path.join(os.path.dirname(__file__), "data")
    
    # File train
    train_input = os.path.join(base_dir, "train.csv")
    train_output = os.path.join(base_dir, "train_vietnamese.csv")
    
    # File test
    test_input = os.path.join(base_dir, "test.csv")
    test_output = os.path.join(base_dir, "test_vietnamese.csv")
    
    # Đảm bảo thư mục tồn tại
    os.makedirs(base_dir, exist_ok=True)
    
    # Dịch file train
    print("===== BẮT ĐẦU DỊCH FILE TRAIN =====")
    translate_with_deep_translator(train_input, train_output)
    
    # Dịch file test
    print("\n===== BẮT ĐẦU DỊCH FILE TEST =====")
    translate_with_deep_translator(test_input, test_output)
    
    print("\n===== HOÀN THÀNH DỊCH TẤT CẢ CÁC FILE =====")

# Chạy hàm xử lý tất cả các file
process_all_files()