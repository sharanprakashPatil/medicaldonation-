import subprocess, sys, os
os.chdir(r'C:\Users\SURAJ MALIPATIL\Downloads\medicaldonation--main\medicaldonation--main')
proc = subprocess.Popen([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        creationflags=subprocess.CREATE_NO_WINDOW)
with open('server_pid.txt', 'w') as f:
    f.write(str(proc.pid))
for line in iter(proc.stdout.readline, b''):
    print(line.decode().rstrip())
