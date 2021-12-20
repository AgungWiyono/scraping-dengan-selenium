# OLX Phone Scraper

## Instalasi

Software yang dibutuhkan antara lain:

1. python3.8
2. pip (python package manager)
3. python virtualenv
4. firefox browser
5. geckodriver (webdriver untuk firefox)

## Virtual Environment

1. Masuk ke folder project atau folder yang sejajar dengan folder project
2. Buat virtual environment dengan menjalankan `python3 -m venv env`
3. Aktifkan virtual environment dengan menjalankan `source /path_to_env_folder/bin/activate`
4. Untuk menonaktifkan jalankan `deactivate` dari manapun

## Instalasi requirements

1. Aktifkan virtual environment
2. Masuk ke folder project
3. Jalankan `pip install -r requirements.txt`


## Cara Menjalankan

Ada 2 step berbeda, step pertama adalah untuk mendapatkan id user sedangkan 
step kedua adalah untuk mendapatkan data user itu sendiri. Result dari step pertama 
adalah file-file json yang berisi user id. Sedangkan isi step kedua adalah 
file json berisi data-data user.

Menjalankan step 1:

1. Aktifkan virtual environment
2. Masuk ke folder project
3. Jalankan `python id_getter.py 'kata kunci'`
4. Program akan berjalan sembari menuliskan user_id di setiap 5 halaman pada folder user_ids.
5. Fitur untuk membatasi halaman mulai dan halaman akhir yang ingin discrape akan ditambahkan.

Menjalankan step 2:

1. Aktifkan virtual environment
2. Masuk ke folder project
3. Jalankan `python data_getter.py file_berisi_user_id.json`
4. Akan muncul kotak dialog yang menanyakan apakah login berhasil dan juga muncul firefox browser yang mengunjungi alamat olx.co.id
5. Login pada halaman olx dengan metode email dan password, jika berhasil jawab **y** pada dialog di konsol, selain itu **n**
6. Hasilnya akan muncul sebagai file json dengan nama file berformat result_datetime.json
7. Akan dilakukan perbaikan untuk penamaan file dan jenis file untuk ekspor hasil
