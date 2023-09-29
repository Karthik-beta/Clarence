import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedService {

  private baseUrl = 'http://localhost:8000';




  private isLoginPageSubject = new BehaviorSubject<boolean>(false);
  isLoginPage$ = this.isLoginPageSubject.asObservable();

  setIsLoginPage(value: boolean): void {
    this.isLoginPageSubject.next(value);
  }


  constructor(private http:HttpClient) { }

  getEmployeeLogs(params: any): Observable<any> {
    let httpParams = new HttpParams();

    for (const key in params) {
      if (params.hasOwnProperty(key)) {
        httpParams = httpParams.append(key, params[key]);
      }
    }

    return this.http.get(`${this.baseUrl}/attendance_record/`, { params: httpParams });
  }

  getEmployeeDetails(param:any): Observable<any> {
    let httpParams = new HttpParams();

    for (const key in param) {
      if (param.hasOwnProperty(key)) {
        httpParams = httpParams.append(key, param[key]);
      }
    }

    return this.http.get(`${this.baseUrl}/employeecrud/`, { params: httpParams });
  }

  getCombinedAutocompleteSuggestions(searchTerm: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/autocomplete/?term=${searchTerm}`);
  }

  getAttendanceStatistics():Observable<any[]>{
    return this.http.get<any[]>(this.baseUrl+'/AttendanceStatistics/');
  }

  getemployee_presence():Observable<any[]>{
    return this.http.get<any[]>(this.baseUrl+'/AttendanceStatisticsMonth/');
  }

  getEmployeeList(params: any): Observable<any> {
    let httpParams = new HttpParams();

    for (const key in params) {
      if (params.hasOwnProperty(key)) {
        httpParams = httpParams.append(key, params[key]);
      }
    }

    return this.http.get(`${this.baseUrl}/employee/`, { params: httpParams });
  }

  getEmployeeDetailsById(employeeId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/employee/${employeeId}/`);
  }

  addEmployee(employee: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/employee/`, employee);
  }

  updateEmployee(employee: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/employee/${employee.employee_id}/`, employee);
  }

  deleteEmployee(employeeId: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/employee/${employeeId}/`);
  }


  downloadEmployeeData(): Observable<any> {
    return this.http.get(`${this.baseUrl}/download_employee_data/`, {
      responseType: 'blob' as 'json', // Set the response type to 'blob' for binary data
    });
  }

  downloadAttendanceData(): Observable<any> {
    return this.http.get(`${this.baseUrl}/download_attendance_data/`, {
      responseType: 'blob' as 'json', // Set the response type to 'blob' for binary data
    });
  }




}
