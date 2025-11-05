FROM node:jod-alpine3.21

WORKDIR /app

COPY package*.json ./

RUN mkdir -p /app/node_modules && chown -R node:node /app

USER node

RUN npm install

COPY --chown=node:node . .

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]


