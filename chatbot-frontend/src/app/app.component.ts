import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="chat-container">
      <div class="messages">
        <div *ngFor="let message of messages" [ngClass]="{'user-message': message.isUser, 'bot-message': !message.isUser}">
          {{ message.text }}
        </div>
      </div>
      <div class="input-area">
        <input [(ngModel)]="userInput" (keyup.enter)="sendMessage()" placeholder="Type your message...">
        <button (click)="sendMessage()">Send</button>
      </div>
      <div class="file-upload">
        <input type="file" (change)="uploadDocument($event)" accept=".pdf">
      </div>
    </div>
  `,
  styles: [`
    .chat-container { max-width: 600px; margin: 20px auto; }
    .messages { height: 300px; border: 1px solid #ccc; overflow-y: auto; padding: 10px; margin-bottom: 10px; }
    .user-message { text-align: right; color: blue; }
    .bot-message { text-align: left; color: green; }
    .input-area input { width: 70%; padding: 5px; }
    .input-area button { padding: 5px 10px; }
  `]
})
export class AppComponent {
  messages: {text: string, isUser: boolean}[] = [];
  userInput: string = '';

  constructor(private http: HttpClient) {}

  sendMessage() {
    if (this.userInput.trim() === '') return;

    this.messages.push({text: this.userInput, isUser: true});
    
    this.http.post('http://localhost:5000/query', {query: this.userInput})
      .subscribe({
        next: (response: any) => {
          this.messages.push({text: response.answer, isUser: false});
        },
        error: (error) => {
          console.error('Error:', error);
          this.messages.push({text: 'Sorry, I encountered an error.', isUser: false});
        },
        complete: () => {
          this.userInput = '';
        }
      });
  }

  uploadDocument(event: any) {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append('file', file);

      this.http.post('http://localhost:5000/upload', formData)
        .subscribe({
          next: (response: any) => {
            this.messages.push({text: 'File uploaded successfully', isUser: false});
          },
          error: (error) => {
            console.error('Error uploading file:', error);
            this.messages.push({text: 'Error uploading file', isUser: false});
          }
        });
    }
  }
}