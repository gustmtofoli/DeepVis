#!/bin/bash

if [ -z "$1" ]; then
    echo "You must specify the virtual environment name. For example: install.sh my-venv"
    exit 1
fi

ENV_NAME="$1"
ANACONDA_INSTALLER="Anaconda3-2024.10-1-Linux-x86_64.sh"
INSTALL_PATH="$HOME/anaconda3"

if ! command -v conda &> /dev/null; then
    echo "[INFO] Anaconda not found. Installing..."
    
    echo "[INFO] Downloading Anaconda"
    wget https://repo.anaconda.com/archive/$ANACONDA_INSTALLER -O /tmp/$ANACONDA_INSTALLER
    bash /tmp/$ANACONDA_INSTALLER -b -p $INSTALL_PATH
    export PATH="$INSTALL_PATH/bin:$PATH"
    echo 'export PATH="$HOME/anaconda3/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    echo "[✅] Anaconda installed"

    echo "[INFO] Creating virtual environment"
    conda create --name "$ENV_NAME" -y
    echo "[✅] Virtual Environment created"

    echo "[INFO] Activating new environment"
    conda activate "$ENV_NAME"
    echo "[✅] Virtual Environment activated"

else
    echo "[✅] Anaconda3 is already installed"
fi

echo "[INFO] Preparing to install the project dependencies"
echo -n "⏳"

for i in {1..3}; do
    echo -n "."
    sleep 1
done
echo "✅"

if ! command -v npm &> /dev/null; then
    echo "[INFO] npm not found. Instalando..."
    sudo apt update && sudo apt install -y nodejs npm
    echo "[✅] npm installed!"
else
    echo "✅ npm os already installed!"
fi

echo "[INFO] Installing esprima with npm"
npm install esprima
echo "✅"

echo "[INFO] Installing neworkx with conda"
conda install networkx
echo "✅"


echo "[INFO] Installing pip"
python -m ensurepip --default-pip
python -m pip install --upgrade pip
echo "✅ pip installed and upgraded"


echo "[INFO] Installing pyvis with pip"
pip install pyvis
echo "✅"

echo "[INFO] Installing fastapi"
conda install fastapi
echo "✅"

echo "[INFO] Installing uvicorn"
conda install uvicorn
echo "✅"

echo "[INFO] Installing javalang"
pip install javalang
echo "✅"
