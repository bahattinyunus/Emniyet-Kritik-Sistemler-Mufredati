# 📘 Modül 4.3: RTCA DO-160G Çevresel Dayanım Testleri ve Kalifikasyon

## 1. RTCA DO-160G / EUROCAE ED-14G Nedir?
Uçuşa elverişli aviyonik donanımların; aşırı soğuk/sıcak, basınç düşüşü, titreşim, şok ve yıldırım gibi fiziksel zorluklar altında fonksiyonlarını kaybetmeden çalışacağını laboratuvar ortamında kanıtlayan çevresel test standartıdır.

---

## 2. Temel Test Kategorileri

| Kategori / Bölüm | Test Adı | Amaç ve Zorluk |
| :--- | :--- | :--- |
| **Bölüm 4** | Sıcaklık ve İrtifa | -55°C ila +70°C arası çalışma; 55.000 ft basınç kaybı (Decompression) |
| **Bölüm 5** | Sıcaklık Değişimi | Dakikada 10°C'ye varan termal şok geçişleri |
| **Bölüm 7** | Operasyonel Şok & Çarpışma Emniyeti | Sert inişler veya kaza anında ekipmanın yuvasından fırlamaması |
| **Bölüm 8** | Titreşim (Vibration) | Jet motoru veya helikopter pallerinin yarattığı rezonans frekansları |
| **Bölüm 16** | Güç Girişi (Power Input) | 28V DC veya 115V AC 400Hz hatlarındaki ani voltaj çöküşleri (Spikes) |
| **Bölüm 22** | Yıldırım Dolaylı Etkileri | Gövdeye düşen yıldırımın kablolarda oluşturduğu kilovolt seviyesinde indüklenmiş akım darbeleri |

---

## 3. Donanım Tasarım Tedbirleri
- **Yıldırım Koruması:** TVS (Transient Voltage Suppressor) diyotları, gas discharge tubes (GDT) ve çok katmanlı PCB toprak ekranlaması.
- **Titreşim Dayanımı:** BGA kılıfların altına epoksi dolgu (Underfill) yapılması ve komponent lehim çatlaklarının önlenmesi.
