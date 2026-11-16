# 📘 Modül 5.1: Gerçek Zamanlı Sistemler ve Determinizm (Hard Real-Time & WCET)

## 1. Hard Real-Time vs. Soft Real-Time
- **Soft Real-Time:** Bir görevin zamanında tamamlanması istenir ancak gecikmesi sistemin çökmesine neden olmaz (Örn: Video akışı).
- **Hard Real-Time:** Bir görevin doğru sonucu üretmesi tek başına yeterli değildir; sonucun **kesinlikle belirlenen son teslim tarihinden (Deadline)** önce üretilmesi şarttır. Bir milisaniyelik gecikme feci bir kazaya yol açabilir (Örn: Uçuş kontrol yüzeyi komutu veya hava yastığı açılma kararı).

---

## 2. Jitter ve WCET (Worst-Case Execution Time)

### A. WCET (En Kötü Durum İcra Süresi)
Bir yazılım fonksiyonunun en olumsuz girdi kombinasyonlarında, önbellek kaçırmalarında (cache misses) ve veri yolu çakışmalarında çalışabileceği en uzun süredir.
- Görev periyodu $T$ ise, emniyet kuralı:
  $$\text{WCET} < \text{Deadline} \le T$$

### B. Jitter (Zaman Salınımı)
Periyodik bir görevin başlama veya bitiş anındaki zamansal sapmadır. Kontrol algoritmalarında yüksek jitter, faz gecikmesine ve sistemin kararsızlaşmasına (instability) neden olur.

---

## 3. Deterministik Zamanlama Algoritmaları
- **Rate Monotonic Scheduling (RMS):** Periyodu kısa olan göreve yüksek öncelik verilir. Statik ve tahmin edilebilirdir.
- **Zaman Dilimli (Time-Triggered / Cyclic Executive):** Kesmeler yerine önceden tanımlanmış statik zaman tablolarına dayanır. Emniyet-kritik aviyonik sistemlerin vazgeçilmezidir.
