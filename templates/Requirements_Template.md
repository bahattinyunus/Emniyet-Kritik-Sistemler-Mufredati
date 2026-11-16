# 📑 EARS Metodolojisi ile Gereksinim Şablonu
> **Referans Standart:** ARP 4754B (SYSR) / RTCA DO-178C (HLR & LLR)

## 1. Gereksinim Hiyerarşisi

```
[HAZ-XXX] (Tehlike Kaydı)
   └── [SYS-XXX] (Sistem Gereksinimi - ARP 4754B)
         ├── [HLR-XXX] (Üst Seviye Yazılım Gereksinimi - DO-178C)
         │     └── [LLR-XXX] (Alt Seviye Tasarım Gereksinimi)
         │           ├── Kod Gerçeklemesi (C/C++ / MISRA)
         │           └── [UTEST-XXX] (Birim / MC-DC Testi)
         └── [HWR-XXX] (Donanım Gereksinimi - DO-254)
               └── [HIL-XXX] (Donanım Doğrulama Testi)
```

---

## 2. EARS (Easy Approach to Requirements Syntax) Kalıpları

Emniyet-kritik sistemlerde gereksinimler **yoruma kapalı, tekil (atomik), test edilebilir ve izlenebilir** olmalıdır:

1. **Ubiquitous (Her zaman geçerli):**
   * *Format:* Sistem [eylemi] yapacaktır / `shall [action]`.
   * *Örnek:* `[SYS-001]` Sistem, güç verildiği andan itibaren her 10 milisaniyede bir kalp atışı (heartbeat) sinyali üretecektir.

2. **Event-Driven (Olay Tetiklemeli):**
   * *Format:* [Olay] gerçekleştiğinde, sistem [eylemi] yapacaktır / `WHEN [event], the system shall [action]`.
   * *Örnek:* `[SYS-002]` Birincil sensör veri kaybı algılandığında, sistem 5 ms içinde ikincil sensör hattına geçiş yapacaktır.

3. **State-Driven (Durum Tabanlı):**
   * *Format:* [Durumda] iken, sistem [eylemi] yapacaktır / `WHILE [state], the system shall [action]`.
   * *Örnek:* `[SYS-003]` Uçuş modu "TIRMANMA" durumunda iken, sistem maksimum hücum açısı sınırlayıcısını devrede tutacaktır.

4. **Unwanted Behavior (İstenmeyen / Arıza Durumu):**
   * *Format:* Eğer [arıza] oluşursa, sistem [eylemi] yapacaktır / `IF [fault], THEN the system shall [action]`.
   * *Örnek:* `[HLR-010]` EĞER ARINC 429 hattından gelen veri parite hatası içerirse, O ZAMAN yazılım ilgili veriyi geçersiz (invalid) olarak işaretleyecektir.

---

## 3. Örnek İzlenebilirlik Tablosu

| Gereksinim ID | Üst Seviye Referansı | EARS Tipi | Gereksinim Metni | Güvence Seviyesi | Doğrulama Yöntemi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`[SYS-FCS-101]`** | `[HAZ-002]` | Event-Driven | Birincil ve ikincil kanal arasındaki fark 1.5 dereceyi aştığında, sistem aktüatörü ayıracaktır. | DAL A | HIL Testi / Analiz |
| **`[HLR-FCS-201]`** | `[SYS-FCS-101]` | State-Driven | Kontrol döngüsü çalışırken, yazılım her 10 ms'de sapma miktarını hesaplayacaktır. | DAL A | Yazılım Entegrasyon Testi |
| **`[LLR-FCS-301]`** | `[HLR-FCS-201]` | Unwanted Behavior | EĞER ardışık 2 döngüde sapma eşik değerin üzerindeyse, O ZAMAN shutoff bayrağı 1 yapılacaktır. | DAL A | MC/DC Birim Testi `[UTEST-001]` |
