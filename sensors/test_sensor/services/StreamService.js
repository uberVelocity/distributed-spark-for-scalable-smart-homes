/**
 * This directly communicates with the database interface.
 * Not the case in the final implementation.
 */
const url = "http://dbinterface:4000/api/insert/test";
const axios = require('axios');

module.exports = class StreamService {

    static async streamData(data) {
        return await axios.post(url, {
            data
        });
    }
}