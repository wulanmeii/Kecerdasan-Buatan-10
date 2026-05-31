import random

# ─── Data Domain ───────────────────────────────────────────────
teachers  = ['Guru A', 'Guru B', 'Guru C']
subjects  = ['Matematika', 'Fisika', 'Kimia']
classes   = ['Kelas 1', 'Kelas 2', 'Kelas 3']
timeslots = ['Senin P1', 'Senin P2', 'Selasa P1', 'Selasa P2']

# ─── Representasi Kromosom ──────────────────────────────────────
# Kromosom: [guru, mata_pelajaran, kelas, slot_waktu]
def create_individual():
    return [
        random.choice(teachers),
        random.choice(subjects),
        random.choice(classes),
        random.choice(timeslots)
    ]

# ─── Fungsi Fitness ─────────────────────────────────────────────
# Menghitung jumlah konflik jadwal (semakin kecil semakin baik)
def fitness(individual, schedule):
    conflicts = 0
    for item in schedule:
        # Konflik: kelas yang sama di waktu yang sama
        if individual[2] == item[2] and individual[3] == item[3]:
            conflicts += 1
        # Konflik: guru yang sama di waktu yang sama
        if individual[0] == item[0] and individual[3] == item[3]:
            conflicts += 1
    return conflicts

# ─── Seleksi ────────────────────────────────────────────────────
# Memilih dua individu terbaik berdasarkan nilai fitness
def selection(population, schedule):
    sorted_pop = sorted(population,
                        key=lambda ind: fitness(ind, schedule))
    return sorted_pop[0], sorted_pop[1]

# ─── Crossover (Single-Point) ────────────────────────────────────
def crossover(parent1, parent2):
    point = random.randint(1, 3)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# ─── Mutasi ─────────────────────────────────────────────────────
def mutate(individual):
    point = random.randint(0, 3)
    options = [teachers, subjects, classes, timeslots]
    individual[point] = random.choice(options[point])
    return individual

# ─── Algoritma Genetika Utama ────────────────────────────────────
def genetic_algorithm():
    POP_SIZE   = 10
    GENERATIONS = 50

    population = [create_individual() for _ in range(POP_SIZE)]
    schedule   = []   # jadwal final yang terbentuk

    for gen in range(GENERATIONS):
        new_population = []
        for _ in range(POP_SIZE // 2):
            p1, p2 = selection(population, schedule)
            c1, c2 = crossover(p1, p2)
            new_population.extend([mutate(c1), mutate(c2)])
        population = new_population

        # Pilih individu terbaik generasi ini
        best = min(population,
                   key=lambda ind: fitness(ind, schedule))
        schedule.append(best)
        print(f'Gen {gen+1:2d}: {best}'
              f' | Konflik: {fitness(best, schedule)}')

    print('\n=== JADWAL AKHIR ===')
    for idx, item in enumerate(schedule, 1):
        print(f'{idx}. {item[2]} - {item[1]}'
              f' oleh {item[0]} pada {item[3]}')

# ─── Jalankan ────────────────────────────────────────────────────
if __name__ == '__main__':
    genetic_algorithm()
