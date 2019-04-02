import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-clock',
  templateUrl: './clock.component.html',
  styleUrls: ['./clock.component.css']
})
export class ClockComponent implements OnInit {

  todayDate;
  constructor () {
    this.todayDate = new Date();
  }

  ngOnInit() {
  }

}
