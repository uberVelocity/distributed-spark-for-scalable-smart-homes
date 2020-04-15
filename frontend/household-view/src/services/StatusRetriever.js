import axios from 'axios';

const url = "http://localhost:3005/api/status/";

class StatusRetriever {
    static async getStatus() {
        return await axios.post(`${url}`);
    }
}

export default StatusRetriever;