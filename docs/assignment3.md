# Dijital Görüntü İşleme - Ödev 3

## Ödev 3: Gelişmiş Görüntü İşleme Uygulamaları

Bu ödevde, kontrast güçlendirme, Hough dönüşümü ile nesne tespiti, deblurring algoritması geliştirme ve nesne sayma gibi ileri seviye görüntü işleme uygulamaları gerçekleştireceksiniz. Kodlarınızı 1. ödevde hazırladığınız arayüz menülerine entegre etmeniz gerekmektedir. Kodlarınızı Github'a yüklemeniz ekstra 5 puan kazandıracaktır.

### Görevler

#### 1. S-Curve Metodu ile Kontrast Güçlendirme

- Seçtiğiniz bir görüntü için aşağıdaki fonksiyonları kullanarak S-curve metodu ile kontrast güçlendirme işlemi yapınız:
  - a) Standart Sigmoid Fonksiyonu (5 puan)
  - b) Yatay Kaydırılmış Sigmoid Fonksiyonu (5 puan)
  - c) Eğimli Sigmoid Fonksiyonu (5 puan)
  - d) Kendi ürettiğiniz bir fonksiyon (10 puan)
- S-curve metodunu raporunuzda açıklayınız (5 puan)
- (Fig 3 görseli buraya eklenecek)
- **Açıklama:** Bu metot, biyomedikal görüntülerde hastalık tespiti, askeri görüntülerde nesne tespiti gibi uygulamalarda başarıyı artırmak için kullanılır.

#### 2. Hough Transform ile Nesne Tespiti

- a) Yoldaki çizgileri tespit eden bir uygulama geliştirin (10 puan)
- b) Yüz resminde gözleri tespit eden bir uygulama geliştirin (10 puan)
- Hough transform metodunu raporunuzda açıklayınız ve sonuçlarını gösteriniz (10 puan)
- (Göz görseli buraya eklenecek)

#### 3. Deblurring Algoritması Geliştirme

- Hareketli cisimlerin fotoğraflarında oluşan motion blur bozulmasını gidermek için kendi geliştirdiğiniz bir deblurring algoritması uygulayınız.
- Akış diyagramı, önce ve sonra görüntülerini raporunuza ekleyiniz (10 puan)
- (Deblur görseli buraya eklenecek)

#### 4. Nesne Sayma ve Özellik Çıkarma

- Ekte verilen tarladan çekilmiş hiperspektral görüntüdeki "koyu yeşil" bölgeleri tespit ediniz.
- Her bir nesne için aşağıdaki gibi bir excel tablosu oluşturacak kodu yazınız (40 puan):

| No  | Center  | Length | Width | Diagonal | Energy | Entropy | Mean | Median |
| --- | ------- | ------ | ----- | -------- | ------ | ------- | ---- | ------ |
| 1   | 211,344 | 20 px  | 52 px | 78 px    | 3,477  | 36,25   | 127  | 134    |
| 2   | 386,896 | 48 px  | 12 px | 44 px    | 6,42   | 22,98   | 80   | 96     |

- (Nesne sayma görseli buraya eklenecek)

### Önemli Notlar

- **Dış Kütüphane Kullanımı:** Görüntü işleme operasyonları için herhangi bir dış kütüphane kullanımı yasaktır.
- **Detaylı Açıklamalar:** Her operasyon için adım adım açıklamalar rapora eklenecektir.
- **Kod Organizasyonu:** Kodlar modüler ve okunabilir şekilde organize edilecektir.

### Uygulama Yapısı

- `main.py`: Ana uygulama dosyası
- `ui/`: UI bileşenlerini içeren klasör
  - `image_operations.py`: Görüntü işleme operasyonları
  - `interpolation.py`: İnterpolasyon ve S-curve yöntemleri
  - `hough.py`: Hough transform ve nesne tespiti
  - `deblurring.py`: Deblurring algoritması
  - `object_counting.py`: Nesne sayma ve özellik çıkarma
- `utils/`: Yardımcı fonksiyonları içeren klasör
- `assets/`: Görsel ve diğer kaynakları içeren klasör
