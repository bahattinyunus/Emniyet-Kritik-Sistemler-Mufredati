# 📑 Emniyet Vakası (Safety Case) ve Hedef Yapılandırma Notasyonu (GSN)

## 1. Safety Case Nedir?

Bir sistemin belirli bir operasyonel ortamda kabul edilebilir seviyede emniyetli olduğunu iddia eden (**Claim**), bu iddiayı mantıksal argümanlarla savunan (**Argument**) ve somut doğrulama kanıtlarıyla destekleyen (**Evidence**) yapılandırılmış dokümana **Safety Case (Emniyet Dosyası)** denir.

---

## 2. GSN (Goal Structuring Notation) Temel Elemanları

```mermaid
graph TD
    G1["G1 (Ana Hedef): Sistem tanımlı uçuş rejiminde emniyetlidir"]
    C1["C1 (Bağlam): Uçuş zarfı ve çevre şartları (DO-160G)"]
    A1["A1 (Argüman): Tüm kritik tehlikeler analiz edilmiş ve izole edilmiştir"]
    G2["G2 (Alt Hedef): Donanımsal tekil arızalar felakete yol açmaz"]
    G3["G3 (Alt Hedef): Yazılım DAL A gereksinimlerini karşılar"]
    Sn1["Sn1 (Kanıt): SSA ve FTA Raporu (ARP 4761A)"]
    Sn2["Sn2 (Kanıt): %100 MC/DC Test Raporu (DO-178C)"]

    G1 --- C1
    G1 --> A1
    A1 --> G2
    A1 --> G3
    G2 --> Sn1
    G3 --> Sn2

    classDef goal fill:#1e3a8a,stroke:#3b82f6,stroke-width:2px,color:#fff;
    classDef context fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#fff;
    classDef arg fill:#701a75,stroke:#c084fc,stroke-width:2px,color:#fff;
    classDef evidence fill:#78350f,stroke:#f59e0b,stroke-width:2px,color:#fff;

    class G1,G2,G3 goal;
    class C1 context;
    class A1 arg;
    class Sn1,Sn2 evidence;
```

* **Hedef (Goal):** Emniyet ile ilgili doğrulanması gereken iddia.
* **Bağlam (Context):** Hedefin geçerli olduğu operasyonel ortam ve varsayımlar.
* **Argüman (Argument):** Hedefin alt hedeflere nasıl bölündüğünü açıklayan mantıksal kurgu.
* **Kanıt (Solution / Evidence):** Hedefin başarıldığını gösteren test sonuçları, analizler, sertifikalar.
