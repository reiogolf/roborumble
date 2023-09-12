.DEFAULT_GOAL := help
SHELL := bash
.ONESHELL:

install:        ## Install dependencies and apt packages
	@echo "installing apt packages..."
	@sudo apt-get install -y git python3-pip python3-rpi.gpio zbar-tools 
	@sudo apt-get install -y python3-picamera2 --no-install-recommends
	@echo "installing dependencies..."
	@pip install --upgrade pip setuptools wheel
	@pip install --upgrade pip
	@pip install -r requirements.txt --extra-index-url https://www.piwheels.org/simple
	@echo "python dependencies installed successfully."
