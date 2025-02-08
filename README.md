# Nesne Tespit ve Takip Sistemi

Bu proje, OpenCV ve Python kullanarak belirli renkteki nesneleri (yeşil, mavi ve sarı) kamera veya video üzerinden algılayıp takip eden bir sistemdir. Algılanan nesnelerin hareket geçmişi kaydedilir ve görselleştirilir.

## İçindekiler
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Çalışma Mantığı](#çalışma-mantığı)
- [Kullanılan Teknikler ve Açıklamalar](#kullanılan-teknikler-ve-açıklamalar)
- [Görseller](#görseller)

## Kurulum

Projeyi çalıştırmak için aşağıdaki bağımlılıkları yükleyin:

```bash
pip install opencv-python imutils numpy
```

Alternatif olarak, `requirements.txt` dosyasından yükleyebilirsiniz:

```bash
pip install -r requirements.txt
```

## Kullanım

Programı başlatmak için aşağıdaki komutu kullanabilirsiniz:

```bash
python object_tracking.py
```

Bir video dosyası kullanmak için:

```bash
python object_tracking.py --video path/to/video.mp4
```

Tampon boyutunu değiştirmek için:

```bash
python object_tracking.py --buffer 128
```

Çıkmak için `q` tuşuna basabilirsiniz.

## Çalışma Mantığı

1. **Video Akışı Başlatma:** Kamera veya video dosyasından giriş alınır.
2. **Önişleme:** Görüntü boyutu küçültülür, bulanıklaştırma ve HSV dönüşümü uygulanır.
3. **Renk Maskeleme:** Yeşil, mavi ve sarı renkler için ayrı maskeler oluşturulur.
4. **Kontur Tespiti:** Nesneler belirlenir ve çevresine daire çizilir.
5. **Nesne Takibi:** Önceki çerçevelerle karşılaştırma yapılarak nesnelerin hareketi takip edilir.
6. **Görselleştirme:** Nesnenin geçmiş hareketi çizgi ile gösterilir.
7. **Çıkış İşlemleri:** `q` tuşuna basıldığında program durur.

## Kullanılan Teknikler ve Açıklamalar

### 1. **OpenCV ile Görüntü İşleme**
   - **Gaussian Blur:** Gürültüyü azaltmak için kullanılır.
   - **HSV Renk Uzayı:** Işık değişimlerinden etkilenmemesi için RGB yerine kullanılır.
   - **inRange:** Belirli renk aralıklarını maskeleme için kullanılır.
   
### 2. **Nesne Algılama ve Takip**
   - **cv2.findContours:** Nesnelerin dış hatlarını bulmak için kullanılır.
   - **cv2.minEnclosingCircle:** Nesne çevresine minimum çaplı bir daire çizer.
   - **cv2.moments:** Nesnenin ağırlık merkezini hesaplar.

### 3. **Nesne Tanımlama ve ID Atama**
   - Nesneler, en yakın geçmiş konumlarına göre tanımlanır.
   - **numpy.linalg.norm:** Mesafe hesaplamak için kullanılır.
   - Eğer bir nesne 50 pikselden daha uzaksa, yeni bir nesne olarak kaydedilir.
   
### 4. **Hareket Geçmişi ve Görselleştirme**
   - `deque` kullanılarak nesnenin önceki pozisyonları saklanır.
   - **cv2.line:** Nesnenin geçmiş hareketini göstermek için kullanılır.
   
## Görseller

Proje çalışırken elde edilen örnek bir kare:

![Object Tracking](path/to/example_image.jpg)

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.
