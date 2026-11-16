# 📘 Modül 6.1: Havacılık Veri Yolları (ARINC 429, MIL-STD-1553B & AFDX)

## 1. Veri Yollarının Karşılaştırmalı Özeti

| Protokol | Geliştirici / Standart | Topoloji | Hız | Determinizm Türü | Temel Kullanım Alanı |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ARINC 429** | Aeronautical Radio Inc. | Point-to-Point / Simplex | 12.5 - 100 kbps | Donanımsal Tek Yönlü | Sivil Uçak Aviyonikleri |
| **MIL-STD-1553B** | ABD Savunma Bakanlığı | Çift Yedekli Veri Yolu | 1 Mbps | Komuta / Yanıt (Master-Slave) | Askeri Uçak, Tank, Uydu |
| **AFDX (ARINC 664)** | Airbus / Boeing / SAE | Yıldız (Switched Ethernet) | 10 - 100 Mbps | Virtual Link (Zaman & Bant Kısıtlı) | A380, A350, B787 Modern Jetler |

---

## 2. ARINC 429 Veri Formatı (32-Bit Kelime Yapısı)
ARINC 429, tek bir vericinin (Transmitter) en fazla 20 alıcıya (Receiver) veri gönderdiği bükümlü çift kablo mimarisidir.

```text
Bit 32         Bit 30 29        Bit 11 10      Bit 9 8        Bit 1
+-------------+------+---------------+--------+------+-------------+
|   Parity    | SSM  |     Data      |  SDI   |     Label (Sekizlik)|
| (Odd/Even)  | (2b) |    (19-bit)   |  (2b)  |         (8-bit)     |
+-------------+------+---------------+--------+------+-------------+
```
- **Label (8-bit):** Bilginin türü (Örn: `203` İrtifa, `204` Barometrik Düzeltme).
- **SDI (Source/Destination Identifier):** Hangi alt sistemden geldiği.
- **SSM (Sign/Status Matrix):** Verinin geçerliliği (Normal, Uyarı, Test, Arıza).
- **Parity (1-bit):** İletim hattındaki tek bitlik bozulmaları yakalamak için.

---

## 3. AFDX (Avionics Full-Duplex Switched Ethernet)
Standart Ethernet deterministik değildir (CSMA/CD çakışmaları ve belirsiz gecikmeler). AFDX bu sorunu iki ana patentli mekanizmayla çözer:
1. **Virtual Link (VL):** Fiziksel ağ üzerinde mantıksal izole tüneller oluşturur.
2. **BAG (Bandwidth Allocation Gap):** İki ardışık çerçeve arasındaki minimum bekleme süresidir (örn: 1 ms, 2 ms, 4 ms). Böylece bir istasyon ağı asla kilitleyemez.
