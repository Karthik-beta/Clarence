import { Component, OnInit } from '@angular/core';
import { SharedService } from '../shared.service';
import { TableLazyLoadEvent } from 'primeng/table';
import { MessageService, ConfirmationService, ConfirmEventType } from 'primeng/api';

@Component({
  selector: 'app-employeemaster',
  templateUrl: './employeemaster.component.html',
  styleUrls: ['./employeemaster.component.css']
})
export class EmployeemasterComponent implements OnInit {

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

  ModalTitle: string = "";
  ActivateAddEditEmp: boolean = false;
  emp: any;

  visible: boolean = false;

  showDialog() {
    this.visible = true;
  }


  constructor(private service: SharedService, private messageService: MessageService, private confirmationService: ConfirmationService) { }


  addClick() {
    this.emp = {
      employee_id: null,
      device_enroll_id: "",
      employee_name: "",
      company: "",
      location: "",
    };
    this.ModalTitle = "Add New Employee";
    this.ActivateAddEditEmp = true;
  }

  onEmployeeAdded() {
    this.loadData();
  }


  closeClick() {
    this.ActivateAddEditEmp = false;
    this.loadData();
    // window.location.reload();
  }

  editClick(log: any) {
    // console.log(log);
    this.emp = log;
    this.ModalTitle = "Edit Employee Details";
    this.ActivateAddEditEmp = true;
  }
  deleteClick(log: { employee_id: any }) {
    // Extract the employee_id from the log object
    const employeeId = log.employee_id;

    // Display the confirmation dialog before proceeding with deletion
    this.confirmationService.confirm({
      message: 'Are you sure that you want to delete this employee?',
      header: 'Confirmation',
      icon: 'pi pi-exclamation-triangle',
      accept: () => {
        // Call the deleteEmployee method from the service
        this.service.deleteEmployee(employeeId).subscribe({
          next: (response) => {
            // Handle success response if needed
            // console.log('Employee deleted:', response);

            // Show success message
            this.messageService.add({
              severity: 'success',
              summary: 'Success',
              detail: 'Employee has been deleted successfully.'
            });

            // Load data
            this.loadData();
          },
          error: (error) => {
            // Handle error if needed
            console.error('Error deleting employee:', error);

            // Show error message
            this.messageService.add({
              severity: 'error',
              summary: 'Error',
              detail: 'Failed to delete employee.'
            });
          }
        });
      },
      reject: () => {
        // User rejected the confirmation, do nothing or handle as needed
        this.messageService.add({ severity: 'error', summary: 'Rejected', detail: 'You have Cancelled' });
        // console.log('Deletion cancelled by user.');
      }
    });
  }




  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.loading = true;

    const params = {
      page: this.currentPage.toString(),
      page_size: this.rows.toString(),
      employeeid: this.selectedEmployee ? this.selectedEmployee.employeeid : '',
    };

    this.service.getEmployeeList(params).subscribe((data: any) => {
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

    this.service.getEmployeeList(params).subscribe((data: any) => {
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

    this.service.getEmployeeDetails(params).subscribe((data: any) => {
      this.combinedLogs = data.results;
      this.totalRecords = data.count;
      this.loading = false;
    });
  }




  downloadEmployeeData() {
    this.service.downloadEmployeeData().subscribe({
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
        const filename = `employee_data_${formattedDate}.xlsx`;

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
