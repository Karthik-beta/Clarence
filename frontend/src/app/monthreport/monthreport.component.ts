import { Component } from '@angular/core';
import { SharedService } from '../shared.service';
import { ApexChart, ApexDataLabels, ApexNonAxisChartSeries, ApexTitleSubtitle } from 'ng-apexcharts';
import { TableLazyLoadEvent } from 'primeng/table';

@Component({
  selector: 'app-monthreport',
  templateUrl: './monthreport.component.html',
  styleUrls: ['./monthreport.component.css']
})
export class MonthreportComponent {

  constructor(private service: SharedService) { }


  combinedLogs: any[] = [];
  totalRecords: number = 0;
  rowsPerPageOptions: number[] = [10, 20, 30];
  rows: number = 10;
  currentPage: number = 1;
  loading: boolean = false;

  date: Date[] | undefined;


  ngOnInit(): void {
    this.fetchEmployeePresence();
    this.loadData();
  }

  loadData(): void {
    this.loading = true;

    const params = {
      page: this.currentPage.toString(),
      page_size: this.rows.toString(),
      // employee_id: this.selectedEmployee ? this.selectedEmployee.employee_id : '',
    };

    this.service.getEmployeeLogs(params).subscribe((data: any) => {
      this.combinedLogs = data.results; // Assuming your API response has a 'results' property
      this.totalRecords = data.count;   // Assuming your API response has a 'count' property
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


  fetchEmployeePresence(): void {
    this.service.getemployee_presence().subscribe((data: any) => {
      if (data && data.length > 0) {
        const presenceData = data;

        this.chartBarLabels = presenceData.map((entry: any) => entry.logdate);
        this.chartBarSeries = [
          {
            name: 'Early Exit',
            data: presenceData.map((entry: any) => entry.early_exit_count)
          },
          {
            name: 'Present',
            data: presenceData.map((entry: any) => entry.present_count)
          },
          {
            name: 'Late Entry',
            data: presenceData.map((entry: any) => entry.late_entry_count)
          },
          {
            name: 'Absent',
            data: presenceData.map((entry: any) => entry.absent_count)
          },
          {
            name: 'Overtime',
            data: presenceData.map((entry: any) => entry.overtime_count)
          }
        ];
      }
    });
  }


  chartBarOptions: ApexChart = {
    type: 'bar',
    height: '300px',
    // width: '100%',
    stacked: true,
    zoom: {
      enabled: false
    },

    toolbar: {
      show: true,
      tools: {
        download: true,
        selection: true,
        zoom: true,
        zoomin: true,
        zoomout: true,
        pan: false,
      },
    },
    animations: {
      enabled: true,
      easing: 'easeinout',
      speed: 800,
      animateGradually: {
        enabled: true,
        delay: 150
      },
      dynamicAnimation: {
        enabled: true,
        speed: 350
      }
    }
  };
  chartBarTitle: ApexTitleSubtitle = {
    text: 'Attendance Strength',
    align: 'center'
  };
  chartDataLabels: ApexDataLabels = {
    enabled: true,
  style: {
    fontSize: '14px',
    fontFamily: 'Helvetica, Arial, sans-serif',
    fontWeight: 'bold',
  }
  };


  chartBarSeries: any[] = [];
  chartBarLabels: string[] = [];




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
