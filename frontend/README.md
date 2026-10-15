# MLBB Hero Classifier - Modern Academic Design

Aplikasi klasifikasi hero Mobile Legends Bang Bang menggunakan AI dengan desain modern, akademik, dan glassmorphism yang profesional.

## 🎨 Design Features

### Glassmorphism UI

- **Background**: Gradient soft blue dan indigo dengan pattern grid
- **Cards**: White/60% opacity dengan backdrop blur untuk efek kaca
- **Borders**: Subtle slate-200/50% untuk kesan elegan
- **Shadows**: Soft shadows untuk depth yang natural

### Color Palette

- **Primary**: Indigo (600-700) untuk action buttons
- **Secondary**: Blue (500-600) untuk camera features
- **Success**: Emerald (500-600) untuk positive states
- **Warning**: Amber (500-600) untuk processing states
- **Role Colors**: Soft pastels (orange, red, purple, rose, blue, emerald)

### Typography

- **Headers**: Slate-800, font-bold untuk hierarchy yang jelas
- **Body**: Slate-600/700 untuk readability
- **Labels**: Slate-500, uppercase, tracking-wide untuk professional look

## 📁 File Structure

```
/home/claude/
├── page.js              # Main page component
├── layout.js            # Root layout
├── globals.css          # Global styles & animations
├── InputArea.js         # Upload & camera input component
├── CameraCapture.js     # Live camera interface
├── ResultDisplay.js     # Results with hero images
└── README.md           # This file
```

## 🚀 Features

1. **Upload Image**: Upload hero image dari device
2. **Camera Capture**: Tangkap langsung dari kamera
3. **AI Classification**: Deteksi hero dan role dengan confidence score
4. **Real Hero Images**: Menggunakan gambar hero dari internet
5. **Responsive Design**: Mobile-friendly layout
6. **Smooth Animations**: Scan animation dan transitions

## 🎯 Hero Images

Hero images diambil dari internet (CDN) dengan mapping:

- Default placeholder untuk hero yang tidak ada di database
- Support untuk semua hero MLBB
- Automatic fallback ke default image

## 💡 Usage

1. Copy semua file ke dalam project Next.js Anda
2. Pastikan struktur folder components sudah sesuai
3. Install dependencies: `npm install`
4. Jalankan dev server: `npm run dev`
5. Akses di browser: `http://localhost:3000`

## 🔧 Customization

### Menambah Hero Images

Edit `heroImages` object di `ResultDisplay.js`:

```javascript
const heroImages = {
  "HeroName": "https://url-to-image.jpg",
  // tambahkan hero lainnya
};
```

### Mengubah Color Scheme

Edit `roleStyles` di `ResultDisplay.js` untuk custom role colors.

### API Endpoint

Update `API_URL` di `page.js` sesuai dengan backend Anda:

```javascript
const API_URL = "http://your-backend-url:port/predict";
```

## 📱 Responsive Breakpoints

- **Mobile**: < 768px (1 column layout)
- **Tablet**: 768px - 1024px (adaptive grid)
- **Desktop**: > 1024px (2 column layout)

## 🎨 Design Philosophy

Desain ini menggabungkan:

- **Academic**: Professional, clean, structured
- **Modern**: Glassmorphism, smooth animations
- **Game-themed**: Color coding by role, hero avatars
- **Accessible**: High contrast, readable typography

## 📝 Notes

- Semua komponen menggunakan "use client" untuk interaktivitas
- Glassmorphism effect optimal di browser modern
- Hero images require internet connection
- Camera requires HTTPS in production

## 🔗 Dependencies

- Next.js 14+
- React 18+
- Tailwind CSS 3+
- Lucide React (icons)
