# 📋 Fonksiyonel Tehlike Değerlendirmesi (FHA) Şablonu
> **Referans Standart:** SAE ARP 4761A / ARP 4754B

## 1. Sistem ve Fonksiyon Tanımı
* **Sistem Adı:** [Örn: Uçuş Kontrol Sistemi - FCS]
* **Alt Sistem / Fonksiyon:** [Örn: Pitch Ekseni Trim Kontrolü]
* **Sistem Mühendisi:** [İsim / Ekip]
* **Tarih & Versiyon:** [YYYY-MM-DD / v1.0]

---

## 2. Fonksiyonel Hata Durumları ve Tehlike Tablosu

| Tehlike ID | Fonksiyonel Hata Tanımı | Operasyonel Uçuş Fazı | Hata Etkisi (Uçak, Ekip, Yolcu) | Şiddet Seviyesi (Severity) | Tasarım Güvence Seviyesi (DAL) | İzin Verilen Max Olasılık (/saat) | Doğrulama & İyileştirme Stratejisi |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`[HAZ-001]`** | Fonksiyonun tamamen kaybı (Loss of function) | Kalkış / Tırmanma | Pilot yükünü artırır, alternatif yedek kanal devrededir | Major | DAL C | $< 10^{-5}$ | Bağımsız yedek trim kanalı |
| **`[HAZ-002]`** | İstenmeyen / Yanlış komut üretimi (Uncommanded / Malfunction) | Seyir / Alçalış | İrtifa kumandasında kontrolsüz dalış veya yunuslama | Catastrophic | DAL A | $< 10^{-9}$ | COM/MON çift kanal mimarisi ve donanımsal cut-off |
| **`[HAZ-003]`** | Komut iletiminde aşırı gecikme (>150ms latency) | Son Yaklaşma / İniş | Pilot uçağı stabil tutmakta zorlanır | Hazardous | DAL B | $< 10^{-7}$ | Deterministik ARINC 429 yolu ve watchdog zamanlayıcısı |

---

## 3. Tehlike Sınıflandırma Kılavuzu

* **Catastrophic (DAL A):** Uçağın kaybı ve/veya çoklu ölümcül yaralanmalar.
* **Hazardous / Severe-Major (DAL B):** Uçağın operasyonel kabiliyetinde kritik düşüş, ekipte yüksek stres/iş yükü, yolcularda ciddi yaralanma.
* **Major (DAL C):** Operasyonel kısıtlar, emniyet marjlarında azalma, hafif yaralanmalar.
* **Minor (DAL D):** Rutin prosedürlerle tolere edilebilen hafif emniyet etkisi.
* **No Safety Effect (DAL E):** Emniyete hiçbir etkisi olmayan durumlar.
