import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardComponent } from './dashboard/dashboard.component';
import { ReportComponent } from './report/report.component';
import { MonthreportComponent } from './monthreport/monthreport.component';
import { LoginComponent } from './login/login.component';
import { EmployeemasterComponent } from './employeemaster/employeemaster.component';
import { ShiftmanagementComponent } from './shiftmanagement/shiftmanagement.component';
import { AddshiftmanagementComponent } from './shiftmanagement/addshiftmanagement/addshiftmanagement.component';
import { ShiftstrengthComponent } from './shiftstrength/shiftstrength.component';
import { ShiftskillComponent } from './shiftskill/shiftskill.component';
import { MaterialtransactionComponent } from './materialtransaction/materialtransaction.component';


const routes: Routes = [
  {path: '', redirectTo:'/dashboard', pathMatch:'full'},
  {path: 'dashboard', component:DashboardComponent},
  {path: 'report', component:ReportComponent},
  {path: 'monthly', component:MonthreportComponent},
  {path: 'login', component:LoginComponent},
  {path: 'employee', component:EmployeemasterComponent},
  {path: 'Shift_Management', component:ShiftmanagementComponent},
  {path: 'Shift_Management/Add_Edit', component:AddshiftmanagementComponent},
  {path: 'Shift_Strength', component:ShiftstrengthComponent},
  {path: 'Shift_Skill', component:ShiftskillComponent},
  {path: 'material', component:MaterialtransactionComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
