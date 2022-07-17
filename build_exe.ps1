#$versionPy = Get-Content terminal/version.py
#$versionPy -match "'(?<year>\d{4})\.(?<major>\d+).(?<minor>\d+)'"
#$versionYear = [int]$Matches.year
#$versionMajor = [int]$Matches.major
#$versionMinor = [int]$Matches.minor
#$versionMinor++
#$version = "{0}.{1}.{2}" -f $versionYear $versionMajor $versionMinor
#
#Set-Content app/version.py -Value("version = '{0}'" -f $version)
#$name = "teminal-app-"+$version
$name = "teminal-app-v1"

$dir = "dist\"+$name

pyinstaller --noconfirm --onefile -n main terminal\main.py --paths "." --distpath $dir
New-Item -ItemType directory -Force -Path $dir
Compress-Archive -Path $dir\* -DestinationPath $dir\$name".zip"
