# Dashboard en Tiempo Real

App web con Flask que muestra un dashboard con datos del clima de Ciudad de México y precios de criptomonedas (Bitcoin, Ethereum, Solana). Se actualiza automáticamente cada 60 segundos.

## APIs integradas

### Open-Meteo (Clima)
- **URL:** https://api.open-meteo.com/v1/forecast
- **Parámetros:** `latitude=19.43&longitude=-99.13&current=temperature_2m,wind_speed_10m`
- **Costo:** Gratis, sin API key
- **Datos:** Temperatura actual (°C) y velocidad del viento (km/h)

### CoinGecko (Criptomonedas)
- **URL:** https://api.coingecko.com/api/v3/simple/price
- **Parámetros:** `ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true`
- **Costo:** Gratis para uso básico, sin API key
- **Datos:** Precio en USD y variación porcentual en 24h

## Endpoints de la app

| Ruta | Descripción |
|------|-------------|
| `/` | Dashboard visual con HTML y CSS |
| `/api/weather` | JSON con temperatura y viento |
| `/api/crypto` | JSON con precios de BTC, ETH y SOL |

## Desplegar en Portainer

### Opción 1: Stack con repositorio Git (recomendado)

1. Abre Portainer y ve a **Stacks**
2. Haz clic en **Add stack**
3. Selecciona **Git repository**
4. Completa los campos:
   - **Name:** `dashboard`
   - **Repository URL:** `https://github.com/IsraelSaucedoDavid/portainer.git`
   - **Repository reference:** `refs/heads/main`
   - **Compose path:** `docker-compose.yml`
5. Activa **Automatic updates** si quieres que se redeploye automáticamente al hacer push
6. Haz clic en **Deploy the stack**

### Opción 2: Stack con Docker Compose manual

1. Ve a **Stacks** → **Add stack** → **Web editor**
2. Pega el contenido de `docker-compose.yml`:
```yaml
version: "3.8"

services:
  mi-app:
    build: .
    container_name: app-python
    ports:
      - "5000:5000"
    restart: unless-stopped
```
3. Haz clic en **Deploy the stack**

### Opción 3: Imagen preconstruida (sin build)

Si ya subiste la imagen a Docker Hub o un registry privado:

1. Ve a **Containers** → **Add container**
2. En **Image** escribe tu imagen, ej: `tuusuario/portainer-dashboard:latest`
3. En **Port mapping** agrega: `Host = 5000`, `Container = 5000`
4. En **Restart policy** selecciona `Unless stopped`
5. Haz clic en **Deploy the container**

## Acceder al dashboard

Una vez desplegado, abre tu navegador en:
```
http://<IP-de-tu-servidor>:5000
```

La página carga los datos vía JavaScript desde los endpoints `/api/weather` y `/api/crypto`, y se refresca automáticamente cada 60 segundos.

## Estructura del proyecto

```
portainer/
├── app.py              # App Flask + dashboard HTML
├── requirements.txt    # Dependencias: Flask, requests
├── Dockerfile          # Imagen Docker basada en python:3.12-slim
├── docker-compose.yml  # Configuración para Portainer/Docker Compose
└── README.md           # Este archivo
```

## Notas

- No se requiere ninguna API key para el funcionamiento actual.
- CoinGecko tiene límites de rate limit en su tier gratuito; si recibes errores 429, espera unos minutos y vuelve a intentar.
- Si cambias la ubicación del clima, edita la latitud y longitud en `app.py` en la función `weather()`.
