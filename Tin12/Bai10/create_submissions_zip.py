import os
import json
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HD3_DIR = os.path.join(BASE_DIR, "data", "submissions_hd3")
HD3_DATA_FILE = os.path.join(BASE_DIR, "data", "submissions_hd3.json")
OUTPUT_ZIP = os.path.join(BASE_DIR, "Bai10_HD3_TatCaBaiLam_THTH_DHSP.zip")


def create_zip():
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        if os.path.exists(HD3_DIR):
            for fname in sorted(os.listdir(HD3_DIR)):
                if fname.endswith(".html"):
                    zf.write(os.path.join(HD3_DIR, fname), arcname=os.path.join("BaiLam_Bai10", fname))
        if os.path.exists(HD3_DATA_FILE):
            with open(HD3_DATA_FILE, "r", encoding="utf-8") as f:
                subs = json.load(f)
            lines = [f"BẢNG TỔNG HỢP BÀI THỰC HÀNH - BÀI 10: TẠO LIÊN KẾT (THTH-DHSP)", "=" * 60]
            for i, s in enumerate(subs, 1):
                lines.append(
                    f"{i}. [{s.get('className','')} - {s.get('studentNumber','')}] "
                    f"{s.get('studentName','')} | Tiêu chí: {s.get('criteriaCount',0)}/8 | Nộp: {s.get('submittedAt','')}"
                )
            zf.writestr("TongKet_LopHoc_Bai10.txt", "\n".join(lines))
    return OUTPUT_ZIP


if __name__ == "__main__":
    print("Created:", create_zip())
