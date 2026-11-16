# 📋 Şablon: GSN (Goal Structuring Notation) Tabanlı Emniyet Dosyası (Safety Case)

## 1. Doküman Bilgileri
- **Proje Adı:** `[PROJE ADI]`
- **Sistem / LRU:** `[SİSTEM ADI]`
- **Güvence Seviyesi:** DO-178C DAL A / ISO 26262 ASIL D
- **Versiyon:** 1.0.0
- **Tarih:** 2026-11-16

---

## 2. GSN Emniyet İddia Hiyerarşisi

```mermaid
graph TD
    G1["G1 (Ana Hedef): Sistem tanımlanan operasyonel profilde kabul edilebilir düzeyde emniyetlidir."]
    S1["S1 (Strateji): Tehlike kategorilerine ve bağımsız mimari bariyerlere göre argüman geliştirme."]
    
    G2["G2: [HAZ-01] İstenmeyen aktüatör hareketi riski 10^-9/saat seviyesine indirilmiştir."]
    G3["G3: Yazılım hatalarından kaynaklı tekil nokta arızaları elenmiştir."]
    
    E1["E1 (Kanıt): ARP 4761A FHA ve FTA Raporu (Ek A)"]
    E2["E2 (Kanıt): DO-178C DAL A MC/DC Yapısal Kapsam Test Raporu (Ek B)"]
    E3["E3 (Kanıt): Çift kanallı COM/MON HIL Entegrasyon Test Kayıtları"]

    G1 --> S1
    S1 --> G2
    S1 --> G3
    G2 --> E1
    G2 --> E3
    G3 --> E2
```

---

## 3. GSN Argüman Elemanları

### Hedefler (Goals):
- **`[G1]`**: Sistem tüm operasyonel fazlarda kaza olasılığını $10^{-9}$/saat sınırında tutar.
- **`[G2]`**: Uçuş kontrol bilgisayarı yazılımı hiçbir tanımsız davranış (Undefined Behavior) içermez.

### Çözümler ve Kanıtlar (Evidence / Solutions):
- **`[E1 - Statik Analiz]`**: MISRA C:2012 kural ihlali bulunmamaktadır (Polyspace / Coverity sıfır hata raporu).
- **`[E2 - Dinamik Kapsam]`**: %100 Statement, %100 Branch ve %100 MC/DC kapsamı elde edilmiştir.
- **`[E3 - İzlenebilirlik]`**: Çift yönlü RTM matrisi boşluksuz olarak tamamlanmıştır.
