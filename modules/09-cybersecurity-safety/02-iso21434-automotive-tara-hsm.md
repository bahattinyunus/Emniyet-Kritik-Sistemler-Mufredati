# 📘 Modül 9.2: Otomotiv Siber Güvenliği, TARA ve Donanım Güvenlik Modülleri (ISO/SAE 21434 & HSM)

## 1. ISO/SAE 21434 ve UNECE R155 Regülasyonu
Modern bağlantılı ve otonom araçlar (SDV - Software-Defined Vehicles); V2X, Bluetooth, Hücresel (5G), OBD-II ve OTA (Over-the-Air) arayüzleri üzerinden dış dünyaya açıktır. Bir saldırganın bilgi-eğlence (Infotainment) sisteminden sızıp CAN veri yolu üzerinden fren veya direksiyon ECU'suna (Electronic Control Unit) sahte mesaj göndermesi doğrudan **ASIL D seviyesinde ölümcül bir emniyet ihlalidir**.

- **ISO/SAE 21434:** Otomotiv elektrik/elektronik (E/E) sistemlerinin konsept aşamasından trafikten çekilmesine (Decommissioning) kadar siber güvenlik mühendisliği süreçlerini tanımlayan uluslararası standarttır.
- **UNECE R155:** Avrupa Birliği ve anlaşmalı ülkelerde yeni tip onayı alacak tüm araçlar için **CSMS (Cyber Security Management System)** sertifikasını yasal zorunluluk haline getirmiştir.

---

## 2. TARA (Threat Analysis and Risk Assessment) Metodolojisi
ISO 26262'deki **HARA (Hazard Analysis and Risk Assessment)** sürecinin siber güvenlikteki karşılığı **TARA**'dır:

```mermaid
flowchart TD
    A["1. Varlık Tanımlama<br/>(Asset Identification - CAN Mesajı, Firmware)"] --> B["2. Tehdit Senaryosu<br/>(STRIDE: Spoofing, Tampering, DoS)"]
    B --> C["3. Etki Derecelendirmesi<br/>(Impact Rating: Safety, Financial, Operational, Privacy)"]
    B --> D["4. Saldırı Yolu Analizi & Fizibilite<br/>(Attack Path & Attack Feasibility: Elapsed Time, Expertise, Equipment)"]
    C --> E["5. Risk Değeri Hesaplama<br/>(Risk Matrix: 1 - 5)"]
    D --> E
    E --> F["6. Siber Güvenlik Hedefleri & Gereksinimleri<br/>(Cybersecurity Goals & CAL 1-4)"]

    classDef tara fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#fff;
    class A,B,C,D,E,F tara;
```

### STRIDE Modeli ve Otomotiv Karşılıkları
| STRIDE Kategorisi | Güvenlik Özelliği | Otomotiv / Aviyonik Saldırı Örneği | Savunma Mekanizması |
| :--- | :--- | :--- | :--- |
| **S - Spoofing (Kimlik Sahteciliği)** | Kimlik Doğrulama (Authentication) | Arıza teşhis portundan sahte Direksiyon Açısı CAN mesajı basılması | AUTOSAR SecOC (CMAC Doğrulaması) |
| **T - Tampering (Kurcalama)** | Bütünlük (Integrity) | ECU Flash belleğindeki kalibrasyon haritasının değiştirilmesi | Secure Boot & HSM Dijital İmza |
| **R - Repudiation (İnkar)** | İnkar Edilemezlik (Non-repudiation) | Kritik parametre değişikliğini kimin yaptığının izlenememesi | Kriptografik Güvenlik Kayıt Defteri (Security Audit Log) |
| **I - Information Disclosure (İfşa)** | Gizlilik (Confidentiality) | JTAG/SWD portundan kriptografik anahtarların ve algoritmanın okunması | JTAG Sigorta Kilidi & HSM Key Store |
| **D - Denial of Service (Hizmet Reddi)** | Erişilebilirlik (Availability) | CAN hattına sürekli yüksek öncelikli (`ID: 0x000`) mesaj basılması | Donanımsal Bus Guardian & Rate Limiter |
| **E - Elevation of Privilege (Yetki Yükseltme)** | Yetkilendirme (Authorization) | Kullanıcı modundan çekirdek (Supervisor) moduna sıçrama | MPU/MMU Bellek Koruması & UDS `0x27` SecurityAccess |

---

## 3. AUTOSAR SecOC (Secure Onboard Communication)
Klasik CAN ve CAN-FD ağlarında mesajların hangi düğümden geldiğini kanıtlayan yerleşik bir kriptografik kimlik doğrulama yoktur. **AUTOSAR SecOC**, emniyet-kritik mesajlara gerçek zamanlı kriptografik doğrulama ekler:

