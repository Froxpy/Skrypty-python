#!/bin/bash

folder="./"
skrypt="$(basename "$0")"

# Funkcja zamienia numer miesiąca na nazwę słowną po polsku
miesiac_slownie() {
  case "$1" in
    01) echo "styczeń" ;;
    02) echo "luty" ;;
    03) echo "marzec" ;;
    04) echo "kwiecień" ;;
    05) echo "maj" ;;
    06) echo "czerwiec" ;;
    07) echo "lipiec" ;;
    08) echo "sierpień" ;;
    09) echo "wrzesień" ;;
    10) echo "październik" ;;
    11) echo "listopad" ;;
    12) echo "grudzień" ;;
    *) echo "nieznany" ;;
  esac
}

# Funkcja przenosząca pliki wg roku i miesiąca słownie
przenies_plik() {
  local plik="$1"

  [ -f "$plik" ] || return
  [ "$(basename "$plik")" = "$skrypt" ] && return

  data=$(stat -f "%SB" -t "%Y-%m-%d" "$plik")
  rok=$(echo "$data" | cut -d'-' -f1)
  miesiac_num=$(echo "$data" | cut -d'-' -f2)
  miesiac=$(miesiac_slownie "$miesiac_num")

  folder_rok="$folder/$rok"
  folder_miesiac="$folder_rok/$miesiac"

  [ -d "$folder_rok" ] || mkdir "$folder_rok"
  [ -d "$folder_miesiac" ] || mkdir "$folder_miesiac"

  mv "$plik" "$folder_miesiac/"
  echo "Przeniesiono $plik → $folder_miesiac/"
}

# 1. Przetwarzamy pliki w głównym folderze
for plik in "$folder"*; do
  przenies_plik "$plik"
done

# 2. Szukamy folderów z nazwą roku (czterocyfrowe liczby)
for rok_folder in "$folder"[0-9][0-9][0-9][0-9]; do
  if [ -d "$rok_folder" ]; then
    # Przetwarzamy pliki znajdujące się bezpośrednio w folderze z rokiem
    for plik in "$rok_folder"/*; do
      przenies_plik "$plik"
    done
  fi
done

echo "Wszystkie pliki uporządkowane wg roku i miesiąca słownie."
