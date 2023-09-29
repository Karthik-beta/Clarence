import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { SharedService } from 'src/app/shared.service';
import { FormGroup, FormControl } from '@angular/forms';
import { MessageService, ConfirmationService, ConfirmEventType } from 'primeng/api';


@Component({
  selector: 'app-add-edit-emp',
  templateUrl: './add-edit-emp.component.html',
  styleUrls: ['./add-edit-emp.component.css']
})
export class AddEditEmpComponent implements OnInit {
  @Input() emp: any;
  @Output() employeeAdded: EventEmitter<void> = new EventEmitter<void>();

  employee_id!:number;
  device_enroll_id:string="";
  employee_name:string="";
  company:string="";
  location:string="";


  constructor(private service: SharedService, private messageService: MessageService, private confirmationService: ConfirmationService) { }

  ngOnInit(): void {
    this.employee_id = this.emp.employee_id;
    this.device_enroll_id = this.emp.device_enroll_id;
    this.employee_name = this.emp.employee_name;
    this.company = this.emp.company;
    this.location = this.emp.location;
  }


  addEmployee() {
    // Create an employee object from form data
    const employee = {
      employee_id: this.employee_id,
      device_enroll_id: this.device_enroll_id,
      employee_name: this.employee_name,
      company: this.company,
      location: this.location,
      // Add other properties as needed
    };

    // Call the service method to update employee data
    this.service.addEmployee(employee).subscribe({
      next: (response) => {
        // Handle success response if needed
        // console.log('Employee data updated:', response);

        // Show success message
        this.messageService.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Successfully Added New Employee'
        });

        // Programmatically trigger the Close button
        const closeButton = document.getElementById('closeButton') as HTMLButtonElement;
        if (closeButton) {
          closeButton.click();
        }

        // Emit event to notify parent component
        this.employeeAdded.emit();

      },
      error: (error) => {
        // Handle error if needed
        // console.error('Error updating employee data:', error);

        // Show error message
        this.messageService.add({ severity: 'warn', summary: 'Failed', detail: 'Failed to Add Employee' });
      }
    });
  }




  updateEmployee(){
    var employee = {
      employee_id: this.employee_id,
      device_enroll_id: this.device_enroll_id,
      employee_name: this.employee_name,
      company: this.company,
      location: this.location,
    };

    this.service.updateEmployee(employee).subscribe({
      next: (response) => {
        // Handle success response if needed
        // console.log('Employee updated:', response);

        // Show success message
         this.messageService.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Successfully Updated Employee Details'
        });

        // Programmatically trigger the Close button
        const closeButton = document.getElementById('closeButton') as HTMLButtonElement;
        if (closeButton) {
          closeButton.click();
        }

        // Emit event to notify parent component
        this.employeeAdded.emit();

      },
      error: (error) => {
        // Handle error if needed
        // console.error('Error updating employee:', error);

        // Show error message
        this.messageService.add({ severity: 'warn', summary: 'Failed', detail: 'Failed to Update Employee Details' });

      }
    });
  }

  deleteEmployee() {
    this.service.deleteEmployee(this.employee_id).subscribe({
      next: (response) => {
        // Handle success response if needed
        console.log('Employee deleted:', response);
      },
      error: (error) => {
        // Handle error if needed
        console.error('Error deleting employee:', error);
      }
    });
  }





}
