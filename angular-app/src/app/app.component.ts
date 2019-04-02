import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  title = "Group 9's Company";

  weatherDegrees = 0;

  weatherApiUrl = "https://api.openweathermap.org/data/2.5/";
  weatherApiKey = "59e2a148fe78b28b8bd2ad6812b4bff0";
  cityId = 6942553;

  constructor (private http: HttpClient) {

  }

  ngOnInit(): void {
    this.http.get(`${this.weatherApiUrl}weather?id=${this.cityId}&APPID=${this.weatherApiKey}`).subscribe((result: any) => {
      this.weatherDegrees = result.main.temp - 273.15;
    });
  }
}
