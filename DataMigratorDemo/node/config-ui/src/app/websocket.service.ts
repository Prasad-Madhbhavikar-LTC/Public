import { Injectable } from '@angular/core';
import { Subject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {
  private socket!: WebSocket;
  private messageSubject: Subject<any> = new Subject<any>();

  constructor() {
    this.connect();
  }

  private connect(): void {
    try {
      this.socket = new WebSocket('ws://localhost:3000');

      this.socket.onmessage = (event) => {
        console.log(event)
        const data = JSON.parse(event.data);
        this.messageSubject.next(data);
      };

      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      this.socket.onclose = () => {
        console.log('WebSocket connection closed');
      };
    } catch (error) {
      console.error('Error creating WebSocket:', error);
    }
  }

  getMessages(): Observable<any> {
    return this.messageSubject.asObservable();
  }

  ngOnDestroy(): void {
    // Clean up: Close the WebSocket connection
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.close();
    }
  }
}
