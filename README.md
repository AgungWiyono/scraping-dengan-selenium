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

1. Aktifkan virtual environment
2. Masuk ke folder project
3. Jalankan `python scraper.py`
4. Akan muncul dialog untuk 
	1. Keyword pencarian
	2. Halaman mulai pencarian (isikan 0 untuk halaman paling awal)
	3. Halaman akhir yang ingin discrape (isikan 0 untuk tanpa batas)
5. Browser akan terbuka, lakukan login dan kembali ke konsol
6. Isikan n bila login gagal, y bila login berhasil
7. Bila diisi selain y, maka program akan berhenti

Bila diisi y maka program akan berjalan melakukan scraping mulai dari halaman
yang awal sampai batas yang ditentukan. Atau bila ada kegagalan, maka script
akan menyimpan result dari halaman-halaman yang telah berhasil di-scrape
dan menampilkan log tentang halaman yang gagal di scrape.
