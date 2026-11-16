# 🛡️ Emniyet-Kritik Sistemlerde MISRA C ve Güvenli Kodlama Kılavuzu

Emniyet-kritik yazılımlarda (DO-178C DAL A/B, ISO 26262 ASIL D, EN 50128 SIL 4) kod kalitesi ve determinizm hayati önem taşır. Kodun derleyici optimizasyonlarından ve tanımsız davranışlardan (Undefined Behavior) etkilenmemesi gerekir.

---

## 1. Altın Kurallar (Golden Rules)

### ❌ 1. Dinamik Bellek Tahsisi Yasaktır
* `malloc()`, `calloc()`, `realloc()`, `free()` ve C++ için `new`/`delete` kullanımı kesinlikle yasaktır.
* **Neden?** Bellek parçalanması (fragmentation), yetersiz bellek hatası (out of memory) ve deterministik olmayan çalışma zamanı riskleri.
* **Çözüm:** Tüm veri yapıları statik veya yığın (stack) üzerinde derleme zamanında boyutlandırılmalıdır.

### ❌ 2. Sınırsız / Özyinelemeli (Recursive) Fonksiyonlar Yasaktır
* Bir fonksiyonun doğrudan veya dolaylı olarak kendini çağırması yasaktır.
* **Neden?** Yığın taşması (Stack Overflow) riskinin ve Maksimum Yığın Tüketiminin (Worst-Case Stack Usage) statik olarak hesaplanmasını imkansız kılar.

### ❌ 3. Standart Tipler Yerine Sabit Genişlikli Tipler Kullanılmalıdır
* `int`, `long`, `short` yerine `<stdint.h>` içindeki `int32_t`, `uint32_t`, `int16_t`, `uint8_t` tipleri zorunludur.
* **Neden?** Donanım mimarisine bağlı taşma ve gösterim farklılıklarını önlemek.

### ❌ 4. İşaretçi Aritmetiği (Pointer Arithmetic) Sınırlandırılmalıdır
* Dizi indisleme tercih edilmeli, doğrudan adres artırma/azaltma yapılmamalıdır.
* Her işaretçi kullanılmadan önce `NULL` denetiminden geçirilmelidir.

---

## 2. Örnek MISRA Uyumlu Kod Deseni

```c
#include <stdint.h>
#include <stdbool.h>

#define SENSOR_ARRAY_CAPACITY  (8U)
#define SENSOR_UPPER_LIMIT_MV  (5000U)

typedef struct {
    uint32_t raw_samples[SENSOR_ARRAY_CAPACITY];
    uint32_t valid_sample_count;
    bool     fault_detected;
} SensorChannel_t;

void SensorChannel_Process(SensorChannel_t * const channel)
{
    /* Kural: Null pointer denetimi */
    if (channel == (void *)0) {
        return;
    }

    uint32_t sum = 0U;
    uint32_t i;

    /* Kural: Statik sınırlar ve deterministik döngü */
    for (i = 0U; i < SENSOR_ARRAY_CAPACITY; i++) {
        if (channel->raw_samples[i] > SENSOR_UPPER_LIMIT_MV) {
            channel->fault_detected = true;
            break;
        }
        sum += channel->raw_samples[i];
    }

    if (!channel->fault_detected) {
        channel->valid_sample_count = SENSOR_ARRAY_CAPACITY;
    }
}
```
