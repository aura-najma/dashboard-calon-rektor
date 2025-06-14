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
    kategori_penelitian = df_penelitian['kategori'].dropna().unique().tolist()
    tahun_penelitian = df_penelitian['tahun'].dropna().unique().tolist()

    data_sks = df_sks.to_dict(orient='records')
    data_gabungan = df_gabungan.to_dict(orient='records')
    data_penelitian = df_penelitian.to_dict(orient='records')
    # Extract and count the occurrences of each "jabatan fungsional" from your data
    jabfung_counts = df_jabatan['jabatan fungsional'].value_counts()

    # Prepare labels and values for the pie chart
    jabfung_labels = jabfung_counts.index.tolist()  # List of unique job titles
    jabfung_values = jabfung_counts.values.tolist()  # Corresponding count for each job title    bidang_counts = df_jabatan['bidang'].value_counts()
    bidang_counts = df_jabatan['bidang'].value_counts()

    # Persiapkan data untuk ditampilkan di chart
    bidang_labels = bidang_counts.index.tolist()
    bidang_values = bidang_counts.values.tolist()

    df_aras_sorted = df_aras[['Nama', 'aras score', 'rank']].dropna().sort_values(by='rank', ascending=True)

    tabel_aras = df_aras_sorted.to_dict(orient='records')
    data_aras = df_aras.drop(columns=['aras score', 'rank']).dropna().to_dict(orient='records')
    unique_candidates_count = df_aras['Nama'].nunique()
    df_s3 = df_pendidikan[df_pendidikan['jenjang'] == 'S3']
    
    # Count the occurrences of each university for S3
    university_counts = df_s3['perguruan tinggi'].value_counts()
    university_names = university_counts.index.tolist()
    university_values = university_counts.values.tolist()

    sks_data = df_gabungan.groupby(['jabatan fungsional', 'tahun'])['jumlah sks mengajar'].sum().reset_index()

    # Extract unique jabatan (job titles) and years before converting the DataFrame to a list
    jabatan_labels = sks_data['jabatan fungsional'].unique().tolist()
    years = sks_data['tahun'].unique().tolist()

    # Convert the grouped DataFrame to a list of dictionaries
    sks_data = sks_data.to_dict(orient='records')

    print(sks_data)
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
                           unique_researchers=unique_researchers,
                           bidang_counts=bidang_counts,
                           bidang_labels=bidang_labels,
                           bidang_values=bidang_values,
                           tabel_aras=tabel_aras,
                           data_aras=data_aras,
                           university_names=university_names,
                           university_values=university_values,
                           jabfung_labels=jabfung_labels,
                           jabfung_values=jabfung_values,
                           jabatan_labels=jabatan_labels,
                           sks_data=sks_data,
                           years=years,
                           kategori_penelitian=kategori_penelitian,
                           tahun_penelitian=tahun_penelitian)

# Route untuk halaman MCDM Analysis
@app.route('/transparansi_data')
def transparansi_data():
    # Convert df_penelitian to list of records (this is correct)
    data_penelitian = df_penelitian.to_dict(orient='records')

    # Filter and rename columns in df_s3
    df_s3 = df_pendidikan[df_pendidikan['jenjang'] == 'S3']
    df_s3 = df_s3.rename(columns={
        'perguruan tinggi': 'perguruan_tinggi',
        'gelar akademik': 'gelar_akademik'
    })
    # Convert df_s3 to a list of records after renaming columns
    df_s3 = df_s3.to_dict(orient='records')


    # Return the rendered template with the data passed in
    return render_template('transparansi_data.html',  
                           data_penelitian=data_penelitian,
                           df_s3=df_s3)


# Menjalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
