# 📘 Modül 2.3: EARS ile Atomik ve Test Edilebilir Gereksinim Mühendisliği

## 1. Giriş: Emniyet-Kritik Gereksinimlerin Önemi
Yazılım ve sistem hatalarının %60'ından fazlası yanlış, eksik veya çelişkili gereksinimlerden kaynaklanır. DO-178C ve ARP 4754B sertifikasyon süreçlerinde denetçilerin ilk baktığı konu gereksinimlerin **doğrulanabilirliği (verifiability)** ve **belirsizlikten uzaklığıdır (unambiguity)**.

---

## 2. EARS (Easy Approach to Requirements Syntax) Metodolojisi
Rolls-Royce tarafından geliştirilen EARS, doğal dildeki muğlaklığı ortadan kaldıran 5 ana şablon sunar:

| Şablon Türü | EARS Sözdizimi | Kullanım Amacı | Örnek Gereksinim |
| :--- | :--- | :--- | :--- |
| **Ubiquitous (Her Zaman Geçerli)** | *The `<system>` shall `<action>`.* | Sürekli aktif olan temel fonksiyonlar | `[SYS-EARS-01]` The FCC shall continuously monitor internal core temperature. |
| **Event-Driven (Olay Tetiklemeli)** | *WHEN `<trigger>`, the `<system>` shall `<action>`.* | Bir olay meydana geldiğinde verilen tepki | `[HLR-EARS-02]` WHEN elevator discrepancy exceeds 1.5 deg, the FCC shall assert bypass mode. |
| **State-Driven (Durum Bağımlı)** | *WHILE `<state>`, the `<system>` shall `<action>`.* | Belirli bir uçuş veya çalışma modundaki davranış | `[HLR-EARS-03]` WHILE in Landing Phase, the FCC shall restrict bank angle to 25 degrees. |
| **Unwanted Behavior (İstenmeyen Durum)** | *IF `<condition>`, THEN the `<system>` shall `<action>`.* | Hata yakalama, sınır aşımı veya arıza yönetimi | `[HLR-EARS-04]` IF sensor data is stale for >50ms, THEN the system shall flag sensor invalid. |
| **Optional Feature (Seçeneğe Bağlı)** | *WHERE `<feature>`, the `<system>` shall `<action>`.* | Donanım konfigürasyonuna göre değişen işlev | `[SYS-EARS-05]` WHERE TCAS hardware is fitted, the system shall provide audio collision alerts. |

---

## 3. "Shall", "Should", "May" Hukuki Semantiği
- **SHALL (Zorunlu):** Sertifikasyon için test edilmesi ve doğrulanması yasal olarak zorunlu gereksinim.
- **SHOULD (Tavsiye):** Emniyet riski oluşturmayan mimari tavsiye (Sertifikasyon gereksinimi olarak kullanılmamalıdır).
- **MAY (İsteğe Bağlı):** Opsiyonel işlevsellik.

---

## 4. Kötü vs. İyi Gereksinim Karşılaştırması

❌ **Kötü Gereksinim:**
> *"Sistem aşırı sıcaklıklarda motoru korumalı ve gerektiğinde pilotu uyarmalıdır."*
*(Hata: "aşırı sıcaklık" kaç derece? "korumalı" nasıl bir eylem? "gerektiğinde" ne zaman?)*

✅ **İyi Gereksinim (EARS Uyumlu):**
> `[SYS-ENG-088]` WHEN engine core temperature exceeds 850°C for more than 500 ms, the FADEC shall illuminate the ENGINE_OVERHEAT caution lamp within 100 ms.
