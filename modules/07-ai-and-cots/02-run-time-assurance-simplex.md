# 📘 Modül 7.2: Run-Time Assurance (RTA) ve Simplex Mimarisi (ASTM F3269)

## 1. Run-Time Assurance (RTA) Felsefesi
Sertifiye edilemeyen karmaşık bir algoritmanın (Yapay Zeka, Derin Takviyeli Öğrenme, COTS İşlemci) emniyet-kritik bir sisteme dahil edilmesinin yolu **Run-Time Assurance (Çalışma Zamanı Güvencesi)** mimarisidir.

> **Prensip:** Karmaşık yapay zeka modelinin kendisini değil; yapay zekanın ürettiği kararların emniyet sınırlarını (Safety Envelope) aşıp aşmadığını çalışma zamanında denetleyen basit, formel olarak kanıtlanmış bir monitör sertifiye edilir.

---

## 2. Simplex Mimarisi Blok Şeması (ASTM F3269-17)

```mermaid
flowchart TD
    Sensor["Sensör Verileri"] --> CC["Karmaşık Kontrolcü (Complex Controller)<br/>Derin Öğrenme / AI (Sertifikasız)"]
    Sensor --> SC["Emniyet Kontrolcüsü (Safety Controller)<br/>Basit / Deterministik PID (DAL A)"]
    Sensor --> Mon["Emniyet Monitörü (Safety Monitor)<br/>Uçuş Zarfı Denetleyicisi (DAL A)<br/>[SYS-RTA-01]"]

    CC --> Switch{"Seçici Anahtar<br/>(Switching Logic)<br/>[SYS-RTA-02]"}
    SC --> Switch
    Mon -->|Zarf İhlali Tetiklemesi| Switch

    Switch -->|Normal: Karmaşık Komut| Actuator["Uçuş Yüzeyi Aktüatörü"]
    Switch -->|Tehlike: Emniyet Komutu| Actuator
```

---

## 3. Üç Temel Bileşen
1. **Complex Controller (CC):** Yüksek performanslı ancak formel kanıtı olmayan yapay zeka algoritması. Normal şartlarda aktüatörü yönetir.
2. **Safety Monitor (SM):** Sistemi matematiksel olarak modellenmiş "Emniyetli Durum Zarfı" içinde tutar. Eğer CC tehlikeli bir manevra komutu üretirse (örn: stall açısı ihlali), bunu mikro saniyeler içinde tespit eder.
3. **Safety / Recovery Controller (SC):** Sertifikalı, basit, deterministik (DAL A) kurtarma algoritmasıdır. Kontrolü devralıp hava aracını düz uçuş moduna getirir.

---

## 4. İzlenebilirlik İlişkisi
- `[SYS-RTA-01]` Emniyet monitörü hücum açısını (AoA) izlemeli ve 15 derecenin üzerine çıkarsa anahtarlamayı tetiklemelidir.
- `[LLR-RTA-010]` `RTA_CheckSafetyEnvelope()` fonksiyonu 5 ms periyotla zarf denetimi yapmalıdır.
