import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from model import VirusSpread
from sneeze import VirusCloud
from agent import Person 

# --- KONFIGURASI SIMULASI & VIDEO ---
SIMULATION_STEPS_PER_ANIMATION_FRAME = 1
TOTAL_ANIMATION_FRAMES = 100

# --- PEMBUATAN MODEL ---
print("Membuat model...")
model = VirusSpread(
    population_size=100,
    initial_infected=1,
    infection_duration=504,
    infection_probability=0.06,
    mask_usage_percentage=0,
    masking_scenario=1,
    seed=42,
)

# --- SETUP FIGURE DENGAN DUA PANEL (SUBPLOTS) ---
# Mengubah layout menjadi 2 baris, 1 kolom. ax1 di atas, ax2 di bawah.
# figsize diubah agar lebih cocok untuk layout vertikal.
# gridspec_kw mengatur rasio tinggi antara panel atas dan bawah.
fig, (ax1, ax2) = plt.subplots(figsize=(8, 10), nrows=2, ncols=1, gridspec_kw={'height_ratios': [3, 1]})


# --- FUNGSI UTAMA UNTUK UPDATE ANIMASI (render_model diintegrasikan ke sini) ---

def update(frame_number):
    """Fungsi ini dipanggil untuk setiap frame, mengurus update dan penggambaran."""

    # 1. Jalankan langkah simulasi
    for _ in range(SIMULATION_STEPS_PER_ANIMATION_FRAME):
        if model.agents: # Hanya jalankan jika masih ada agen
            model.step()
        else:
            break # Hentikan jika tidak ada agen

    # 2. Hapus gambar frame sebelumnya dari kedua panel
    ax1.cla() # Hapus panel animasi agen
    ax2.cla() # Hapus panel grafik data

    # --- Panel Atas (ax1): Animasi Agen ---
    current_step = model.steps
    current_day = current_step // 72 + 1
    ax1.set_title(f"Simulasi Agen (Hari ke - {current_day})")
    
    # Iterasi melalui semua agen untuk digambar di ax1
    for agent in model.agents:
        if isinstance(agent, VirusCloud):
            x, y = agent.position
            alpha = max(0, agent.intensity) 
            circle = patches.Circle((x, y), radius=agent.cloud_radius, color='purple', alpha=alpha, fill=True)
            ax1.add_patch(circle)
        
        elif isinstance(agent, Person):
            x, y = agent.position 
            color = (
                "red" if agent.state == "Infected" else
                "green" if agent.state == "Recovered" else
                "blue"
            )
            if agent.is_masked:
                # Gambar border (kotak)
                ax1.plot(x, y, 
                         marker='s', # Anda menggunakan 's' (square) untuk border
                         color='black',
                         markersize=10, # Ukuran border (sesuaikan dengan markersize isi)
                         fillstyle='none',
                         markeredgewidth=1)
                # Gambar isi (lingkaran)
                ax1.plot(x, y,
                         marker='o',
                         color=color,
                         markersize=6,
                         linestyle='None')
            else:
                # Agen tidak bermasker
                ax1.plot(x, y,
                         marker='o',
                         color=color,
                         markersize=6,
                         linestyle='None')

    # Atur batas dan aspek untuk panel animasi (ax1)
    # KOREKSI: Gunakan model.width dan model.height yang disimpan di model
    ax1.set_xlim(0, model.width)
    ax1.set_ylim(0, model.height)

    # --- Panel Bawah (ax2): Grafik Data dari DataCollector ---
    ax2.set_title("Kurva S-I-R")

    # Ambil data yang sudah terkumpul dari model
    model_data = model.datacollector.get_model_vars_dataframe()

        # Plot data tersebut jika tidak kosong
    if not model_data.empty:
        colors = {
                'Susceptible': 'blue',
                'Infected': 'red',
                'Recovered': 'green'
            }
        model_data.plot(ax=ax2, 
                            kind='area', 
                            stacked=False, # PENTING: Area tidak ditumpuk
                            alpha=0.3,     # Transparansi agar tumpang tindih terlihat
                            color=[colors.get(col, '#333333') for col in model_data.columns],
                            legend=False)  # Matikan legend di sini, akan dibuat oleh plot garis

            # 2. Gambar garis di atas area agar lebih jelas
        model_data.plot(ax=ax2, 
                            kind='line', 
                            color=[colors.get(col, '#333333') for col in model_data.columns],
                            legend=True)   # Tampilkan legend di sini

        ax2.set_xlabel("Langkah (Step)")
        ax2.set_ylabel("Jumlah Agen")
        ax2.grid(True)
        ax2.set_ylim(0, model.population_size)


    # Menampilkan informasi di terminal
    print(f"Merender frame animasi {frame_number + 1}/{TOTAL_ANIMATION_FRAMES} (Total Model Steps: {model.steps})")
    
    # Menyesuaikan layout agar tidak tumpang tindih
    plt.tight_layout()


# --- PEMBUATAN DAN PENYIMPANAN ANIMASI ---
print("Memulai proses animasi...")
ani = animation.FuncAnimation(fig, update, frames=TOTAL_ANIMATION_FRAMES, repeat=False)

# Simpan animasi sebagai file MP4
print("Menyimpan video dashboard... Ini mungkin akan memakan waktu.")
try:
    # Ganti nama file agar tidak menimpa yang lama jika perlu
    ani.save("virus_spread_dashboard_vertical.mp4", fps=20, writer='ffmpeg', dpi=100) 
    print("Video berhasil disimpan sebagai 'virus_spread_dashboard_vertical.mp4'")
except Exception as e:
    print(f"Gagal menyimpan video: {e}")

plt.close(fig)