# VisualBTC - Visual Bitcoin Private Key Generator

![Bitcoin](https://img.shields.io/badge/Bitcoin-000?style=for-the-badge&logo=bitcoin&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

Una aplicación web interactiva para generar claves privadas de Bitcoin de forma visual usando una grilla de 16x16 bits.

## 🚀 Características

- **Interfaz Visual Intuitiva**: Crea claves privadas usando una grilla interactiva de 256 bits
- **Generación de QR Codes**: Códigos QR automáticos para claves privadas y direcciones
- **Soporte para Claves Comprimidas/No Comprimidas**: Toggle entre formatos de clave
- **Herramientas de Manipulación**: Botones para aleatorizar, limpiar, invertir y rotar la grilla
- **Descarga de QR Codes**: Descarga los códigos QR generados
- **Estadísticas en Tiempo Real**: Visualiza la entropía y estadísticas de tu clave

## 📋 Requisitos

- Python 3.8+
- Ver `requirements.txt` para dependencias específicas

## 🔧 Instalación Local

1. **Clona el repositorio:**
```bash
git clone https://github.com/tu-usuario/visualbtc.git
cd visualbtc
```

2. **Crea y activa un entorno virtual:**
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

3. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecuta la aplicación:**
```bash
streamlit run app.py
```

5. **Abre tu navegador en:** `http://localhost:8501`

## 🌐 Despliegue

### Streamlit Cloud

1. Sube tu código a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repositorio de GitHub
4. Configura la aplicación principal como `app.py`
5. ¡Despliega!

### Heroku

1. **Instala Heroku CLI**
2. **Crea archivos de configuración** (incluidos en este repo):
   - `Procfile`
   - `setup.sh`
   - `requirements.txt`

3. **Despliega:**
```bash
heroku login
heroku create tu-app-name
git push heroku main
```

### Railway

1. Conecta tu repositorio en [railway.app](https://railway.app)
2. La aplicación se desplegará automáticamente

## 📁 Estructura del Proyecto

```
visualbtc/
├── app.py                 # Aplicación principal de Streamlit
├── requirements.txt       # Dependencias de Python
├── README.md             # Este archivo
├── Procfile              # Configuración para Heroku
├── setup.sh              # Script de configuración para Heroku
├── .gitignore            # Archivos a ignorar en Git
└── runtime.txt           # Versión de Python para Heroku
```

## 🔒 Información de Seguridad

**⚠️ ADVERTENCIA IMPORTANTE:**

Esta aplicación es para **propósitos educativos y de demostración**. Para uso real con Bitcoin:

- ✅ Asegúrate de tener suficiente entropía (aleatoriedad)
- ✅ Usa un entorno offline y seguro
- ✅ Nunca compartas tu clave privada
- ✅ Haz copias de seguridad seguras en papel
- ✅ Considera usar carteras probadas para la generación de claves en producción

## 🛠️ Funcionalidades

### Controles de la Grilla
- **🎲 Random**: Genera un patrón aleatorio
- **❌ Clear**: Limpia toda la grilla
- **🔄 Inverse**: Invierte todos los bits
- **↩️ Rotate**: Rota la grilla 90 grados
- **🪙 Flip Coin**: Llena una celda vacía aleatoriamente

### Formatos de Clave
- **Claves Comprimidas**: Más eficientes, recomendadas (WIF empieza con 'K' o 'L')
- **Claves No Comprimidas**: Formato legacy (WIF empieza con '5')

### Salidas Generadas
- Clave privada en formato hexadecimal
- Clave privada en formato WIF (Wallet Import Format)
- Clave pública (comprimida o no comprimida)
- Dirección Bitcoin (Legacy P2PKH)
- Códigos QR para clave privada y dirección

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🎯 Inspiración

Este proyecto está inspirado en el trabajo original de [MrFreeDragon/VisualBTC](https://github.com/MrFreeDragon/VisualBTC). Agradecimientos especiales por la inspiración y el concepto innovador de generación visual de claves Bitcoin.

## 🙏 Agradecimientos

- [MrFreeDragon](https://github.com/MrFreeDragon/VisualBTC) por el concepto original e inspiración
- [Streamlit](https://streamlit.io/) por el framework web
- [ECDSA](https://github.com/starkbank/ecdsa-python) por la criptografía de curva elíptica
- [qrcode](https://github.com/lincolnloop/python-qrcode) por la generación de códigos QR
- La comunidad Bitcoin por la documentación y estándares

---

**⚡ ¡Genera tus claves Bitcoin de forma visual y segura!**