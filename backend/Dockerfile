FROM node:14-alpine AS base

FROM base AS builder
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
RUN wget -O wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x wait-for-it.sh

FROM base AS deps
COPY package*.json ./
RUN npm install --only=production

FROM base
WORKDIR /app
RUN apk add --no-cache bash
COPY --from=builder wait-for-it.sh /usr/local/bin/
COPY --from=builder dist .
COPY --from=deps node_modules node_modules
COPY docker-entrypoint.sh /usr/local/bin/

ARG PORT=3000
ENV PORT $PORT
EXPOSE $PORT

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["node", "index.js"]