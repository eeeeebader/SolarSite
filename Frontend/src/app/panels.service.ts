import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Panel } from './panel.interface';
import { environment as env } from '../environments/environment';

@Injectable({
  providedIn: 'root',
})

export class PanelsService {
  private endpoint = env.backendPath || 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getPanels(): Observable<Panel> {
    return this.http.get<Panel>(`${this.endpoint}/panels`);
  }

  getPanel(id: string): Observable<Panel> {
    return this.http.get<Panel>(`${this.endpoint}/panels/${id}`);
  }
}
