#!/bin/bash

echo "Choose a clustering algorithm:"
echo "c - k-means with centroids"
echo "m - k-means with medoids"
echo "d - divisive clustering"

read -p "Enter 'c', 'm', or 'd': " choice

# Проверка корректности ввода
while [[ "$choice" != "c" && "$choice" != "m" && "$choice" != "d" ]]; do
    echo "Invalid input. Please enter 'c', 'm', or 'd'."
    read -p "Try again: " choice
done

pypy main.py "$choice"

python3 draw.py