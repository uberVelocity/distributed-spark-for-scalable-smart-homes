import axios from 'axios';

const url = "http://status-retriever:3005/api/status/";

class StatusRetriever {

    static async getStatus() {
        alert(url);
        return await axios.post(`${url}`);
    }
}

export default StatusRetriever;