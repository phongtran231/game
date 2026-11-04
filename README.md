# COIN-OPX — Mã Nguồn & Tài Nguyên Web Arcade Online P2P

Bản sao toàn bộ client source code, assets, giao diện và cấu hình của nền tảng **COIN-OPX** (https://arcade.apxn.io.vn).

---

## 📁 Cấu trúc thư mục

```
coin-opx/
├── index.html                   # File HTML chính (khởi chạy React + Nostalgist)
├── manifest.webmanifest         # Cấu hình PWA Web App
├── sw.js                        # Service Worker hỗ trợ cài đặt app PWA
├── serve.py                     # Script khởi chạy local server với COOP / COEP header
├── assets/                      # Toàn bộ mã nguồn bundle JavaScript & CSS
│   ├── index-B7AvUDy9.js        # Logic chính: UI, Netcode Rollback (Wx), Lockstep (Jx), Room P2P
│   ├── vendor-emulator-DTCC6bPL.js # Thư viện Nostalgist.js + RetroArch Emscripten bridge
│   ├── vendor-netplay-BHy6gZjF.js  # Thư viện PeerJS + WebRTC DataChannels / MediaStreams
│   ├── vendor-react-BpaniaUk.js    # React 18/19 Runtime
│   └── index-CoNr-FVv.css       # Tailwind CSS & retro styling
├── covers/                      # Toàn bộ 48 ảnh bìa game Arcade (PNG)
├── icons/                       # Biểu tượng PWA & Favicon
└── samples-roms/
    └── neogeo.zip               # File BIOS Neo Geo MVS chuẩn (1.9MB)
```

---

## 🚀 Cách chạy trên máy tính (Local)

> [!IMPORTANT]
> **Không mở trực tiếp `index.html` bằng double-click**: Giả lập RetroArch WebAssembly yêu cầu tính năng đa luồng `SharedArrayBuffer`, bắt buộc trình duyệt phải nhận 2 HTTP headers:
> - `Cross-Origin-Opener-Policy: same-origin`
> - `Cross-Origin-Embedder-Policy: credentialless` (hoặc `require-corp`)

Chạy bằng script `serve.py` đã tạo sẵn:

```bash
cd ~/Desktop/coin-opx
python3 serve.py
```

Sau đó mở trình duyệt truy cập: **http://localhost:3000**
