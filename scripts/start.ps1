cd ../

git pull origin master

.\virtualenv\Scripts\Activate.ps1
pip install -r dev.requirements.txt
pip install -r requirements.txt

cd app

$secretKey = "secretkey.txt"

if (!(Test-Path $secretKey)) {
    -join ((33..126) | Get-Random -Count 32 | % {[char]$_}) | Out-File $secretKey
}

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py createmissingsuperuser

$cpuCount = (Get-CimInstance Win32_ComputerSystem).NumberOfLogicalProcessors * 2

while ($true) {
    python manage.py start 0.0.0.0 80 $cpuCount
    Start-Sleep -Seconds 1
}

