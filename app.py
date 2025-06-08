import pandas as pd
import os
from flask import Flask, render_template

# Membuat aplikasi Flask
app = Flask(__name__)

# Path ke file Excel di dalam folder data
file_path = os.path.join(os.getcwd(), "data", "Data 11 Kandidat Rektor UNAIR 2025.xlsx")

# Membaca data dari setiap sheet
df_penelitian = pd.read_excel(file_path, sheet_name="penelitian")
df_pendidikan = pd.read_excel(file_path, sheet_name="pendidikan")
df_sks = pd.read_excel(file_path, sheet_name="sks mengajar")
df_berita = pd.read_excel(file_path, sheet_name="berita")
df_jabatan = pd.read_excel(file_path, sheet_name="jabatan fungsional")
df_aras = pd.read_excel(file_path, sheet_name="hasil aras")
df_gabungan = pd.read_excel(file_path, sheet_name="gabungan")
# Route untuk halaman utama
@app.route('/')
def index():
    # Hitung jumlah calon rektor unik
    unique_candidates_count = df_aras['Nama'].nunique()

    # Temukan calon rektor dengan rank 1
    rank_1_candidate = df_aras[df_aras['rank'] == 1]['Nama'].iloc[0]

    df_s3 = df_pendidikan[df_pendidikan['jenjang'] == 'S3']
    
    # Count the occurrences of each university for S3
    university_counts = df_s3['perguruan tinggi'].value_counts()
    print("University Counts:\n", university_counts)
    # Convert this data to a dictionary format for passing to the template
    university_names = university_counts.index.tolist()
    university_values = university_counts.values.tolist()
    print("University Names:", university_names)
    print("University Values:", university_values)
    # Menampilkan halaman utama dengan template index.html
    return render_template('index.html', unique_candidates_count=unique_candidates_count, 
                           rank_1_candidate=rank_1_candidate, 
                           university_names=university_names, 
                           university_values=university_values)

@app.route('/dashboard')
def dashboard():
    unique_candidates_count = df_aras['Nama'].nunique()

    # Temukan calon rektor dengan rank 1
    rank_1_candidate = df_aras[df_aras['rank'] == 1]['Nama'].iloc[0]

    # Filter data untuk jenjang S3 dan urutkan berdasarkan tahun
    df_s3 = df_pendidikan[df_pendidikan['jenjang'] == 'S3']
    df_s3_sorted = df_s3.sort_values(by='tahun', ascending=True)  # Ascending to get the first S3 year
    
    # First rector with S3 (oldest year)
    first_rector_s3 = df_s3_sorted.iloc[0]['nama']

    # Last rector with S3 (most recent year)
    last_rector_s3 = df_s3_sorted.iloc[-1]['nama']

        # Extract the titles (judul) for WordCloud generation
    penelitian_data = df_penelitian[['nama', 'judul']].dropna().to_dict(orient='records')
    penelitian_kategori = df_penelitian[['nama', 'kategori']].dropna().to_dict(orient='records')
    unique_researchers = df_penelitian['nama'].dropna().unique().tolist()
    data_sks = df_sks.to_dict(orient='records')
    data_gabungan = df_gabungan.to_dict(orient='records')
    data_penelitian = df_penelitian.to_dict(orient='records')
    # Menampilkan halaman utama dengan template index.html
    return render_template('dashboard.html',
                           unique_candidates_count=unique_candidates_count, 
                           rank_1_candidate=rank_1_candidate,
                           first_rector_s3=first_rector_s3,
                           last_rector_s3=last_rector_s3,
                           penelitian_data=penelitian_data,
                           penelitian_kategori=penelitian_kategori,
                           data_sks=data_sks,
                           data_penelitian=data_penelitian,
                           data_gabungan=data_gabungan,
                           unique_researchers=unique_researchers)

# Route untuk halaman MCDM Analysis
@app.route('/mcdm_analysis')
def mcdm_analysis():
    df_aras_sorted = df_aras[['Nama', 'aras score', 'rank']].dropna().sort_values(by='rank', ascending=True)

    tabel_aras = df_aras_sorted.to_dict(orient='records')
    data_aras = df_aras.drop(columns=['aras score', 'rank']).dropna().to_dict(orient='records')
    unique_candidates_count = df_aras['Nama'].nunique()
    unique_researchers = df_aras['Nama'].dropna().unique().tolist()

    # Temukan calon rektor dengan rank 1
    rank_1_candidate = df_aras[df_aras['rank'] == 1]['Nama'].iloc[0]
    # Menampilkan halaman mcdm_analysis.html
    return render_template('mcdm_analysis.html', tabel_aras=tabel_aras, 
                           data_aras=data_aras, unique_candidates_count=unique_candidates_count,
                           rank_1_candidate=rank_1_candidate, unique_researchers=unique_researchers)


# Menjalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
