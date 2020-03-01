
const dataServerUrl = "http://127.0.0.1:9950";

let instance = null;
class Service {
    constructor() {
        if (!instance) {
            instance = this;
        }

        return instance;
    }

    getServerVideoUrl() {
        return this.serverVideoUrl;
    }

    setUserId(data) {
        this.userId = data;
    }

    getUserId() {
        return this.userId;
    }

}

const DataService = new Service();
export default DataService;
