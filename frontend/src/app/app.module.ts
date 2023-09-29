import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { SidebarModule } from 'primeng/sidebar';
import { ButtonModule } from 'primeng/button';
import { TableModule } from 'primeng/table';
import { HttpClientModule } from '@angular/common/http';
import { PaginatorModule } from 'primeng/paginator';
import { MenuModule } from 'primeng/menu';
import { MessageService } from 'primeng/api';
import { ConfirmationService } from 'primeng/api';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { ToastModule } from 'primeng/toast';
import { NgApexchartsModule } from 'ng-apexcharts';
import { SkeletonModule } from 'primeng/skeleton';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { DropdownModule } from 'primeng/dropdown';
import { CalendarModule } from 'primeng/calendar';
import { DialogModule } from 'primeng/dialog';



import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedService } from './shared.service';

import { DashboardComponent } from './dashboard/dashboard.component';
import { NavComponent } from './nav/nav.component';
import { ReportComponent } from './report/report.component';
import { MonthreportComponent } from './monthreport/monthreport.component';
import { LoginComponent } from './login/login.component';
import { EmployeemasterComponent } from './employeemaster/employeemaster.component';
import { AddEditEmpComponent } from './employeemaster/add-edit-emp/add-edit-emp.component';
import { ShiftmanagementComponent } from './shiftmanagement/shiftmanagement.component';
import { AddshiftmanagementComponent } from './shiftmanagement/addshiftmanagement/addshiftmanagement.component';
import { ShiftstrengthComponent } from './shiftstrength/shiftstrength.component';
import { ShiftskillComponent } from './shiftskill/shiftskill.component';
import { MaterialtransactionComponent } from './materialtransaction/materialtransaction.component';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    NavComponent,
    ReportComponent,
    MonthreportComponent,
    LoginComponent,
    EmployeemasterComponent,
    AddEditEmpComponent,
    ShiftmanagementComponent,
    AddshiftmanagementComponent,
    ShiftstrengthComponent,
    ShiftskillComponent,
    MaterialtransactionComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    SidebarModule,
    ButtonModule,
    TableModule,
    HttpClientModule,
    PaginatorModule,
    MenuModule,
    ConfirmDialogModule,
    ToastModule,
    NgApexchartsModule,
    SkeletonModule,
    AutoCompleteModule,
    DropdownModule,
    CalendarModule,
    DialogModule,
    ReactiveFormsModule,
    FormsModule,
  ],
  providers: [
    MessageService,
    ConfirmationService,
    SharedService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
