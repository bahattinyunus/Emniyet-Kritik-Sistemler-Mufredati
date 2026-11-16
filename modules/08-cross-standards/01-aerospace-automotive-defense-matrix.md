# 📘 Modül 8.1: Çapraz Sektörel Fonksiyonel Emniyet Matrisi

## 1. Standartların Karşılaştırmalı Eşleşmesi

| Özellik / Kriter | Havacılık (Civil Aviation) | Otomotiv (Automotive) | Savunma (Defense) | Raylı Sistemler (Rail) | Genel Endüstriyel / Tıp |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ana Emniyet Standardı** | SAE ARP 4761A / ARP 4754B | ISO 26262 / ISO 21448 | MIL-STD-882E | CENELEC EN 50126 / 50129 | IEC 61508 / IEC 62304 |
| **Yazılım Standardı** | RTCA DO-178C (ED-12C) | ISO 26262 Part 6 | MIL-STD-882E SwHA | CENELEC EN 50128 | IEC 61508-3 / IEC 62304 |
| **Donanım Standardı** | RTCA DO-254 (ED-80) | ISO 26262 Part 5 | MIL-STD-882E HwHA | CENELEC EN 50129 | IEC 61508-2 |
| **Kritiklik Seviyesi** | **DAL A** | **ASIL D** | **Level 1 / Catastrophic** | **SIL 4** | **SIL 4 / Class C** |
| **İzin Verilen Hata Olasılığı**| $< 10^{-9}$ / uçuş saati | $< 10^{-8}$ / saat (FIT < 10)| Tanımlı Risk Matrisi | $< 10^{-9}$ / saat | $< 10^{-8}$ / saat |
| **Zorunlu Kod Kapsamı** | MC/DC (DAL A) | MC/DC (ASIL D) | Statik/Dinamik Analiz | Branch / MC/DC | MC/DC Kapsamı |

---

## 2. Farklılıklar ve Yaklaşım Felsefeleri

### Havacılık (DO-178C / ARP 4754B):
- **Süreç Güvencesi (Process Assurance):** Geliştirme sürecinin her adımının denetlenmesi ve izlenebilirliğin eksiksiz olması esastır. Hata olasılığı $10^{-9}$ gibi son derece düşüktür çünkü bir uçak havada durup kenara çekemez.

### Otomotiv (ISO 26262):
- **Güvenli Duruma Geçiş (Safe State):** Otomobilde bir arıza olduğunda araç kenara çekip durdurulabilir (Fail-Safe). Havacılıktan farklı olarak sürücünün arızayı telafi edebilme yeteneği (**Controllability**) risk analizine (HARA) dahil edilir.

### Savunma (MIL-STD-882E):
- **Görev vs. Emniyet Dengesi:** Görevin icrası ile tehlikelerin bertaraf edilmesi arasındaki denge askeri makamlarca risk kabulü (Risk Acceptance) ile yönetilir.

---

## 3. Kariyer ve Sertifikasyon Yol Haritası
Bir emniyet mühendisi için standartlar arası geçiş terminoloji farklarını anlamaktan geçer:
- Havacılıktaki **FHA**, otomotivde **HARA** (Hazard Analysis and Risk Assessment) olarak adlandırılır.
- Havacılıktaki **DAL A**, otomotivdeki **ASIL D** ve endüstriyeldeki **SIL 4** seviyesine denktir.
