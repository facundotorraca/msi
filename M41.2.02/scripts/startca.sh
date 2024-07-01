export PYTHONDONTWRITEBYTECODE=1 # do not generite pycache

env="$1"

case "$env" in
    dev)
        fastapi dev main.py 
        ;;
    prod)
        fastapi run main.py
        ;;
esac