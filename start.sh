sudo pigpiod
# Obtener la ruta completa del archivo actual
SCRIPT_PATH=$(realpath "$0")

# Obtener el directorio del archivo actual
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")

# Mostrar la ruta completa y el directorio
#echo "Ruta completa del archivo: $SCRIPT_PATH"
#echo "Directorio del archivo: $SCRIPT_DIR"

cd 
cd $SCRIPT_DIR

sudo python3 app.py -v