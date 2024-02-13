import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Panel } from './panel.interface';

@Injectable({
  providedIn: 'root',
})

export class PanelsService {
  private baseUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getPanels(): Observable<Panel> {
    //console.log(this.http.get<Panel>(`${this.baseUrl}/panels`));
    return this.http.get<Panel>(`${this.baseUrl}/panels`);
  }
}
