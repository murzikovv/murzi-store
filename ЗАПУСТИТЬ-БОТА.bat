@echo off
chcp 65001 >nul
title murzi/store BOT — НЕ ЗАКРЫВАТЬ ЭТО ОКНО
echo.
echo  ════════════════════════════════════════════
echo   Бот-касса @murzistudio_bot запускается...
echo   ПОКА ОКНО ОТКРЫТО — МАГАЗИН ПРОДАЁТ.
echo   Закроешь окно — продажи остановятся.
echo  ════════════════════════════════════════════
echo.
cd /d "%~dp0bot"
:loop
python bot.py
echo.
echo  Бот упал или остановлен. Перезапуск через 5 сек... (Ctrl+C — выйти)
timeout /t 5 >nul
goto loop
