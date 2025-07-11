# Bắt đầu từ một "image" Python 3.10 chính thức
FROM python:3.10-slim

# Đặt thư mục làm việc bên trong container là /app
WORKDIR /app

# Sao chép file requirements vào trước để tận dụng cache của Docker
COPY requirements.txt .

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ code còn lại của bạn vào thư mục làm việc
COPY . .

# Lệnh sẽ được chạy khi container khởi động
CMD ["python", "bot.py"]
