# Akıllı Etkinlik Planlama Platformu

Bu proje, kullanıcıların etkinlik oluşturabileceği, katılabileceği ve etkinliklerle ilgili sosyal etkileşimde bulunabileceği bir web tabanlı Akıllı Etkinlik Planlama Platformu'dur. Platform, kullanıcıların etkinlikleri kişiselleştirilmiş öneriler, haritalar ve mesajlaşma sistemiyle takip etmelerine olanak tanır.

## Projenin Özeti

Akıllı Etkinlik Planlama Platformu, sosyal etkinliklerin planlanmasını kolaylaştırmak için tasarlanmıştır. Kullanıcılar:
- Kendi etkinliklerini oluşturabilir ve yönetebilir,
- İlgi alanlarına uygun kişiselleştirilmiş öneriler alabilir,
- Etkinlikler etrafında sosyal etkileşimde bulunabilir,
- Harita ve rota önerilerini kullanarak etkinliklere kolayca ulaşabilir.

---

## Proje Amaçları

- Web programlama becerilerinin geliştirilmesi,
- Veritabanı tasarımı ve yönetimi konusunda deneyim kazanılması,
- Dinamik, kullanıcı dostu bir web platformu geliştirilmesi,
- Gerçek zamanlı veri işleme ve kullanıcı etkileşimi sistemlerinin oluşturulması,
- API entegrasyonları ve harita işlevleriyle kullanıcı deneyiminin zenginleştirilmesi.

---

## Kullanılan Teknolojiler

- **Frontend**: HTML, CSS
- **Backend**: Django
- **Veritabanı**: MySQL
- **Harita Fonksiyonları**: [OpenStreetMap](https://www.openstreetmap.org)

---

## Temel Özellikler

1. **Kullanıcı Yönetimi**
   - Kayıt olma, giriş yapma, profil düzenleme
   - Kullanıcı rolleri (Admin, Kullanıcı) ile yetkilendirme
2. **Etkinlik Yönetimi**
   - Etkinlik oluşturma, güncelleme ve silme
   - Katılım yönetimi ve öneri sistemi
3. **Kural Tabanlı Öneri Sistemi**
   - İlgi alanı, konum ve katılım geçmişine göre öneriler
4. **Zaman Çakışma Algoritması**
   - Etkinlik zamanlarının çakışmasını kontrol etme
5. **Harita ve Rota Planlama**
   - OpenStreetMap API ile etkinlik konumlarını gösterme ve rota önerileri
6. **Mesajlaşma**
   - Her etkinlik için ayrı sohbet alanı
   - Mesaj geçmişi saklama

---

## Veritabanı Tasarımı

Projede ilişkisel bir veritabanı kullanılmıştır. Tablolar şu şekilde tasarlanmıştır:
- **Kullanıcılar**: ID, kullanıcı adı, şifre, e-posta, konum, ilgi alanları vb.
- **Etkinlikler**: ID, etkinlik adı, tarih, açıklama, konum vb.
- **Katılımcılar**: Kullanıcı ID, Etkinlik ID
- **Mesajlar**: Mesaj ID, Gönderici ID, Alıcı ID, Mesaj Metni, Gönderim Zamanı
- **Puanlar**: Kullanıcı ID, Puanlar, Kazanılan Tarih

---


### Gerekli Bağımlılıklar
- MySQL
- Python 


### Görseller:
  - `![Ekran Görüntüsü](images/Ekran%20görüntüsü%202024-12-05%20171719.png)`
  - `![Opera Anlık Görüntü](images/Opera%20Anlık%20Görüntü_2024-12-05_173637_127.0.0.1.png)`
  

### Kurulum Adımları
- **Depoyu Klonlama** adımındaki bağlantıyı şu şekilde güncelledim:
  ```bash
  git clone https://github.com/icsiee/EtkinlikPlatformu.git
  cd EtkinlikPlatformu

