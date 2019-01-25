cd src
while true; do
  python3 main.py
  # Give three seconds for operator to stop loop code.
  echo "Dicebag stopped with exit code $?. Respawning in 3..."
  sleep 1
  echo "2..."
  sleep 1
  echo "1..."
  sleep 1
done

