### 📂 Cấu trúc thư mục dự án

09 - Phan tich gia ban Laptop dua tren cau hinh/
├── README.md                 # Hướng dẫn quy trình và cách chạy chương trình
├── requirements.txt          # Danh sách thư viện cần cài đặt
├── crawl_code/               # Mã nguồn thu thập dữ liệu
│   └── gearvn_crawl.py       
├── raw data/                 # Thư mục chứa dữ liệu thô
│   ├── dataset_chotot_api.csv
│   ├── dataset_phongvu_full_selenium.csv
│   ├── gearvn_detailed_data.csv
│   ├── kimlongcenter_final_data.csv
│   └── laptop_full_dataset_final.csv
├── clean data/               # Thư mục chứa dữ liệu qua các bước xử lý
│   ├── laptop_cleaned_missing_data.csv
│   ├── laptop_handled_outliers.csv
│   ├── laptop_master_final_processed.csv
│   └── laptop_robust_scaled.csv
└── notebooks/                # File Notebook phân tích chi tiết
    └── khdl.ipynb
    └── khdl.ipynb

1. Cài đặt môi trường
   pip install -r requirements.txt
    - yêu cầu: Python >= 3.8
2. Thu thập dữ liệu thô
    - Công cụ: requests, beautifulsoup4, pandas.
    - Cách thức: về gearvn, crawl bằng máy local, kim long, phong vũ, chợ tốt được crawl trên colab: https://colab.research.google.com/drive/15-bvzd8NsTbeq4ki4ZxcrFd_O0k0YnBE?usp=sharing
    - Kết quả: Dữ liệu thô được lưu tại raw data với hơn 1000 mẫu (1958 mẫu)
  
3. Phân tích và Tiền xử lý dữ liệu (Notebook)
Mở file notebook/khdl.ipynb bằng Jupyter Notebook hoặc VS Code và chạy các Cell theo thứ tự:
 - Phát biểu bài toán:  Xác định bài toán Hồi quy (Regression) để dự đoán giá bán Y
 - Làm sạch dữ liệu: Xử lý giá trị thiếu (Missing values), chuẩn hóa kiểu dữ liệu và trực quan hóa sự thay đổi phân phối trước/sau khi xử lý.
 - Feature Engineering: - Trích xuất đặc trưng từ văn bản (CPU dòng H, Card đồ họa rời, Màn hình cao cấp).
                        - Phân loại dòng máy (Luxury Line) dựa trên tên sản phẩm.
 - Trực quan hóa đa biến: - Sử dụng Heatmap, lmplot để tìm mối quan hệ giữa cấu hình và giá.
 - Kết luận: Đánh giá tính khả thi của tập dữ liệu đối với việc xây dựng mô hình.

Kết quả đạt được
Dữ liệu sạch: File clean data/laptop_master_final_processed.csv chứa đặc trưng quan trọng nhất, sẵn sàng cho mô hình hóa.
Tính khả thi: Dữ liệu có sự phân hóa rõ rệt, các đặc trưng xây dựng có tương quan cao với biến mục tiêu (Giá bán).
