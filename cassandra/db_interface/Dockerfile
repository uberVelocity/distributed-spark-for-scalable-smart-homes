FROM node:10

# Create app directory
WORKDIR test_sensors

# Install app dependencies
COPY package*.json ./

RUN npm install

# Bundle app source
COPY . .

EXPOSE 4000

CMD ["node", "server/index.js"]
