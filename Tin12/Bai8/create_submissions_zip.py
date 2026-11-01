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
    # Bỏ dấu tiếng Việt
    text = unicodedata.normalize('NFD', text)
    text = re.sub(r'[\u0300-\u036f]', '', text)
    text = text.replace('đ', 'd').replace('Đ', 'D')
    # Thay ký tự đặc biệt thành dấu gạch dưới
    text = re.sub(r'[^a-zA-Z0-9]+', '_', text).strip('_')
    return text or 'HocSinh'

def make_submissions_zip(output_zip_path=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(base_dir, 'data', 'submissions_hd3.json')
    
    if not os.path.exists(data_file):
        print("Data file not found:", data_file)
        return None

    with open(data_file, 'r', encoding='utf-8') as f:
        try:
            submissions = json.load(f)
        except Exception as e:
            print("Error loading JSON:", e)
            submissions = []

    if not submissions:
        print("No submissions found.")

    if not output_zip_path:
        today_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_zip_path = os.path.join(base_dir, 'data', f'Bai8_HD3_TatCaBaiLam_{today_str}.zip')

    os.makedirs(os.path.dirname(output_zip_path), exist_ok=True)

    with zipfile.ZipFile(output_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        # 1. Thêm file Tổng quan lớp học (TongKet_LopHoc.txt)
        overview_lines = [
            "=" * 60,
            "TRƯỜNG THTH - DHSP • BÀI 8: ĐỊNH DẠNG VĂN BẢN",
            "BẢNG TỔNG HỢP NỘP BÀI THỰC HÀNH HOẠT ĐỘNG 3 (30 PHÚT)",
            f"Thời điểm xuất file: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            f"Tổng số bài nộp: {len(submissions)} học sinh",
            "=" * 60,
            "",
            f"{'STT':<4} | {'HỌ VÀ TÊN':<25} | {'LỚP':<6} | {'SỐ MÁY':<7} | {'THỜI GIAN NỘP':<18} | {'THƯ MỤC LƯU TRỮ'}",
            "-" * 95
        ]

        seen_folders = set()
        for idx, sub in enumerate(submissions, 1):
            name = sub.get('studentName', 'Học sinh')
            cls = sub.get('className', '12A')
            stt = str(sub.get('studentNumber', '') or idx).zfill(2)
            time_str = sub.get('submittedAt', '')
            
            # Tên thư mục riêng cho từng học sinh
            base_folder = f"{slugify(cls)}_{stt}_{slugify(name)}"
            folder_name = base_folder
            dup_count = 1
            while folder_name in seen_folders:
                dup_count += 1
                folder_name = f"{base_folder}_{dup_count}"
            seen_folders.add(folder_name)

            overview_lines.append(f"{idx:<4} | {name:<25} | {cls:<6} | {stt:<7} | {time_str:<18} | {folder_name}/")

            files = sub.get('files', {})
            # File Bài 1
            b1_code = files.get('bai1', {}).get('code', '')
            zf.writestr(f"{folder_name}/Bai1.html", b1_code.encode('utf-8'))

            # File Bài 2
            b2_code = files.get('bai2', {}).get('code', '')
            zf.writestr(f"{folder_name}/Bai2.html", b2_code.encode('utf-8'))

            # File Bài 3
            b3_code = files.get('bai3', {}).get('code', '')
            zf.writestr(f"{folder_name}/Bai3.html", b3_code.encode('utf-8'))

            # File Thông tin chi tiết của học sinh đó
            student_info = [
                "TRƯỜNG THTH - DHSP • BÀI 8: ĐỊNH DẠNG VĂN BẢN",
                "PHIẾU THÔNG TIN BÀI LÀM HỌC SINH (HĐ 3: LUYỆN TẬP)",
                "-" * 50,
                f"Họ và tên:        {name}",
                f"Lớp:              {cls}",
                f"Số máy / STT:     {stt}",
                f"Thời gian nộp:    {time_str}",
                f"Mã biên nhận:     {sub.get('id', '')}",
                "-" * 50,
                "DANH SÁCH 3 TỆP HTML ĐÍNH KÈM:",
                "1. Bai1.html - Bài toán biện luận phương trình bậc 2",
                "2. Bai2.html - Sử dụng thẻ nhấn mạnh strong, em, b, i, mark, u",
                "3. Bai3.html - Tờ rơi giới thiệu dịch vụ Internet tốc độ cao",
                "-" * 50
            ]
            zf.writestr(f"{folder_name}/ThongTin_BaiLam.txt", "\n".join(student_info).encode('utf-8'))

        # Lưu file tổng hợp ở thư mục gốc của zip
        zf.writestr("00_TONG_KET_LOP_HOC.txt", "\n".join(overview_lines).encode('utf-8'))

    print(f"SUCCESS: Created ZIP with {len(submissions)} student folders at {output_zip_path}")
    return output_zip_path

if __name__ == '__main__':
    out_path = sys.argv[1] if len(sys.argv) > 1 else None
    make_submissions_zip(out_path)

