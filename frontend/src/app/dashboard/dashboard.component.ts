import { Component, OnInit, ViewChild } from '@angular/core';
import { SharedService } from '../shared.service';
import { ApexChart, ApexDataLabels, ApexNonAxisChartSeries, ApexTitleSubtitle } from 'ng-apexcharts';
import { TableLazyLoadEvent } from 'primeng/table';





interface Location {
  name: string
}



@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  constructor(private service: SharedService) {
    this.locations = [
      {name: 'All'},
      {name: 'CHS'},
      {name: 'CKT'},
      {name: 'CET'}
    ];
   }

   combinedLogs: any[] = []; // Initialize as an array
   totalRecords: number = 0;
   rowsPerPageOptions: number[] = [10, 20, 30];
   rows: number = 10;
   currentPage: number = 1;
   loading: boolean = false;

   date: Date | undefined;
   text: string = '';
   results: any[] = [];

   selectedEmployee: any = null;
   locations: Location[];
   selectedLocation!: Location;
   autocompleteSuggestions: any[] = [];

   ngOnInit(): void {
     this.loadData();
     this.fetchAttendanceStatistics();
   }

   onDateSelected(): void {
    // Call the loadData function with the selected date filter
    this.loadData();
  }

  private formatDate(date: Date): string {
    const day = date.getDate();
    const month = date.getMonth() + 1; // Months are zero-based
    const year = date.getFullYear();
    return `${year}/${month}/${day}`;
  }

  loadData(): void {
    this.loading = true;
    const selectedDate = this.date ? this.formatDate(this.date) : '';

    // console.log('Selected Date:', selectedDate); // Check the selected date in the console

    const params: any = {
      page: this.currentPage.toString(),
      page_size: this.rows.toString(),
      search: this.text,
      date: selectedDate,
      // Add other filter parameters here if needed
    };

    // console.log('Params:', params); // Check the complete params object

    this.service.getEmployeeLogs(params).subscribe((data: any) => {
      this.combinedLogs = data.results;
      this.totalRecords = data.count;
      this.loading = false;
    });
  }








  loadLogs(event: TableLazyLoadEvent): void {
    this.loading = true;

    const params: any = {
      page: ((event.first || 0) / (event.rows || 10) + 1).toString(),
      page_size: (event.rows || 10).toString(),
      sortField: event.sortField || '',
      sortOrder: event.sortOrder === 1 ? 'asc' : 'desc',
      // employee_id: this.selectedEmployee ? this.selectedEmployee.employee_id : '',
    };

    this.service.getEmployeeLogs(params).subscribe((data: any) => {
      this.combinedLogs = data.results;
      this.totalRecords = data.count;
      this.loading = false;
    });
  }

  getShiftStatusColor(shiftStatus: string): string {
    if (shiftStatus === 'A') {
      return 'red';
    } else if (shiftStatus === 'P') {
      return 'green';
    } else if (shiftStatus === 'A/P' || shiftStatus === 'P/A') {
      return 'orange';
    } else {
      return '';
    }
  }


  search(event: any): void {
    const searchTerm = event.query;
    this.service.getCombinedAutocompleteSuggestions(searchTerm)
      .subscribe(data => {
        this.autocompleteSuggestions = data; // Store autocomplete suggestions
      });
  }



  private labelColorsMap: { [key: string]: string } = {
    'Present': '#00FF00',   // Green for "Present"
    'Absent': '#FF0000',    // Red for "Absent"
    'Late Entry': '#FFA500', // Orange for "Late Entry"
    'Early Exit': '#008080', // Teal for "Early Exit"
    'Overtime': '#FFD700',  // Gold for "Overtime"
    // Add more colors for other attendance statuses if needed
  };






  fetchAttendanceStatistics(): void {
    this.service.getAttendanceStatistics().subscribe((data: any) => {
      // Extract relevant data from the API response
      const attendanceStats: { [key: string]: any } = {
        'Present': data.present,
        'Absent': data.absent,
        'Late Entry': data.late_entry,
        'Early Exit': data.early_exit,
        'Overtime': data.overtime,
      };

      // Define chart labels based on the extracted data keys
      const chartLabels = Object.keys(attendanceStats);

      // Extract chart data values based on the extracted data values
      const chartData = chartLabels.map((label: string) => attendanceStats[label]);

      // Define custom colors using labelColorsMap object
      const labelColorsMap: { [key: string]: string } = {
        'Present': '#FF0000',
        'Absent': '#FF0000',
        'Late Entry': '#FFA500',
        'Early Exit': '#FFD700',
        'Overtime': '#008080',
      };

      // Extract chart data colors based on the labelColorsMap
      const chartDataColors = chartLabels.map((label: string) => labelColorsMap[label]);

      // Set chart data and options
      this.chartLabels = chartLabels;
      this.chartSeries = chartData;

      // Set custom legend marker fill colors
      this.chartOptions.legend.markers.fillColors = chartDataColors;
    });
  }








  chartDataColors: string[] = []; // Initialize an empty array for chart label colors




  chartSeries: ApexNonAxisChartSeries = [];
  chartLabels: string[] = []; // Initialize an empty array for chart labels
  predefinedLabels: string[] = [];



  chartOptions: any = {
    stacked: true, // Define chart options object
    fill: {
      colors: [],  // Will be set later based on dataColors
    },
    legend: {
      show: true,
      stacked: true,
        position: "bottom",
        offsetX: -10,
        offsetY: 0,
        markers: {
          fillColors: this.chartDataColors
        },
        legend: {
          show: true, // Set to true to display the legend
        position: 'bottom',
          labels: {
            colors: ['#FF0000', '#00FF00', '#0000FF'] // change the legend colors here
          }
        }
    }
  }

  chartDetails: ApexChart = {
    type: 'pie',
    // height: '100%',
    // width: '100%',
    toolbar: {
      show: true,
      tools: {
        download: true,
        selection: true,
        zoom: true,
        zoomin: true,
        zoomout: true,
      },
    }
  };
  chartTitle: ApexTitleSubtitle = {
    text: 'Attendance Analysis',
    align: 'left'
  };




  chartDataLabels: ApexDataLabels = {
    enabled: true,
  style: {
    fontSize: '14px',
    fontFamily: 'Helvetica, Arial, sans-serif',
    fontWeight: 'bold',
  }
  };


  getPresentCount(): number {
    const presentIndex = this.chartLabels.indexOf('Present');
    if (presentIndex !== -1) {
      return this.chartSeries[presentIndex];
    }
    return 0; // Default value if "Present" label is not found
  }

  getAbsentCount(): number {
    const absentIndex = this.chartLabels.indexOf('Absent');
    if (absentIndex !== -1) {
      return this.chartSeries[absentIndex];
    }
    return 0; // Default value if "Absent" label is not found
  }

  getLateEntryCount(): number {
    const lateEntryIndex = this.chartLabels.indexOf('Late Entry');
    if (lateEntryIndex !== -1) {
      return this.chartSeries[lateEntryIndex];
    }
    return 0; // Default value if "Late Entry" label is not found
  }

  getEarlyExitCount(): number {
    const earlyExitIndex = this.chartLabels.indexOf('Early Exit');
    if (earlyExitIndex !== -1) {
      return this.chartSeries[earlyExitIndex];
    }
    return 0; // Default value if "Early Exit" label is not found
  }

  getOvertimeCount(): number {
    const overtimeIndex = this.chartLabels.indexOf('Overtime');
    if (overtimeIndex !== -1) {
      return this.chartSeries[overtimeIndex];
    }
    return 0; // Default value if "Early Exit" label is not found
  }

  getLiveHeadcount(): number {
    const totalPresent = this.getPresentCount();
    const totalAbsent = this.getAbsentCount();
    const totalEarlyExit = this.getEarlyExitCount();

    return totalPresent -  totalEarlyExit;
  }


  onEmployeeSelected(selectedEmployee: any) {
    this.selectedEmployee = selectedEmployee;

    // Update the selected employee details based on the selectedEmployee object
    const params = {
      page: this.currentPage.toString(),
      page_size: this.rows.toString(),
      employee_id: this.selectedEmployee ? this.selectedEmployee.employee_id : '',
    };

    this.service.getEmployeeLogs(params).subscribe((data: any) => {
      this.combinedLogs = data.results;
      this.totalRecords = data.count;
      this.loading = false;
    });
  }


  downloadAttendanceData() {
    this.service.downloadAttendanceData().subscribe({
      next: (data) => {
        // Create a Blob object from the response data
        const blob = new Blob([data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

        // Create a URL for the Blob
        const url = window.URL.createObjectURL(blob);

        // Create a link element and trigger a click event to download the file
        const a = document.createElement('a');
        a.href = url;

        // Get the current date
        const currentDate = new Date();

        // Format the date as a string (e.g., "2023-09-01")
        const formattedDate = currentDate.toISOString().split('T')[0];

        // Define the filename based on the formatted date
        const filename = `Attendance_data_${formattedDate}.xlsx`;

        // Set the download attribute with the filename
        a.download = filename;

        document.body.appendChild(a);
        a.click();

        // Clean up
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      },
      error: (error) => {
        // Handle any error that might occur during the download
        console.error('Error downloading employee data:', error);
      }
    });
  }



}
