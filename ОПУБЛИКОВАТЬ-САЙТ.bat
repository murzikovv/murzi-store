@echo off
chcp 65001 >nul
title murzi/store — публикация сайта
echo.
echo  ╔══════════════════════════════════════════╗
echo  ║   ПУБЛИКАЦИЯ САЙТА murzi/store           ║
echo  ╚══════════════════════════════════════════╝
echo.
cd /d "%~dp0"

echo  [1/3] Забираю свежее из сети...
git pull --rebase origin main

echo  [2/3] Добавляю все изменения...
git add -A
git add -f marketing/pins/*.png 2>nul

for /f "tokens=1-3 delims=. " %%a in ("%date%") do set D=%%a.%%b.%%c
git commit -m "Публикация %D% %time:~0,5%" 2>nul
if errorlevel 1 echo        (изменений нет — публикую как есть)

echo  [3/3] Отправляю на сервер...
git push origin main
if errorlevel 1 (
  echo.
  echo  !!! ОШИБКА ОТПРАВКИ. Проверь интернет и попробуй ещё раз.
  pause & exit /b 1
)

echo.
echo  ✓ ГОТОВО! Сайт обновится через 1-2 минуты:
echo    https://murzikovv.github.io/murzi-store/
echo    https://murzikovv.github.io/murzi-store/v2/
echo.
start https://murzikovv.github.io/murzi-store/v2/
pause
