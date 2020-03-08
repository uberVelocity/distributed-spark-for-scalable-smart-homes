import axios from 'axios';

const url = "http://localhost:4002/api/history/";

class HistoryService {

    static async getHeater() {
        return await axios.post(`${url}heater`);
    }

    static async getLamp() {
        return await axios.post(`${url}lamp`);
    }

    static async getVacuum() {
        return await axios.post(`${url}vacuum`);
    }

}

export default HistoryService;