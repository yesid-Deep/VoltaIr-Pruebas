#!/bin/bash
# Script to enable and configure I2C on Raspberry Pi 5
# Usage: bash setup_i2c.sh

echo "=== Setting up I2C on Raspberry Pi 5 ==="

# 1. Update repositories
sudo apt update && sudo apt upgrade -y

# 2. Install required tools
echo "[+] Installing dependencies..."
sudo apt install -y i2c-tools python3-smbus python3-pip

# 3. Enable I2C in config.txt if not already enabled
CONFIG_FILE="/boot/firmware/config.txt"
if ! grep -q "dtparam=i2c_arm=on" "$CONFIG_FILE"; then
    echo "[+] Enabling I2C in $CONFIG_FILE"
    echo "dtparam=i2c_arm=on" | sudo tee -a $CONFIG_FILE
else
    echo "[=] I2C is already enabled in $CONFIG_FILE"
fi

# 4. Add current user to the i2c group
sudo usermod -aG i2c $USER

# 5. Final instructions
echo "[+] Reboot your Raspberry Pi to apply changes."
echo "[+] After reboot, run: i2cdetect -y 1"
echo "    The SHT30 should appear at address 0x44 or 0x45."
echo "    Run i2cdetect -y 1 for See I2C Directions"

