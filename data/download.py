import sys, os
from pathlib import Path
import requests
from datetime import datetime, timedelta
import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

def check_file_status(filepath, filesize):
    sys.stdout.write('\r')
    sys.stdout.flush()
    size = int(os.stat(filepath).st_size)
    percent_complete = (size/filesize)*100
    sys.stdout.write('%.3f %s' % (percent_complete, '% Completed'))
    sys.stdout.flush()

# email = input('Email: ')
# # Try to get password
# try:
#     import getpass
#     input = getpass.getpass
# except:
#     try:
#         input = raw_input
#     except:
#         pass

# pswd = input('Password: ')

url = 'https://rda.ucar.edu/cgi-bin/login'
values = {'email' : 'omejiaa@uninorte.edu.co' , 'passwd' : 'Omar_080500', 'action' : 'login'}
# Authenticate
ret = requests.post(url,data=values)
if ret.status_code != 200:
    print('Bad Authentication')
    print(ret.text)
    exit(1)
dspath = 'https://rda.ucar.edu/data/ds083.2/'

start = sys.argv[1].split('-')
end = sys.argv[2].split('-')

Path('grib-data').mkdir(parents=True, exist_ok=True)
os.chdir('./grib-data')

filelist = [f'grib2/{start[0]}/{start[0]}.{start[1]}/fnl_{start[0]}{start[1]}{start[2]}_{start[3]}_00.grib2',f'grib2/{end[0]}/{end[0]}.{end[1]}/fnl_{end[0]}{end[1]}{end[2]}_{end[3]}_00.grib2']

for file in filelist:
    filename=dspath+file
    file_base = os.path.basename(file)
    print('\nDownloading',file_base)
    try:
        req = requests.get(filename, cookies = ret.cookies, allow_redirects=True, stream=True)
        filesize = int(req.headers['Content-length'])
        with open(file_base, 'wb') as outfile:
            chunk_size=1048576
            for chunk in req.iter_content(chunk_size=chunk_size):
                outfile.write(chunk)
                if chunk_size < filesize:
                    check_file_status(file_base, filesize)
        check_file_status(file_base, filesize)
    except:
        print(f'{file_base} no se pudo descargar')

print("\nData saved in ./grib-data")
