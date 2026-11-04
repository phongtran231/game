# Hướng Dẫn Triển Khai (Deployment Guide) — COIN-OPX

Tài liệu hướng dẫn chi tiết cách triển khai nền tảng máy thùng trực tuyến **COIN-OPX** lên môi trường Production (VPS Linux, Docker, hoặc Cloudflare Pages).

---

## ⚠️ Điều Kiện Tiên Quyết Bắt Buộc

Nền tảng chạy giả lập WebAssembly RetroArch đa luồng với độ trễ thấp thông qua `SharedArrayBuffer`. Để tính năng này hoạt động:
1. **Bắt buộc phải có HTTPS** (Trình duyệt sẽ chặn `SharedArrayBuffer` trên HTTP thường, ngoại trừ `localhost`).
2. **Bắt buộc phải có 2 HTTP Response Headers**:
   - `Cross-Origin-Opener-Policy: same-origin`
   - `Cross-Origin-Embedder-Policy: credentialless` (hoặc `require-corp`)

---

## Cách 1: Triển Khai Bằng Nginx Trên VPS (Ubuntu / Debian)

### 1. Chuẩn bị thư mục và tải mã nguồn
```bash
# Tạo thư mục web
sudo mkdir -p /var/www/coin-opx
sudo chown -R $USER:$USER /var/www/coin-opx

# Copy toàn bộ source từ máy tính lên VPS (hoặc git clone)
# Ví dụ từ máy tính:
# scp -r ~/Desktop/coin-opx/* user@vps_ip:/var/www/coin-opx/
```

### 2. Cấu hình Nginx
Tạo file cấu hình virtual host:
```bash
sudo nano /etc/nginx/sites-available/coin-opx
```

Nội dung cấu hình:
```nginx
server {
    listen 80;
    server_name arcade.yourdomain.com; # Thay bằng tên miền của bạn
    root /var/www/coin-opx;
    index index.html;

    # 1. BẮT BUỘC: Headers kích hoạt SharedArrayBuffer cho WebAssembly
    add_header Cross-Origin-Opener-Policy same-origin always;
    add_header Cross-Origin-Embedder-Policy credentialless always;

    # 2. Xử lý Single Page Application (SPA fallback)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 3. Cache tối ưu cho assets và ROMs
    location ~* \.(js|css|png|jpg|jpeg|gif|svg|ico|wasm)$ {
        expires 30d;
        add_header Cache-Control "public, no-transform";
        add_header Cross-Origin-Opener-Policy same-origin always;
        add_header Cross-Origin-Embedder-Policy credentialless always;
    }

    location /samples-roms/ {
        expires 7d;
        add_header Cache-Control "public, no-transform";
        add_header Access-Control-Allow-Origin "*";
        add_header Cross-Origin-Opener-Policy same-origin always;
        add_header Cross-Origin-Embedder-Policy credentialless always;
    }
}
```

Kích hoạt site và reload Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/coin-opx /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. Cài đặt SSL miễn phí với Let's Encrypt (Certbot)
```bash
sudo apt update
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d arcade.yourdomain.com
```

---

## Cách 2: Triển Khai Bằng Docker & Docker Compose

Nếu bạn thích quản lý bằng container gọn nhẹ:

### 1. Tạo file `Dockerfile`
```dockerfile
FROM nginx:alpine
COPY . /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 2. Tạo file `nginx.conf`
```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    add_header Cross-Origin-Opener-Policy same-origin always;
    add_header Cross-Origin-Embedder-Policy credentialless always;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(zip|wasm|js|css|png|svg)$ {
        add_header Cross-Origin-Opener-Policy same-origin always;
        add_header Cross-Origin-Embedder-Policy credentialless always;
        add_header Access-Control-Allow-Origin "*";
    }
}
```

### 3. Tạo file `docker-compose.yml`
```yaml
version: '3.8'

services:
  coin-opx:
    build: .
    container_name: coin-opx-web
    restart: always
    ports:
      - "8080:80"
```

Khởi chạy container:
```bash
docker compose up -d --build
```
*(Sau đó dùng Cloudflare Tunnel hoặc Nginx Proxy Manager trỏ domain về cổng 8080 kèm SSL).*

---

## Cách 3: Triển Khai Lên Cloudflare Pages (Miễn Phí, Toàn Cầu)

Đây chính là kiến trúc mà trang gốc `arcade.apxn.io.vn` đang sử dụng:
1. Đẩy mã nguồn lên GitHub/GitLab repository.
2. Đăng nhập vào [Cloudflare Dashboard](https://dash.cloudflare.com) -> **Workers & Pages** -> **Create Application** -> **Pages**.
3. Kết nối với repo và chọn build setting:
   - **Framework preset**: None
   - **Build output directory**: `.` (thư mục gốc)
4. **Cấu hình Headers trong Cloudflare Pages**:
   Tạo file `_headers` ngay tại thư mục gốc của repo:
   ```
   /*
     Cross-Origin-Opener-Policy: same-origin
     Cross-Origin-Embedder-Policy: credentialless
     Cache-Control: public, max-age=0, must-revalidate

   /assets/*
     Cache-Control: public, max-age=31536000, immutable

   /samples-roms/*
     Access-Control-Allow-Origin: *
     Cross-Origin-Resource-Policy: same-origin
     Cache-Control: public, max-age=604800
   ```
5. Nhấn **Save and Deploy**. Cloudflare sẽ tự động cấp SSL, CDN toàn cầu và bật HTTP/3.

---

## 📡 Cấu Hình Signaling Server Cho P2P Multiplayer

Mặc định hệ thống sử dụng PeerJS Cloud và Cloudflare STUN (`stun:stun.cloudflare.com:3478`).

Nếu bạn muốn tự vận hành Signaling Server riêng trên VPS để không phụ thuộc vào PeerJS bên ngoài:
```bash
# Cài đặt PeerJS Server qua Node.js trên VPS
npm install -g peer
peerjs --port 9000 --path /myapp
```
Sau đó thay đổi cấu hình khởi tạo Peer trong `vendor-netplay` sang endpoint VPS của bạn:
`new Peer("coin-opx-p2p-" + roomCode, { host: "yourdomain.com", port: 443, path: "/myapp", secure: true })`.
