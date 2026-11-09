import os
import sys
import json
import zipfile
import re
import unicodedata
from datetime import datetime

def slugify(text):
    if not text:
        return 'HocSinh'
    text = unicodedata.normalize('NFD', text)
    text = re.sub(r'[\u0300-\u036f]', '', text)
    text = text.replace('đ', 'd').replace('Đ', 'D')
    text = re.sub(r'[^a-zA-Z0-9]+', '_', text).strip('_')
    return text or 'HocSinh'

def make_submissions_zip(output_zip_path=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(base_dir, 'data', 'submissions_hd3.json')
    hd3_dir = os.path.join(base_dir, 'data', 'submissions_hd3')
    
    if not os.path.exists(data_file):
        print("Data file not found:", data_file)
        return None

    with open(data_file, 'r', encoding='utf-8') as f:
        try:
            submissions = json.load(f)
        except Exception as e:
            print("Error loading JSON:", e)
            submissions = []

    if not output_zip_path:
        today_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_zip_path = os.path.join(base_dir, 'data', f'Bai9_HD3_TatCaBaiLam_{today_str}.zip')

    os.makedirs(os.path.dirname(output_zip_path), exist_ok=True)

    with zipfile.ZipFile(output_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        # 1. Thêm file Tổng quan lớp học (TongKet_LopHoc.txt)
        overview_lines = [
            "=" * 70,
            "TRƯỜNG THTH - DHSP • BÀI 9: TẠO DANH SÁCH, BẢNG",
            "BẢNG TỔNG HỢP NỘP BÀI THỰC HÀNH HOẠT ĐỘNG 3 (CLB.html)",
            f"Thời điểm xuất file: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            f"Tổng số bài nộp: {len(submissions)} học sinh",
            "=" * 70,
            "",
            f"{'STT':<4} | {'HỌ VÀ TÊN':<25} | {'LỚP':<6} | {'SỐ MÁY':<7} | {'THỜI GIAN NỘP':<18} | {'TÊN FILE LƯU'}",
            "-" * 95
        ]

        seen_files = set()
        for idx, sub in enumerate(submissions, 1):
            name = sub.get('studentName', 'Học sinh')
            cls = sub.get('className', '12A1')
            num = sub.get('studentNumber', 'N/A')
            sub_time = sub.get('submittedAt', '')
            filename = sub.get('filename', f"{cls}_{slugify(num)}_{slugify(name)}_CLB.html")

            overview_lines.append(f"{idx:<4} | {name:<25} | {cls:<6} | {num:<7} | {sub_time:<18} | {filename}")

            file_path = os.path.join(hd3_dir, filename)
            if os.path.exists(file_path):
                zf.write(file_path, arcname=os.path.join("BaiLam_HocSinh", filename))
                seen_files.add(filename)
            elif sub.get('code'):
                zf.writestr(os.path.join("BaiLam_HocSinh", filename), sub.get('code'))
                seen_files.add(filename)

        overview_text = "\n".join(overview_lines)
        zf.writestr("TongKet_LopHoc_Bai9.txt", overview_text.encode('utf-8'))

    print(f"✓ Đã tạo thành công file zip: {output_zip_path}")
    return output_zip_path

if __name__ == '__main__':
    make_submissions_zip()
