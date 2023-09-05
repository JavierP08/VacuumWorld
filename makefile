# Makefile para instalar las librerías de Pygame en Python

# Comandos
PIP := pip
PYTHON := python

# Objetivo predeterminado: instalar las librerías
install: install-requirements

# Instalar las dependencias usando pip
install-requirements:
	@$(PIP) install -r requirements.txt
	@echo "Librerías instaladas correctamente."

# Limpiar los archivos generados
clean:
	@rm -rf __pycache__
	@echo "Archivos generados eliminados."

.PHONY: install install-requirements clean
