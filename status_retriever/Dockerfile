FROM node:10

# Create app directory
WORKDIR statusretriever

# Install app dependencies
COPY package*.json ./

RUN npm install

# Bundle app source
COPY . .

EXPOSE 3005

CMD ["node", "server/index.js"]
