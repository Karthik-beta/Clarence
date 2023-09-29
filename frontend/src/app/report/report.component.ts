import { Component, OnInit } from '@angular/core';
import { SharedService } from '../shared.service';
import { LazyLoadEvent } from 'primeng/api';
import { TableLazyLoadEvent } from 'primeng/table';


interface Location {
  name: string
}

interface Criteria {
  name: string
}



@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.css']
})
export class ReportComponent implements OnInit {

  combinedLogs: any[] = [];
  totalRecords: number = 0;
  rowsPerPageOptions: number[] = [10, 20, 30];
  rows: number = 10;
  currentPage: number = 1;
  loading: boolean = false;
  rangeDates: Date[] | undefined;

  text: string = '';
  results: any[] = [];

  selectedEmployee: any = null; // Declare selectedEmployee here

  locations: Location[];

    selectedLocation!: Location;

  criterias: Criteria[];

    selectedCriteria!: Criteria;

  constructor(private service: SharedService) {
    this.locations = [
      {name: 'All'},
      {name: 'CHS'},
      {name: 'CKT'},
      {name: 'CET'}
    ];
    this.criterias = [
      {name: 'All Employees'},
      {name: 'Select Employee'},
      {name: 'Department'},
      {name: 'Designation'},
      {name: 'Division'},
      {name: 'Category'},
      {name: 'Location'}
    ];
  }

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.loading = true;

    const params = {
      page: this.currentPage.toString(),
      page_size: this.rows.toString(),
      employee_id: this.selectedEmployee ? this.selectedEmployee.employee_id : '',
    };

    this.service.getEmployeeLogs(params).subscribe((data: any) => {
      this.combinedLogs = data.results; // Assuming your API response has a 'results' property
      this.totalRecords = data.count;   // Assuming your API response has a 'count' property
      this.loading = false;
    });
  }




  onPageChange(event: any): void {
    this.rows = event.rows;
    this.currentPage = event.page;

    this.loadData();
  }

  loadLogs(event: TableLazyLoadEvent): void {
    this.loading = true;

    const params: any = {
      page: ((event.first || 0) / (event.rows || 10) + 1).toString(),
      page_size: (event.rows || 10).toString(),
      sortField: event.sortField || '',
      sortOrder: event.sortOrder === 1 ? 'asc' : 'desc',
      employee_id: this.selectedEmployee ? this.selectedEmployee.employee_id : '',
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

  search(event: any) {
    const searchTerm = event.query;
    this.service.getCombinedAutocompleteSuggestions(searchTerm)
      .subscribe(data => {
        this.results = data;
      });
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


}
