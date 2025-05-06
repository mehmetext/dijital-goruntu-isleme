# Dijital Görüntü İşleme - Ödev 2

## Ödev 2: Temel Görüntü Operasyonları ve İnterpolasyon

Bu ödevde, görüntü boyutunu büyütme, küçültme, zoom in, zoom out, döndürme gibi temel görüntü işleme operasyonlarını gerçekleştireceksiniz. Bu operasyonları gerçekleştirirken herhangi bir dış kütüphane kullanmadan, kendi algoritmalarınızı geliştirmeniz beklenmektedir.

### Görevler

#### 1. Görüntü Boyutunu Büyütme

- Görüntüyü belirli bir ölçüde büyütme
- Kullanıcıdan alınan faktör ile piksel değerlerini hesaplama
- Farklı interpolasyon yöntemlerini uygulama (bilinear, bicubic, average)

#### 2. Görüntü Boyutunu Küçültme

- Görüntüyü belirli bir ölçüde küçültme
- Kullanıcıdan alınan faktör ile piksel değerlerini yeniden hesaplama
- Farklı interpolasyon yöntemlerini uygulama

#### 3. Zoom In ve Zoom Out

- Görüntüyü belirli bir oranda yakınlaştırma (zoom in)
- Görüntüyü belirli bir oranda uzaklaştırma (zoom out)
- Piksel değerlerini uygun şekilde yeniden hesaplama

#### 4. Görüntü Döndürme

- Kullanıcıdan alınan açıya göre görüntüyü döndürme
- Döndürme işlemi için formül kullanarak piksel değerlerini hesaplama
- Farklı interpolasyon yöntemlerini uygulama

#### 5. Interpolasyon Yöntemleri

- Bilinear interpolasyon implementasyonu
- Bicubic interpolasyon implementasyonu
- Average interpolasyon implementasyonu
- Her yöntem için formüllerin uygulanması

### Önemli Notlar

- **Dış Kütüphane Kullanımı**: Görüntü işleme operasyonları için herhangi bir dış kütüphane kullanımı yasaktır.
- **Detaylı Açıklamalar**: Her operasyon için adım adım açıklamalar rapora eklenecektir.
- **Kod Organizasyonu**: Kodlar modüler ve okunabilir şekilde organize edilecektir.

### Uygulama Yapısı

- `main.py`: Ana uygulama dosyası
- `ui/`: UI bileşenlerini içeren klasör
  - `image_operations.py`: Görüntü işleme operasyonları
  - `interpolation.py`: İnterpolasyon yöntemleri
- `utils/`: Yardımcı fonksiyonları içeren klasör
- `assets/`: Görsel ve diğer kaynakları içeren klasör
