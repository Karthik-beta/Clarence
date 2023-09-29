import { Component, OnDestroy, OnInit } from '@angular/core';

@Component({
  selector: 'app-shiftskill',
  templateUrl: './shiftskill.component.html',
  styleUrls: ['./shiftskill.component.css']
})
export class ShiftskillComponent implements OnInit, OnDestroy {
  currentShift: string = '';
  currentTime: Date = new Date();
  clockInterval: any; // Declare the clockInterval property

  ngOnInit() {
    this.updateClock(); // Start the real-time clock
  }

  ngOnDestroy() {
    clearInterval(this.clockInterval); // Clear the clock interval when the component is destroyed
  }

  getCurrentShift(): string {
    const currentHour = this.currentTime.getHours();

    if (currentHour >= 6 && currentHour < 14) {
      return 'A';
    } else if (currentHour >= 14 && currentHour < 22) {
      return 'B';
    } else {
      return 'C';
    }
  }

  updateClock() {
    this.clockInterval = setInterval(() => {
      this.currentTime = new Date();
      this.currentShift = this.getCurrentShift();
    }, 1000); // Update the clock every second
  }


  selectedEmployeeSubAssembly: string='';
  selectedEmployeeSubAssembly2: string='';
  selectedEmployeeMainAssembly: string='';
  selectedEmployeeInstallationTesting: string='';

  employeeOptions: string[] = [
    'Meshak, 223044347',
    'Ramachandra G, 305020222',
    'Raja Shankara G, 305022167',
    'Nagendra Swamy C G, 305021393',
    // Add more employee options here if needed
  ];



}

