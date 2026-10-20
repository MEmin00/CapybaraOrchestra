<div align="center">

# 🎵 Capybara Orchestra 🐹 🎻

**Python & Pygame ile geliştirilmiş sevimli bir müzikal idle / clicker oyunu.**  
*Piyano çalmak için tıkla, notaları topla, kapibara müzisyenleri orkestraya kat ve görkemli bir senfoni oluştur!*

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.5+-green?style=for-the-badge&logo=gamepad&logoColor=white)](https://www.pygame.org/)
[![Lisans: MIT](https://img.shields.io/badge/Lisans-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PR'lar-Açık-brightgreen.svg?style=for-the-badge)](README.md)

[English](README.md) • [Türkçe](README.tr.md)

<br/>

<img src="varliklar/capibaralar/giris.png" alt="Capybara Orchestra Banner" width="800" style="border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);"/>

</div>

---

## 📖 Genel Bakış

**Capybara Orchestra**, Python ve **Pygame** kütüphanesi kullanılarak geliştirilmiş eğlenceli ve rahatlatıcı bir ritim/tıklama (clicker) oyunudur.

Oyuna sahnede tek başına piyano çalan azimli bir kapibara piyanist olarak başlarsınız. Sahneye her tıkladığınızda müzik notaları kazanırsınız. Kazandığınız notalar arttıkça yeni kapibara müzisyenleri (zil, org, keman, bateri, koro) kiralayabilirsiniz.

Oyunun en dikkat çekici özelliği **dinamik çok kanallı ses motorudur**: Satın aldığınız her yeni enstrüman, gerçek zamanlı olarak ana müziğe kendi parçasını ekler. Tek bir piyano melodisiyle başlayan yolculuk, adım adım dev bir kapibara orkestrasına ve son aşamada salonu dolduran seyircilerin alkışladığı görkemli bir senfoniye dönüşür!

---

## ✨ Özellikler

- 🎹 **Dinamik Katmanlı Ses Sistemi:** Her orkestra üyesi eklendiğinde kendi enstrüman kanalı eşzamanlı olarak arka plandaki müziğe katılır.
- 🐹 **Özel Kapibara Karakterleri:** Çalma ve bekleme durumlarına göre tepki veren sevimli piksel/çizim karakter animasyonları.
- ⚡ **Artımlı İlerleme (Idle/Clicker):** Tıkladıkça notalar kazanın, çarpanları katlayın ve orkestranızı büyütün.
- 💬 **Uçan Skor Bildirimleri:** Her vuruşta ekranda beliren dinamik "+N" nota göstergeleri.
- 🎚️ **Oyun İçi Kontroller ve Menü:** Duraklatma menüsü, ses seviyesi kaydırıcısı ve pratik arayüz.
- 🌿 **Hafif ve Sade:** Harici ağır oyun motorlarına gerek kalmadan saf Python & Pygame ile çalışır.

---

## 🎼 Orkestra ve Geliştirmeler

Notalarınızı biriktirdikçe sağ üstteki **Upgrade** menüsünden yeni müzisyenleri sahneye dahil edebilirsiniz:

| Müzisyen | Enstrüman | Gereken Nota | Çarpan | Rol / Sahne Konumu |
| :--- | :---: | :---: | :---: | :--- |
| **Piyanist Kapibara** *(Sen)* | 🎹 Kuyruklu Piyano | *Başlangıç* | **1x** | Başlangıç solisti (Sahne Merkezi) |
| **Crash Kapibara** | 💥 Zil / Crash | 1.000 | **4x** | Ritmik vurgular (Sol Ön) |
| **Orgcu Kapibara** | 🎹 Org / Klavye | 5.000 | **10x** | Melodi ve armoni (Sağ Köşe) |
| **Kemancı Kapibara** | 🎻 Klasik Keman | 20.000 | **25x** | Duygusal yaylılar (Sağ Ön) |
| **Baterist Kapibara** | 🥁 Bateri Kiti | 75.000 | **50x** | Güçlü ritim bölümü (Sol Köşe) |
| **Koro Kapibara** | 🎶 Kapibara Korosu | 300.000 | **100x** | Çok sesli görkemli koro (Arka Orta) |
| **Seyirci (Final)** | 👏 Salon Dolusu Seyirci | 1.000.000 | **500x** | Tüm orkestra ve alkışlarla dev senfoni finali! |

---

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler

- **Python 3.8+**
- `pip` (Python paket yöneticisi)

### Adım Adım Kurulum

1. **Projeyi klonlayın:**
   ```bash
   git clone https://github.com/MEmin00/CapybaraOrchestra.git
   cd CapybaraOrchestra
   ```

2. **Sanal ortam oluşturun ve aktif edin (Önerilen):**
   ```bash
   # macOS / Linux için:
   python3 -m venv venv
   source venv/bin/activate

   # Windows için:
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Gerekli bağımlılıkları yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Oyunu başlatın:**
   ```bash
   python main.py
   ```

---

## 🕹️ Nasıl Oynanır?

- **Sol Fare Tıklaması:**
  - Piyanist kapibaraya tıklayarak nota üretin.
  - Sahnede açılan müzisyenlere tıklayarak çalma animasyonlarını ve enstrüman seslerini tetikleyin.
  - Menü butonlarına tıklayarak ekranlar arasında geçiş yapın.
- **Sağ Üstteki "Upgrade" Butonu:** Geliştirme menüsünü açarak yeni müzisyenler satın alın.
- **Durdurma (Pause) Menüsü:** Müziğin genel ses düzeyini ayarlayın veya ana menüye dönün.

---

## 📁 Proje Dizin Yapısı

```text
CapybaraOrchestra/
├── main.py                     # Ana oyun döngüsü ve ekran koordinatörü
├── requirements.txt            # Python bağımlılıkları (pygame)
├── LICENSE                     # MIT Lisansı
├── README.md                   # İngilizce dokümantasyon
├── README.tr.md                # Türkçe dokümantasyon
│
├── oyun/                       # Oyun mekanikleri ve ekran sınıfları
│   ├── anaMenu.py              # Giriş menüsü ve buton kontrolleri
│   ├── sahne.py                # Sahne yönetimi, enstrüman sesleri ve mikser
│   ├── upgrade.py              # Geliştirme (shop) paneli ve kaydırma mantığı
│   ├── arayuz.py               # Yeniden kullanılabilir arayüz bileşenleri (Buton vb.)
│   └── kayanMetin.py           # Tıklama ile uçuşan skor/nota efektleri
│
├── varliklar/                  # Oyun varlıkları (Assets)
│   ├── capibaralar/            # Karakter görselleri (normal ve çalan halleri)
│   ├── kullaniciArayuzu/       # Arayüz ikonları (pause, buton, onay işareti vb.)
│   └── ses/                    # Enstrüman sesleri ve fon müzikleri (.mp3)
│
└── images/                     # Ekran görüntüleri ve tanıtım görselleri
```

---

## 🗺️ Gelecek Planları (Roadmap)

Projeye katkıda bulunmak isteyenler için planlanan yenilikler:

- [ ] 💾 **Kayıt Sistemi (Save/Load):** Oyuncunun topladığı notaları ve açtığı yükseltmeleri yerel JSON formatında kaydetme.
- [ ] ⏱️ **Pasif Nota Üretimi (NPS):** Tıklamaya gerek kalmadan saniye başına otomatik nota geliri.
- [ ] 🏆 **Başarım Sistemi:** Belirli hedeflere ulaşıldığında rozetler ve bildirimler.
- [ ] 🎷 **Yeni Enstrümanlar:** Saksafon, arp, akordeon ve zil çalan yeni kapibara üyeleri.
- [ ] 🌐 **Web Tarayıcısı Desteği:** Pygbag kullanılarak Itch.io üzerinden tarayıcıda doğrudan oynanabilen sürüm.
- [ ] ✨ **Görsel Efektler:** Nota parçacıkları, konfeti ve sahne ışıklandırmaları.

---

## 🤝 Katkıda Bulunma

Açık kaynak dünyasına ve Kapibara Orkestrası'na hoş geldiniz! Hata bildirimleri, yeni enstrüman/özellik fikirleri ve PR'lar memnuniyetle kabul edilir:

1. Bu depoyu **fork** edin.
2. Yeni bir özellik dalı açın (`git checkout -b ozellik/YeniEnstruman`).
3. Değişikliklerinizi commit edin (`git commit -m 'Saksafoncu kapibara eklendi'`).
4. Dalınızı push edin (`git push origin ozellik/YeniEnstruman`).
5. Bir **Pull Request** gönderin.

---

## 📜 Lisans

Bu proje [MIT Lisansı](LICENSE) kapsamında açık kaynak olarak sunulmuştur. Dilediğiniz gibi inceleyebilir, geliştirebilir ve kendi projelerinizde esinlenebilirsiniz.

---

## 👥 Geliştiriciler & Emeği Geçenler

Sevgiyle geliştirenler:

- **[Mehmet Emin Dereci](https://github.com/MEmin00)** — Geliştirme
- **[Berat Salih Ersoy](https://github.com/beratersoy0)** — Geliştirme
- **[Tugay Arıcan](https://github.com/tugayarican)** — Müzikler & Ses Tasarımı / Geliştirme

*Yıldız ⭐ vermeyi ve fikirlerinizi paylaşmayı unutmayın!*
