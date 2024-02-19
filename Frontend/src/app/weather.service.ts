import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { WeatherData } from './weather.interface';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class WeatherService {
  private endpoint = 'https://api.openweathermap.org/data/2.5/weather?lat=47.93972794656145&lon=12.848657792315324&appid=' + environment.weatherAPIKey + '&units=metric';

  constructor(private http: HttpClient) {}

  getWeather(): Observable<WeatherData> {
    return this.http.get<WeatherData>(this.endpoint);
  }
}
