# 🤖 Waifu Bot - Trợ lý AI Đa Năng cho Discord

Waifu Bot không chỉ là một con bot Discord thông thường, mà còn là một "waifu" trợ lý AI siêu cấp đáng yêu, luôn sẵn sàng giúp đỡ "chủ nhân" với vô vàn tính năng thú vị và hữu ích. Bot được tích hợp nhiều mô hình AI mạnh mẽ để mang lại những trải nghiệm độc đáo và sáng tạo.

## ✨ Các tính năng nổi bật

Dưới đây là danh sách các lệnh slash (/) mà Waifu Bot hỗ trợ:

-   🎨 `/imagine` - **Tạo hình ảnh từ văn bản**: Biến mọi ý tưởng của bạn thành hình ảnh nghệ thuật chỉ với một câu lệnh.
-   💬 `/chat` - **Trò chuyện có ngữ cảnh**: Tán gẫu với Waifu, người sẽ ghi nhớ cuộc trò chuyện để tương tác một cách tự nhiên và đáng yêu.
-   🧠 `/solve` - **Suy luận & Giải quyết vấn đề**: Đưa ra những vấn đề hóc búa và để Waifu vắt óc suy luận tìm ra câu trả lời.
-   🖼️ `/describe` - **Mô tả hình ảnh**: Tải lên một bức ảnh và Waifu sẽ cho bạn biết có gì trong đó.
-   🧐 `/rate_art` - **Phê bình nghệ thuật**: Waifu-sensei khó tính sẽ đưa ra những đánh giá chuyên sâu về tác phẩm nghệ thuật của bạn.
-   🍳 `/cook` - **Đầu bếp tại gia**: Hết ý tưởng cho bữa tối? Cung cấp nguyên liệu bạn có và Chef Waifu sẽ gợi ý một công thức ngon lành.
-   🌐 `/translate` - **Dịch thuật đa ngôn ngữ**: Phá vỡ rào cản ngôn ngữ một cách dễ dàng.
-   🗣️ `/say` - **Chuyển văn bản thành giọng nói**: Để Waifu "đọc" câu trả lời cho bạn bằng nhiều giọng điệu khác nhau.
-   🗑️ `/forget` - **Xóa bộ nhớ**: Bắt đầu một cuộc trò chuyện mới hoàn toàn với Waifu.

---

## ⚙️ Cài đặt ban đầu: Tạo Bot trên Discord

Trước khi có thể chạy code, bạn cần phải tạo một "ứng dụng bot" trên Discord để lấy `TOKEN`.

