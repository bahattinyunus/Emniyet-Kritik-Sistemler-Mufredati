# 📘 Modül 1.2: Fonksiyonel Tehlike Değerlendirmesi (FHA)

## 1. FHA (Functional Hazard Assessment) Nedir?
ARP 4761A standardı uyarınca FHA, sistem seviyesindeki fonksiyonların başarısız olması durumunda ortaya çıkacak potansiyel sonuçları ve bu sonuçların şiddetini sınıflandırma sürecidir.

## 2. Hata Durumu Sınıflandırması
1. **Catastrophic (DAL A):** Uçağın ve canların kaybına yol açan durumlar ($P < 10^{-9}$ / uçuş saati).
2. **Hazardous / Severe-Major (DAL B):** Görev kabiliyetinde ağır düşüş, mürettebatta yüksek stres ve aşırı iş yükü ($P < 10^{-7}$ / uçuş saati).
3. **Major (DAL C):** Mürettebat iş yükünde artış, emniyet paylarında azalma ($P < 10^{-5}$ / uçuş saati).
4. **Minor (DAL D):** Rutin prosedürlerle kontrol altına alınabilen küçük sapmalar ($P < 10^{-3}$ / uçuş saati).
5. **No Safety Effect (DAL E):** Uçuş emniyetine hiçbir olumsuz etkisi bulunmayan işlevler.

## 3. İzlenebilirlik Örneği
* Tehlike: `[HAZ-FCS-01]` İrtifa kumandasının kilitlenmesi veya aşırı komut üretmesi.
* Önlem: `[SYS-FCS-01]` Çift kanallı mimari ve otomatik ayrıştırma devresi.
