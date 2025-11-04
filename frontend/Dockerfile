FROM node:18-alpine

WORKDIR /app

# Установка системных зависимостей для сборки нативных модулей
RUN apk add --no-cache python3 make g++

# Установка зависимостей с обработкой ошибок
COPY package*.json ./
RUN npm ci --legacy-peer-deps || npm install --legacy-peer-deps

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
