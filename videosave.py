# videosave.py (SUDAH DIPERBAIKI)

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from model import VirusSpread
from sneeze import VirusCloud
from agent import Person # <-- Tambahkan import Person untuk isinstance

SIMULATION_STEPS_PER_ANIMATION_FRAME = 1  # Ubah nilai ini sesuai kebutuhan (misal: 5 atau 10)
TOTAL_ANIMATION_FRAMES = 100

def render_model(model):
    """Merender kondisi model saat ini ke plot."""
    plt.clf()  # Hapus frame sebelumnya
    ax = plt.gca() # Dapatkan axis saat ini

    # Iterasi melalui semua agen untuk digambar
    for agent in model.agents:
        # Cek apakah ini VirusCloud
        if isinstance(agent, VirusCloud):
            x, y = agent.position
            # Gunakan intensitas sebagai alpha (transparansi) untuk efek visual
            # Pastikan intensitas tidak negatif untuk alpha
            alpha = max(0, agent.intensity) 
            circle = patches.Circle((x, y), radius=agent.cloud_radius, color='purple', alpha=alpha, fill=True)
            ax.add_patch(circle)
        
        # Cek apakah ini Person
        elif isinstance(agent, Person):
            # BENAR: Gunakan agent.position
            x, y = agent.position 
            
            # Tentukan warna berdasarkan status agen
            color = (
                "red" if agent.state == "Infected" else
                "green" if agent.state == "Recovered" else
                "blue"
            )
            if agent.is_masked:
                # 1. Gambar border terlebih dahulu (lingkaran besar & kosong)
                plt.plot(x, y, 
                         marker='s', 
                         color='black',            # Warna border
                         markersize=15,            # Ukuran lebih besar dari isi
                         fillstyle='none',         # PENTING: Membuatnya kosong/hollow
                         markeredgewidth=1)        # Ketebalan garis border itu sendiri

                # 2. Gambar isi di atasnya (lingkaran kecil & berwarna)
                plt.plot(x, y,
                         marker='o',
                         color=color,              # Warna sesuai status agen
                         markersize=6,             # Ukuran normal
                         linestyle='None')

            # Jika agen tidak memakai masker, gambar seperti biasa
            else:
                plt.plot(x, y,
                         marker='o',
                         color=color,
                         markersize=6,
                         linestyle='None')

    # Atur batas dan aspek plot
    plt.xlim(0, model.space.size[0])
    plt.ylim(0, model.space.size[1])
    ax.set_aspect('equal', adjustable='box')


# --- Bagian Simulasi dan Penyimpanan Video ---
    """Create a new Virus Spread model.

        Args:
            population_size: Number of Person in the simulation (default: 100)
            width: Width of the space (default: 100)
            height: Height of the space (default: 100)
            infection_radius: Radius within which an infected person can infect others (default: 2)
            infection_probability: Probability of infection when in range (default: 0.2)
            infection_duration: Duration of infection in steps (default: 30)
            initial_infected: Number of initially infected persons (default: 1)
            seed: Random seed for reproducibility (default: None)
            speed: Speed of movement for each agent (default: 1.0)
            cloud_decay_rate: Rate at which the sneeze cloud dissipates (default: 0.02)
            sneeze_probability: Probability of an infected person sneezing (default: 0.05)
            cloud_radius: Radius of the sneeze cloud (default: 2.0)
            cloud_init_intensity: Initial intensity of the sneeze cloud (default: 1.0)
    """

print("Membuat model...")
model = VirusSpread(
    population_size=100,
    initial_infected=10,
    sneeze_probability=0.03,
    infection_duration=100,
    speed=0.8,
    width=50,
    height=50,
    infection_probability=0.4,
    infection_radius=1.0,
    cloud_decay_rate=0.02,
    cloud_radius=2.0,
    cloud_init_intensity=0.8,
    mask_usage_percentage=0.5,  # 50% agen memakai masker
    mask_effectiveness=0.5,      # Masker mengurangi transmisi 80%
    seed=42,
)

# Siapkan figure untuk animasi
fig, (ax1, ax2) = plt.subplots(figsize=(18, 8), nrows=1, ncols=2)
print("Memulai proses animasi...")

def update(frame_number):
    """Fungsi yang dipanggil untuk setiap frame animasi."""
    for _ in range(SIMULATION_STEPS_PER_ANIMATION_FRAME):
        model.step()

    ax1.cla()
    ax2.cla()

    # --- Panel Kiri (ax1): Animasi Agen ---
    ax1.set_title(f"Simulasi Agen (Langkah: {model.steps})")

    render_model(model)
    print(f"Merender frame animasi {frame_number + 1}/{TOTAL_ANIMATION_FRAMES} (Total Model Steps: {model.steps})")

# Buat animasi
ani = animation.FuncAnimation(fig, update, frames=TOTAL_ANIMATION_FRAMES, repeat=False)

# Simpan animasi sebagai file MP4
print("Menyimpan video... Ini mungkin memakan waktu beberapa saat.")
ani.save("virus_spread_simulation1.mp4", fps=30, writer='ffmpeg')

print("Video berhasil disimpan sebagai 'virus_spread_simulation.mp4'")
plt.close(fig) # Tutup figure setelah selesai