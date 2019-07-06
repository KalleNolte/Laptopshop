import * as io from 'socket.io-client';
import { Observable } from 'rxjs/';

export class WebsocketService {
    private url = 'http://localhost:5001/';
    private socket;

    constructor() {
        this.socket = io.connect(this.url);
    }

    public sendMessage(message) {
        this.socket.emit('new-message', message);
    }

    public getMessages = () => {
        return Observable.create((observer) => {
            this.socket.on('new-message', (message) => {
                observer.next(message);
            });
        });
    }
}
