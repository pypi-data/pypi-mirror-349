# WNote - Terminal Note Taking Application

WNote là ứng dụng ghi chú CLI chạy hoàn toàn trên terminal với giao diện đẹp mắt và dễ sử dụng.

![WNote Screenshot](https://via.placeholder.com/800x450.png?text=WNote+Terminal+Application)

## Tính năng

- ✏️ Tạo, chỉnh sửa, xem và xóa ghi chú
- 🏷️ Gắn thẻ (tag) cho ghi chú
- 🎨 Tùy chỉnh màu sắc cho từng thẻ
- 🔍 Lọc ghi chú theo thẻ
- 📝 Soạn thảo ghi chú với trình soạn thảo yêu thích của bạn (vim, nano, etc.)
- 📎 Đính kèm file hoặc thư mục vào ghi chú
- 🖥️ Mở file/thư mục đính kèm trực tiếp từ ghi chú
- 🔄 Đồng bộ hóa ghi chú giữa các thiết bị (qua Dropbox)
- 📱 Giao diện đẹp mắt với tùy chỉnh chủ đề màu
- 📊 Thống kê và phân tích ghi chú
- 🔐 Mã hóa ghi chú quan trọng
- 📅 Lịch và nhắc nhở cho ghi chú
- 📤 Xuất ghi chú sang nhiều định dạng (Markdown, PDF, HTML)

## Cài đặt

### Yêu cầu

- Python 3.7+
- pip

### Bước cài đặt

#### Từ PyPI (đề nghị)

```bash
pip install wnote
```

#### Từ source code

1. Clone repository:
```bash
git clone https://github.com/your-username/wnote.git
cd wnote
```

2. Cài đặt ứng dụng:
```bash
pip install -e .
```

## Sử dụng

### Các lệnh cơ bản

- Tạo ghi chú mới:
```bash
wnote add "Tiêu đề ghi chú" -t "tag1,tag2"
```

- Tạo ghi chú với file đính kèm:
```bash
wnote add "Tiêu đề ghi chú" -f "/đường/dẫn/đến/file"
```

- Đính kèm file vào ghi chú hiện có:
```bash
wnote attach 1 "/đường/dẫn/đến/file"
```

- Xem tất cả ghi chú:
```bash
wnote show
```

- Xem ghi chú theo ID:
```bash
wnote show 1
```

- Xem ghi chú theo ID và tự động mở tất cả file đính kèm:
```bash
wnote show 1 -o
```

- Xem ghi chú theo thẻ:
```bash
wnote show -t "work"
```

- Chỉnh sửa nội dung ghi chú:
```bash
wnote edit 1
```

- Cập nhật tiêu đề hoặc thẻ:
```bash
wnote update 1 -t "new title" --tags "tag1,tag2,tag3"
```

- Xóa ghi chú:
```bash
wnote delete 1
```

- Xem tất cả thẻ:
```bash
wnote tags
```

- Đặt màu cho thẻ:
```bash
wnote color work blue
```

- Xem cấu hình:
```bash
wnote config
```

### Các tính năng mới

- Xuất ghi chú sang Markdown:
```bash
wnote export 1 --format markdown
```

- Mã hóa ghi chú:
```bash
wnote encrypt 1
```

- Đồng bộ hóa ghi chú:
```bash
wnote sync
```

- Thống kê ghi chú:
```bash
wnote stats
```

- Tùy chỉnh chủ đề màu:
```bash
wnote theme dark
```

## Đường dẫn cấu hình

- Cơ sở dữ liệu: `~/.config/wnote/notes.db`
- Tệp cấu hình: `~/.config/wnote/config.json`
- Thư mục đính kèm: `~/.config/wnote/attachments`

## Các màu có sẵn

- red, green, blue, yellow, magenta, cyan, white, black
- bright_red, bright_green, bright_blue, bright_yellow, bright_magenta, bright_cyan, bright_white

## Phân phối cho người khác

### 1. Cài đặt thông qua PyPI

Bạn có thể phân phối WNote thông qua PyPI để người dùng có thể cài đặt một cách dễ dàng:

```bash
pip install wnote
```

### 2. Đóng gói dưới dạng Standalone App

Sử dụng PyInstaller để tạo ra executable file độc lập:

```bash
pip install pyinstaller
pyinstaller --onefile wnote.py
```

File thực thi sẽ được tạo trong thư mục `dist/`.

### 3. Sử dụng Docker

```bash
# Dockerfile đã được cung cấp trong repo
docker build -t wnote .
docker run -it wnote
```

### 4. Đồng bộ qua dịch vụ đám mây

Bạn có thể sử dụng tính năng đồng bộ hóa để chia sẻ ghi chú giữa các thiết bị:

```bash
# Cấu hình đồng bộ với Dropbox
wnote sync --setup dropbox
```

## Đóng góp

Chúng tôi rất hoan nghênh đóng góp từ cộng đồng. Vui lòng làm theo các bước sau:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/amazing-feature`)
3. Commit thay đổi của bạn (`git commit -m 'Add some amazing feature'`)
4. Push lên branch (`git push origin feature/amazing-feature`)
5. Tạo Pull Request mới

## Giấy phép

Phân phối dưới giấy phép MIT. Xem `LICENSE` để biết thêm chi tiết. 