/**
 * This directly communicates with the database interface.
 * Not the case in the final implementation.
 */
const url = "http://db_interface:4001/api/insert";

module.exports = class StreamService {

    static async streamData(data) {
        return await axios.post(url, {
            data
        });
    }

}