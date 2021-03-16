from ftplib import FTP

ftp = FTP("192.168.0.4")
ftp.login("ftpuser", "password")
print(ftp.retrlines('LIST'))
files = []
ftp.dir(files.append)
for f in files:
    print(f)

ftp.cwd("dir")
with open('local_test.txt', 'w') as local_file:
    response = ftp.retrlines('RETR test', local_file.write)
    if response.startswith('226'):
        print('Transfer complete')

with open("schedules.todo.template", "w") as file:
    file.write("TESTDATA")
    file.close()
with open("schedules.todo.template", "rb") as file:
    ftp.storlines("STOR schedules.todo.template", file)
    file.close()