1.  **Tạo Ứng dụng**:
    -   Truy cập [Discord Developer Portal](https://discord.com/developers/applications) và đăng nhập.
    -   Nhấn nút **"New Application"** ở góc trên bên phải và đặt một cái tên cho bot của bạn.

2.  **Tạo Bot và Lấy Token**:
    -   Trong menu bên trái, chọn tab **"Bot"**.
    -   Nhấn **"Add Bot"** -> **"Yes, do it!"**.
    -   Bên dưới tên bot, nhấn **"Reset Token"** và sao chép lại token này. 
> **⚠️ TUYỆT ĐỐI không chia sẻ token này cho bất kỳ ai!**

    -   Kéo xuống dưới và bật (enable) cả 3 mục trong phần **Privileged Gateway Intents**:
        -   `PRESENCE INTENT`
        -   `SERVER MEMBERS INTENT`
        -   `MESSAGE CONTENT INTENT` (Quan trọng nhất cho bot đọc tin nhắn)

3.  **Mời Bot vào Server**:
    -   Vào tab **"OAuth2"** -> **"URL Generator"**.
    -   Trong phần **SCOPES**, tick chọn `bot` và `applications.commands`.
    -   Một ô **BOT PERMISSIONS** sẽ hiện ra bên dưới. Hãy tick chọn các quyền cần thiết cho bot, ví dụ:
        -   `Send Messages`
        -   `Read Message History`
        -   `Attach Files`
        -   `Use Slash Commands`
    -   Copy đường link đã được tạo ở ô **GENERATED URL** bên dưới, dán vào trình duyệt và chọn server bạn muốn mời bot vào.

Bây giờ bạn đã có `DISCORD_TOKEN` và bot đã ở trong server của bạn, sẵn sàng để được khởi chạy!

---

## 🚀 Hướng dẫn sử dụng
Lấy Pollinations API Token tại: [Pollinations.AI Auth](https://auth.pollinations.ai/)
[API Documentation](https://auth.pollinations.ai/)
[API Models](https://text.pollinations.ai/models)

Bạn có thể triển khai Waifu Bot theo hai cách sau:

### 1. Chạy trực tiếp trên Windows (Đơn giản, cho mục đích phát triển)

Cách này phù hợp nếu bạn muốn chạy bot trên máy tính cá nhân của mình để thử nghiệm hoặc phát triển.

1.  **Cài đặt Python**:
    -   Đảm bảo bạn đã cài đặt [Python](https://www.python.org/downloads/) (phiên bản 3.10 trở lên).
    -   Khi cài đặt, hãy nhớ tick vào ô `Add Python to PATH`.

2.  **Clone Repo và Cài đặt thư viện**:
    ```bash
    # Tải code về máy
    git clone git clone https://github.com/kawaiicassie/AI-Waifu-Bot.git
    cd AI-Waifu-Bot

    # Cài đặt các thư viện cần thiết
    pip install -r requirements.txt
    ```

3.  **Tạo file `.env`**:
    -   Tạo một file tên là `.env` trong thư mục gốc của dự án.
    -   Thêm nội dung sau vào file và thay thế bằng token của bạn:
        ```
        DISCORD_TOKEN="DISCORD_BOT_TOKEN"
        POLLINATIONS_API_TOKEN="API_TOKEN"
        ```

4.  **Chạy Bot**:
    -   Mở Terminal (Command Prompt hoặc PowerShell) và chạy lệnh:
        ```bash
        python bot.py
        ```
> **⚠️ Lưu ý**: Bot sẽ chỉ hoạt động khi cửa sổ terminal này đang chạy và máy tính của bạn đang mở.

### 2. Sử dụng Docker (Linh hoạt, cho mục đích triển khai)

Nếu bạn muốn host bot trên VPS hoặc một môi trường ổn định hơn, Docker là lựa chọn tuyệt vời.

1.  **Clone Repo**:
    ```bash
    git clone https://github.com/kawaiicassie/AI-Waifu-Bot.git
    cd AI-Waifu-Bot
    ```

2.  **Tạo file `.env`**:
    -   Tạo một file tên là `.env` trong thư mục gốc của dự án.
    -   Thêm nội dung sau vào file và thay thế bằng token của bạn:
        ```
        DISCORD_TOKEN="DISCORD_BOT_TOKEN"
        POLLINATIONS_API_TOKEN="API_TOKEN"
        ```

3.  **Build và Run Docker Container**:
    -   Mở terminal và chạy các lệnh sau:
        ```bash
        # Build Docker image
        docker build -t image-name:latest .

        # Run container ở chế độ nền (detached mode)
        docker run -d --name container-name image-name:latest
        ```
    -   Bot của bạn giờ đã hoạt động bên trong container!

---

## 💜 Lời kết

Nếu bạn thấy dự án này thú vị và hữu ích, đừng ngần ngại cho mình một ⭐ trên GitHub nha! (´｡• ᵕ •｡`)♡

Và nếu bạn có ý tưởng gì hay ho để cải thiện bé Waifu, hãy **Fork** repo và tạo một Pull Request nhé. Mọi sự đóng góp đều đáng quý!

Cảm ơn bạn đã ghé thăm! (ﾉ´ヮ´)ﾉ*:･ﾟ✧
