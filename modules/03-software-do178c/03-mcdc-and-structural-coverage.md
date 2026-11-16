# 📘 Modül 3.3: Yapısal Kod Kapsama ve MC/DC (Modified Condition/Decision Coverage)

## 1. Kod Kapsama Seviyeleri Nelerdir?
Geleneksel testlerde genellikle kodun çalışıp çalışmadığına bakılır. Emniyet-kritik yazılımlarda (DO-178C DAL A/B/C ve ISO 26262 ASIL D) testlerin kaynak kodun mantıksal yollarını ne kadar kapsamlı tetiklediği matematiksel olarak kanıtlanmalıdır.

1. **Statement Coverage (DAL C):** Koddaki her yürütülebilir satır en az 1 kez çalıştırıldı mı?
2. **Decision Coverage / Branch (DAL B):** Her `if`, `while`, `switch` kararının hem `TRUE` hem de `FALSE` dalları test edildi mi?
3. **MC/DC Coverage (DAL A):** Kararı oluşturan her bir alt koşulun (condition), diğer koşullar sabit tutulurken nihai kararı tek başına değiştirebildiği kanıtlandı mı?

---

## 2. MC/DC Matematiksel Mantığı ve Doğruluk Tablosu

Örnek Bir Uçuş Emniyet Kararı:
```c
/* Motor kapatma kararı: Karar = (A OR B) AND C */
bool shutdown = (over_temp || fuel_leak) && engine_running;
```
Burada:
- **Koşul A:** `over_temp`
- **Koşul B:** `fuel_leak`
- **Koşul C:** `engine_running`
- **Nihai Karar (Decision):** `(A || B) && C`

Toplam $2^3 = 8$ olası kombinasyon vardır. Ancak MC/DC test süresi ve karmaşıklığı patlatmadan **$N + 1$ adet test vakası** ile bağımsız etkiyi kanıtlar ($3 + 1 = 4$ test).

| Test Vaka ID | A (`over_temp`) | B (`fuel_leak`) | C (`running`) | Karar Çıktısı | Hangi Koşulun Bağımsız Etkisini Kanıtlar? |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **T1** | **FALSE** | **FALSE** | TRUE | **FALSE** | Referans Durumu |
| **T2** | **TRUE**  | FALSE | TRUE | **TRUE**  | **A Koşulu Kanıtlandı:** T1 ve T2'de B ve C aynı, A değişti, Karar değişti! |
| **T3** | FALSE | **TRUE**  | TRUE | **TRUE**  | **B Koşulu Kanıtlandı:** T1 ve T3'te A ve C aynı, B değişti, Karar değişti! |
| **T4** | TRUE  | FALSE | **FALSE**| **FALSE** | **C Koşulu Kanıtlandı:** T2 ve T4'te A ve B aynı, C değişti, Karar değişti! |

> ✅ **Sonuç:** Sadece 4 test vakası (T1, T2, T3, T4) ile DO-178C DAL A seviyesinde tam MC/DC kanıtı sağlanmış olur.

---

## 3. Ölü Kod (Dead Code) vs. Devre Dışı Kod (Deactivated Code)
- **Ölü Kod (Dead Code):** Gereksinimi olmayan ve hiçbir koşulda icra edilemeyen kod parçasıdır (örn: `if (0) { ... }` veya artık fonksiyonlar). DAL A sistemlerde **kesinlikle yasaktır ve temizlenmelidir**.
- **Devre Dışı Kod (Deactivated Code):** Bilinçli olarak kapatılan kodlardır (örneğin sadece yerde bakım modunda çalışan kodlar). Varlığı gerekçelendirilmeli ve uçuş sırasında aktive olamayacağı kanıtlanmalıdır.

---

## 4. İzlenebilirlik İlişkisi
- `[LLR-MCDC-01]` Yangın söndürme valfi kararı `(temp_high || smoke_detected) && valve_armed` koşulunu sağlamalıdır.
- `[UTEST-MCDC-01]` MC/DC matrisi 4 test vakası ile `[LLR-MCDC-01]`'i doğrulamalıdır.
