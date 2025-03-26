import heapq
import random

class Event:
    def __init__(self, time, type, passenger=None):
        self.time = time  # Olayın zamanı
        self.type = type  # Olayın türü: 'arrival', 'inspection', veya 'departure'
        self.passenger = passenger  

    def __lt__(self, other):
        return self.time < other.time  # Olayları zamanlarına göre karşılaştırma

class Passenger:
    def __init__(self, id, arrival_time):
        self.id = id  # Yolcunun benzersiz kimliği
        self.arrival_time = arrival_time  # Yolcunun varış zamanı
        self.denied = False  # Yolcunun reddedilip reddedilmediği

def generate_arrival_time(current_time):
    return current_time + random.uniform(3, 7)  # Her bir yolcu için 5±2 dakika aralığında rastgele varış zamanı üretir

def generate_inspection_time():
    return random.expovariate(1/10)  # Her bir yolcu için ortalama 10 dakika olan üstel dağılımlı havaalanında inceleme süresi üretir

def simulation():
    FEL = []  # Gelecekteki Olay Listesi (Future Event List) olarak min heap
    queue = []  # İnceleme için bekleyen yolcuların kuyruğu
    denied_passengers = 0  # Reddedilen yolcu sayısı
    max_queue_length = 0  # Kuyrukta bulunan maksimum yolcu sayısı
    passenger_id_counter = 0  # Yolcu ID'lerini saymak için sayaç
    queue_length_times = []  # Kuyruk uzunluklarının sürelerini izlemek için liste
    last_event_time = 0  # Son olayın zamanı

    # İlk olay
    initial_arrival_time = generate_arrival_time(0)
    heapq.heappush(FEL, Event(initial_arrival_time, 'arrival'))  # İlk varış olayını FEL'e ekler

    while denied_passengers < 100:
        event = heapq.heappop(FEL)  # FEL'den bir sonraki olayı alır
        current_time = event.time  # Geçerli zamanı günceller
        time_since_last_event = current_time - last_event_time  # Son olaydan bu yana geçen süreyi hesaplar
        last_event_time = current_time  # Son olay zamanını günceller

        # Kuyruğun önceki uzunluğunda geçen toplam süreyi günceller
        if queue_length_times:
            queue_length_times[-1][1] += time_since_last_event

        if event.type == 'arrival':
            passenger_id_counter += 1  # Yeni benzersiz ID almak için sayaç artırılır, yeni yolcu girişi kısmı da diyebiliriz
            passenger = Passenger(passenger_id_counter, current_time)  # Yeni yolcu oluşturulur
            print(f"t={current_time:.2f}: Passenger {passenger.id} arrived for inspection.")  # Varış bilgisi yazdırılır
            if len(queue) == 0:  # Eğer kuyruk boşsa, inceleme hemen başlar
                inspection_time = current_time + generate_inspection_time()
                heapq.heappush(FEL, Event(inspection_time, 'inspection', passenger))
                print("  Inspection starts")  # İnceleme başlangıcı yazdırılır
            queue.append(passenger)  # Yolcu kuyruğa eklenir
            print(f"  Queue length={len(queue)-1}")  # Güncel kuyruk uzunluğu yazdırılır
            next_arrival_time = generate_arrival_time(current_time)  # Bir sonraki varış zamanı üretilir
            heapq.heappush(FEL, Event(next_arrival_time, 'arrival'))  # Bir sonraki varış olayı FEL'e eklenir
            print(f"  New arrival generated and scheduled for t={next_arrival_time:.2f}")  # Bir sonraki varış bilgisi yazdırılır

        elif event.type == 'inspection':
            inspected_passenger = event.passenger  # İncelenen yolcu
            if random.random() < 0.05:  # %5 ihtimalle inceleme başarısız olur
                inspected_passenger.denied = True
                denied_passengers += 1  # Reddedilen yolcu sayısı artırılır
                print(f"  t={current_time:.2f}: Passenger {inspected_passenger.id} inspection failed (failed no. {denied_passengers})")  # Reddedilme bilgisi yazdırılır
            else:
                print(f"  t={current_time:.2f}: Passenger {inspected_passenger.id} passed inspection")  # İncelemeden geçme bilgisi yazdırılır
            queue.pop(0)  # Yolcu kuyruktan çıkarılır
            if queue:  # Eğer kuyrukta başka yolcu varsa, bir sonraki inceleme için olay planlanır
                next_inspection_time = current_time + generate_inspection_time()
                heapq.heappush(FEL, Event(next_inspection_time, 'inspection', queue[0]))
                print("  Next inspection scheduled")  # Bir sonraki inceleme planı yazdırılır

        max_queue_length = max(max_queue_length, len(queue))  # Maksimum kuyruk uzunluğu güncellenir
        queue_length_times.append([len(queue), 0])  # Yeni kuyruk uzunluğu kaydedilir ve zamanlayıcı sıfırlanır

    total_time = last_event_time  # Toplam simülasyon süresi
    total_time_weighted_queue_lengths = sum(length * time for length, time in queue_length_times)  # Zaman ağırlıklı kuyruk uzunlukları toplamı
    average_queue_length = total_time_weighted_queue_lengths / total_time  # Ortalama kuyruk uzunluğu hesaplanır

    # Final raporu
    print("\nFinal Raporu:")
    print(f"Toplam simülasyon süresi: {total_time:.2f} dakika")
    print(f"Simülasyon sonunda FEL uzunluğu: {len(FEL)}")
    print("Simülasyon sonunda FEL içeriği:")
    for event in FEL:
        print(f"  Olay Türü: {event.type}, Planlanan Zaman: {event.time:.2f}")  # FEL'deki olayların detayları yazdırılır
    print(f"Ortalama kuyruk uzunluğu: {average_queue_length:.2f}")  # Ortalama kuyruk uzunluğu yazdırılır
    print(f"Maksimum kuyruk uzunluğu: {max_queue_length}")  # Maksimum kuyruk uzunluğu yazdırılır

simulation()  # Simülasyon başlatılır
