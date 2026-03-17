import os
import re
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ==========================================================
# 1. CẤU HÌNH ĐƯỜNG DẪN & TRÌNH DUYỆT BRAVE
# ==========================================================
folder_path = r"D:\DHBK\KHDL\raw data"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

chrome_options = Options()
chrome_options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

print("crawl GearVN...")
driver = webdriver.Chrome(options=chrome_options)

# 4 Phân khúc giá của GearVN
urls = [
    "https://gearvn.com/collections/laptop-hoc-tap-va-lam-viec-duoi-15tr",
    "https://gearvn.com/collections/laptop-van-phong-ban-chay",
    "https://gearvn.com/collections/laptop-hoc-tap-va-lam-viec-tu-15tr-den-20tr",
    "https://gearvn.com/collections/laptop-hoc-tap-va-lam-viec-tren-20-trieu"
]

data_final = []

try:
    for url_goc in urls:
        print(f"\nĐANG QUÉT: {url_goc.split('/')[-1].upper()}")
        
        # Quét 2 trang đầu của mỗi phân khúc để đảm bảo đủ mẫu
        for page in range(1, 3):
            driver.get(f"{url_goc}?page={page}")
            time.sleep(4)
            
            # Cuộn trang từ từ để load hết dữ liệu
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
            time.sleep(1.5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Nhắm vào khung sản phẩm của GearVN (thường là .product-row hoặc .product-item)
            items = soup.select('.product-row') or soup.select('.product-item')
            
            if not items: # Nếu không tìm thấy class, quét đại trà các khối div chứa giá
                items = [div for div in soup.find_all('div') if '₫' in div.text and len(div.text) < 500]

            for item in items:
                raw_text = item.get_text(separator='|').strip()
                lines = [l.strip() for l in raw_text.split('|') if l.strip()]
                
                # Kiểm tra máy hợp lệ
                if any(h in raw_text.upper() for h in ['LAPTOP', 'MACBOOK', 'ASUS', 'HP', 'DELL', 'LENOVO', 'ACER', 'MSI']):
                    
                    ten = lines[0]
                    gia = 0
                    cpu = ram = ssd = vga = "N/A"
                    
                    # Tách thương hiệu
                    list_hang = ['ASUS', 'HP', 'DELL', 'LENOVO', 'ACER', 'MSI', 'MACBOOK', 'GIGABYTE', 'SURFACE']
                    thuong_hieu = next((h for h in list_hang if h in ten.upper()), "Other")
                    
                    for l in lines:
                        l_up = l.upper()
                        if '₫' in l:
                            num = re.sub(r'[^\d]', '', l)
                            if num: gia = int(num)
                        elif any(c in l_up for c in ['CORE', 'RYZEN', 'APPLE M', 'ULTRA']):
                            cpu = l
                        elif 'GB' in l_up and 'RAM' in l_up:
                            # Trích xuất số GB (8, 16, 32...)
                            match = re.search(r'(\d+)', l)
                            ram = match.group(1) if match else l
                        elif any(s in l_up for s in ['SSD', 'HDD', 'Ổ CỨNG']):
                            ssd = l
                        elif any(v in l_up for v in ['RTX', 'GTX', 'GRAPHICS', 'RADEON', 'VGA', 'INTEL IRIS']):
                            vga = l
                    
                    if gia > 3000000:
                        data_final.append({
                            'ten_san_pham': ten,
                            'thuong_hieu': thuong_hieu,
                            'cpu': cpu,
                            'ram_gb': ram,
                            'o_cung_gb': ssd,
                            'vga': vga,
                            'gia_ban': gia
                        })
            
            print(f"Đã gom được {len(data_final)} mẫu...")

    # Xuất file
    df = pd.DataFrame(data_final)
    df.drop_duplicates(subset=['ten_san_pham'], inplace=True)
    
    save_file = os.path.join(folder_path, "gearvn_detailed_data.csv")
    df.to_csv(save_file, index=False, encoding='utf-8-sig')
    
    print("\n" + "="*40)
    print(f"THÀNH CÔNG! Tổng cộng: {len(df)} máy.")
    print(f"File lưu tại: {save_file}")
    print("="*40)
    print(df.head())

except Exception as e:
    print(f"Lỗi: {e}")
finally:
    driver.quit()