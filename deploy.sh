#!/bin/sh

echo "Starting to deploy"
./telegramBot/bot.py &
cd Categorizing
./main.py
