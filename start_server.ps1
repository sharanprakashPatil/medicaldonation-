$server = Start-Process -NoNewWindow -FilePath "python" -ArgumentList "manage.py runserver 0.0.0.0:8000" -WorkingDirectory "C:\Users\SURAJ MALIPATIL\Downloads\medicaldonation--main\medicaldonation--main" -PassThru
$server.Id | Out-File -FilePath "C:\Users\SURAJ MALIPATIL\Downloads\medicaldonation--main\medicaldonation--main\server_pid.txt"