```text
+-------------------+------------------------+---------------------------+
|   CAN-FD Başlığı  |   Kontrol Verisi       |   SecOC Güvenlik Alanı    |
|   (Arbitration)   |   (Hız, Tork, Fren)    |  [Fv (Tazelik)] + [MAC]   |
|      11/29-bit    |      4 - 48 Bayt       |   8-24 bit      24-64 bit |
+-------------------+------------------------+---------------------------+
```

1. **Freshness Value (Fv - Tazelik Sayacı):** Saldırganın daha önce kaydedilmiş geçerli bir fren mesajını tekrar ağa basmasını (**Replay Attack**) engellemek için her mesajda artan monotonik sayaç veya senkron zaman damgası kullanılır.
2. **MAC (Message Authentication Code - AES-128-CMAC):** Gönderici ECU; `Data ID + Payload + Tam Tazelik Sayacı` verisini gizli simetrik anahtarla (HSM içinde) imzalar ve kesilmiş (truncated) MAC etiketini mesaja ekler. Alıcı ECU, MAC doğrulanmazsa mesajı **kesinlikle işleme almaz**.

---

## 4. Donanım Güvenlik Modülü (HSM - Hardware Security Module) ve Güvenli Önyükleme (Secure Boot)

Yazılımsal kriptografi tek başına yetersizdir; çünkü anahtarlar normal RAM veya Flash bellekte durursa bellek dökümü (dump) ile çalınabilir. Bu nedenle modern emniyet işlemcilerinde (Örn: Infineon AURIX TC3xx/TC4xx, NXP S32G, Renesas RH850) ana işlemciden fiziksel güvenlik duvarıyla ayrılmış gömülü bir **HSM (EVITA Full / Medium)** çekirdeği bulunur.

### Güvenli Önyükleme Zinciri (Chain of Trust / Secure Boot)
```mermaid
sequenceDiagram
    participant ROM as Donanım Kök Güveni (Immutable Boot ROM)
    participant HSM as HSM Güvenlik Çekirdeği (AES/ECC Motoru)
    participant BL as Önyükleyici (Bootloader)
    participant APP as Emniyet-Kritik Uygulama (ASIL D / DAL A)

    ROM->>HSM: 1. Reset sonrası HSM'yi başlat
    HSM->>BL: 2. Bootloader Flash alanının CMAC/RSA imzasını oku
    Note over HSM: Donanım içindeki gizli kök anahtar ile doğrula
    alt İmza Geçerli
        HSM->>ROM: 3. Doğrulama Başarılı (Host CPU serbest bırakıldı)
        ROM->>BL: 4. Bootloader'ı çalıştır
        BL->>HSM: 5. Uygulama (APP) imajını doğrula
        HSM->>APP: 6. Uygulama başlatıldı & Çalışma zamanı bellek taraması aktif
    else İmza Geçersiz (Kurcalama Tespiti!)
        HSM-->>ROM: 3b. Güvenlik İhlali! İşlemciyi Safe State'de kilitle
    end
```

---

## 5. İzlenebilirlik Zinciri
- Tehlike & Tehdit Kaydı: `[HAZ-CYB-02]` CAN-FD veri yolu üzerinde tekrar saldırısı (Replay Attack) ile otonom direksiyon aktüatörüne eski manevra komutunun enjekte edilmesi.
- Sistem Gereksinimi: `[SYS-CYB-105]` Tüm ASIL D şasi kontrol mesajları AUTOSAR SecOC Profil 1 (AES-128-CMAC ve 24-bit monotonik tazelik sayacı) ile korunmalıdır.
- Donanım Gereksinimi: `[HWR-HSM-015]` Kriptografik anahtarlar yalnızca EVITA-Full uyumlu HSM güvenli belleğinde saklanmalı, ana CPU tarafından doğrudan okunamamalıdır.
- Alt Seviye Yazılım Gereksinimi: `[LLR-CYB-210]` `SecOC_VerifyRxPdu()` fonksiyonu, gelen mesajın tazelik sayacı son kabul edilen değerden küçük veya eşitse `SECOC_E_REPLAY_DETECTED` hatası döndürmeli ve paketi düşürmelidir.
- Doğrulama Testi: `[HIL-CYB-305]` CANoe/Vector donanımı üzerinden kaydedilmiş geçerli direksiyon paketinin 50 ms sonra tekrar gönderilerek reddedildiğinin doğrulanması.
