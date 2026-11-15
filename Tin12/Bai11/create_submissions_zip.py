import os
import json
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HD3_DIR = os.path.join(BASE_DIR, "data", "submissions_hd3")
HD3_DATA_FILE = os.path.join(BASE_DIR, "data", "submissions_hd3.json")
OUTPUT_ZIP = os.path.join(BASE_DIR, "Bai11_HD3_TatCaBaiLam_THTH_DHSP.zip")


def create_zip():
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        if os.path.exists(HD3_DIR):
            for root_dir, _, files in sorted(os.walk(HD3_DIR)):
                for fname in sorted(files):
                    if fname.endswith((".html", ".htm")):
                        full_path = os.path.join(root_dir, fname)
                        rel_path = os.path.relpath(full_path, HD3_DIR)
                        zf.write(full_path, arcname=os.path.join("BaiLam_Bai11", rel_path))
        if os.path.exists(HD3_DATA_FILE):
            with open(HD3_DATA_FILE, "r", encoding="utf-8") as f:
                subs = json.load(f)
            lines = [f"BẢNG TỔNG HỢP BÀI THỰC HÀNH - BÀI 11: CHÈN TỆP TIN ĐA PHƯƠNG TIỆN VÀ KHUNG NỘI TUYẾN VÀO TRANG WEB (THTH-DHSP)", "=" * 60]
            for i, s in enumerate(subs, 1):
                lines.append(
                    f"{i}. [{s.get('className','')} - {s.get('studentNumber','')}] "
                    f"{s.get('studentName','')} | Tiêu chí: {s.get('criteriaCount',0)}/8 | Nộp: {s.get('submittedAt','')}"
                )
            zf.writestr("TongKet_LopHoc_Bai11.txt", "\n".join(lines))
    return OUTPUT_ZIP


if __name__ == "__main__":
    print("Created:", create_zip())
