# 📘 Modül 3.4: Deterministik Kodlama & MISRA C:2012 / MISRA C++:2023

## 1. Neden C ve C++ Tehlikelidir?
C ve C++ dilleri; tanımsız davranışlar (Undefined Behavior), örtülü tip dönüşümleri (Implicit Type Conversions), işaretçi aritmetiği ve bellek sınır kontrollerinin olmaması nedeniyle kontrolsüz kullanıldığında emniyet-kritik sistemlerde ölümcül hatalara yol açabilir.

MISRA (Motor Industry Software Reliability Association), bu riskleri minimize etmek için endüstri standardı haline gelmiş kural setleridir.

---

## 2. Emniyet-Kritik Sistemlerdeki Temel Kodlama Kısıtları

### 1. Dinamik Bellek Tahsisinin Kesinlikle Yasaklanması
```c
/* ❌ KESİNLİKLE YASAK (MISRA C:2012 Rule 21.3) */
void *ptr = malloc(sizeof(SensorData_t));

/* ✅ DOĞRU YAKLAŞIM: Statik Bellek Tahsisi */
static SensorData_t g_sensor_buffer[MAX_SENSORS];
```
*Gerekçe:* Heap parçalanması (fragmentation), bellek sızıntısı (memory leak) ve `malloc`'un deterministik çalışma süresi garantisi verememesi.

### 2. Özyineleme (Recursion) Yasağı
```c
/* ❌ KESİNLİKLE YASAK (MISRA C:2012 Rule 17.2) */
uint32_t Factorial(uint32_t n) {
    if (n <= 1) return 1;
    return n * Factorial(n - 1); /* Yığın taşmasına (Stack Overflow) yol açabilir */
}

/* ✅ DOĞRU YAKLAŞIM: Deterministik Döngü */
uint32_t Factorial_Iterative(uint32_t n) {
    uint32_t result = 1U;
    for (uint32_t i = 1U; (i <= n) && (i <= MAX_BOUND); i++) {
        result *= i;
    }
    return result;
}
```

### 3. İşaretçi Aritmetiği ve Tip Güvenliği
```c
/* ❌ YASAK: Standart int kullanımı ve tanımsız işaretçi kaydırma */
int *p = buffer;
p += 4; 

/* ✅ DOĞRU: <stdint.h> açık boyutlu tipler ve dizi indisleme */
uint32_t value = buffer[4U];
```

---

## 3. Statik Kod Analizi ve Kalifikasyon (DO-330)
- Emniyet projelerinde MISRA kuralları insan gözüyle değil, onaylı (Qualified Tool) statik analiz araçlarıyla (Coverity, Polyspace, PC-lint, SonarQube) otomatik denetlenir.
- Eğer bir kural ihlal edilmek zorundaysa (örneğin donanım register adresine doğrudan işaretçi atama), resmi bir **Sapma Raporu (Deviation Report)** yazılmalı ve gerekçelendirilmelidir.
