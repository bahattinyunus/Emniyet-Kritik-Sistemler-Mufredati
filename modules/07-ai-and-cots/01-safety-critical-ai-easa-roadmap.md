# 📘 Modül 7.1: Emniyet-Kritik Sistemlerde Yapay Zeka (AI) ve EASA Yol Haritası

## 1. Emniyet-Kritik Sistemlerde Neden Yapay Zeka Sertifikasyonu Zordur?
Klasik yazılım mühendisliğinde (DO-178C) her kod satırı bir gereksinime dayanır ve %100 deterministiktir. 
Yapay zeka (Derin Öğrenme / Sinir Ağları) ise:
- **Kara Kutu (Black Box):** Milyarlarca parametre arasındaki ağırlıkların neden o kararı verdiği formel olarak kanıtlanamaz.
- **İstatistiki Belirsizlik:** %99.9 doğruluk, $10^{-9}$ emniyet gerektiren havacılık için yetersizdir.
- **Out-of-Distribution (OOD):** Model eğitim setinde hiç görmediği bir girdiyle karşılaştığında tamamen saçmalayabilir.

---

## 2. EASA AI Yol Haritası (AI Roadmap 2.0)
Avrupa Havacılık Emniyeti Ajansı (EASA), yapay zekanın havacılığa entegrasyonu için 3 kademeli bir evrim tanımlamıştır:

1. **Seviye 1A/1B (Mürettebat Destek / İnsan Merkezli):** Yapay zeka pilota öneride bulunur (örn: türbülans tahmini), son karar ve yetki tamamen pilottadır.
2. **Seviye 2 (İnsan-Yapay Zeka İşbirliği):** Yapay zeka belirli görevleri otonom icra eder, insan gözetmen konumundadır.
3. **Seviye 3 (Tam Otonomi):** İnsan kokpitte bulunmaz. Tamamen sertifikalı, kendi kendini izleyen ve kurtaran yapay zeka sistemleri.

---

## 3. Güvenilirlik ve Açıklanabilirlik (Explainability & Trustworthiness)
- **W-Shaped V-Model:** Makine öğrenmesi yaşam döngüsü veri hazırlığı, model eğitimi ve model doğrulaması ile genişletilir.
- **Formel Doğrulama:** Ağırlıkların belirli bir girdi aralığında istenmeyen bir çıktı üretmeyeceğinin matematiksel ispatı (Abstract Interpretation, SMT Çözücüler).
