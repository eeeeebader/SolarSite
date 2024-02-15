import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { PanelComponent } from "./panel/panel.component";
import { WeatherService } from './weather.service';
import { WeatherData } from './weather.interface';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, HttpClientModule, PanelComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'Frontend';

  readonly iconToDescriptionLookup: { [iconCode: string]: { description: string; dayOrNight: string } } = {
    "01d": { description: "clear-sky", dayOrNight: "day" },
    "01n": { description: "clear-sky", dayOrNight: "night" },
    "02d": { description: "few-clouds", dayOrNight: "day" },
    "02n": { description: "few-clouds", dayOrNight: "night" },
    "03d": { description: "scattered-clouds", dayOrNight: "day" },
    "03n": { description: "scattered-clouds", dayOrNight: "night" },
    "04d": { description: "broken-clouds", dayOrNight: "day" },
    "04n": { description: "broken-clouds", dayOrNight: "night" },
    "09d": { description: "shower-rain", dayOrNight: "day" },
    "09n": { description: "shower-rain", dayOrNight: "night" },
    "10d": { description: "rain", dayOrNight: "day" },
    "10n": { description: "rain", dayOrNight: "night" },
    "11d": { description: "thunderstorm", dayOrNight: "day" },
    "11n": { description: "thunderstorm", dayOrNight: "night" },
    "13d": { description: "snow", dayOrNight: "day" },
    "13n": { description: "snow", dayOrNight: "night" },
    "50d": { description: "mist", dayOrNight: "day" },
    "50n": { description: "mist", dayOrNight: "night" }
    };

  public icon: string = "few-clouds";
  public dayOrNight: string = "day";
  

  //private ctx: CanvasRenderingContext2D | null = null;

  constructor(private weatherService: WeatherService) {}

  ngOnInit(): void {
    this.weatherService.getWeather().subscribe((weather:any) => {
      this.setDescription;
      this.setTime;
      console.log(this.icon, this.dayOrNight);
    });
  }

  setDescription(iconCode: string): void {
    const iconDescription = this.iconToDescriptionLookup[iconCode];
    this.icon = iconDescription ? iconDescription.description : "few-clouds";
  }

  setTime(iconCode: string): void {
    const iconDescription = this.iconToDescriptionLookup[iconCode];
    this.dayOrNight = iconDescription ? iconDescription.description : "day";
  }
}

