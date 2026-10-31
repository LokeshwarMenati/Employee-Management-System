import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, of } from 'rxjs';
import { environment } from '../../environments/environment';
import { Employee, Department, Attendance, Dashboard, LeaveRequest, Shift, Timesheet, PayrollRecord, EmployeeDocument, AuditEntry } from './models';
import { MOCK_DASHBOARD, MOCK_EMPLOYEES, MOCK_DEPARTMENTS, MOCK_ATTENDANCE, MOCK_LEAVE_REQUESTS, MOCK_SHIFTS, MOCK_TIMESHEETS, MOCK_PAYROLL, MOCK_DOCUMENTS, MOCK_AUDIT } from './mock-data';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  private u = (p: string) => `${environment.apiUrl}/${p}`;

  dashboard() {
    return this.http.get<Dashboard>(this.u('dashboard/')).pipe(
      catchError(() => of(MOCK_DASHBOARD))
    );
  }

  employees() {
    return this.http.get<Employee[]>(this.u('employees/')).pipe(
      catchError(() => of(MOCK_EMPLOYEES))
    );
  }

  createEmployee(v: Employee) {
    return this.http.post<Employee>(this.u('employees/'), v).pipe(
      catchError(() => of({ ...v, id: Math.floor(Math.random() * 1000) + 10 }))
    );
  }

  updateEmployee(id: number, v: Employee) {
    return this.http.put<Employee>(this.u(`employees/${id}/`), v).pipe(
      catchError(() => of(v))
    );
  }

  deleteEmployee(id: number) {
    return this.http.delete(this.u(`employees/${id}/`)).pipe(
      catchError(() => of(null))
    );
  }

  departments() {
    return this.http.get<Department[]>(this.u('departments/')).pipe(
      catchError(() => of(MOCK_DEPARTMENTS))
    );
  }

  createDepartment(v: Department) {
    return this.http.post<Department>(this.u('departments/'), v).pipe(
      catchError(() => of({ ...v, id: Math.floor(Math.random() * 1000) + 10, employee_count: 0 }))
    );
  }

  updateDepartment(id: number, v: Department) {
    return this.http.put<Department>(this.u(`departments/${id}/`), v).pipe(
      catchError(() => of(v))
    );
  }

  deleteDepartment(id: number) {
    return this.http.delete(this.u(`departments/${id}/`)).pipe(
      catchError(() => of(null))
    );
  }

  attendance() {
    return this.http.get<Attendance[]>(this.u('attendance/')).pipe(
      catchError(() => of(MOCK_ATTENDANCE))
    );
  }

  createAttendance(v: Attendance) {
    return this.http.post<Attendance>(this.u('attendance/'), v).pipe(
      catchError(() => of({ ...v, id: Math.floor(Math.random() * 1000) + 10 }))
    );
  }

  leaveRequests() {
    return this.http.get<LeaveRequest[]>(this.u('leave-requests/')).pipe(
      catchError(() => of(MOCK_LEAVE_REQUESTS))
    );
  }

  createLeave(v: LeaveRequest) {
    return this.http.post<LeaveRequest>(this.u('leave-requests/'), v).pipe(
      catchError(() => of({ ...v, id: Math.floor(Math.random() * 1000) + 10 }))
    );
  }

  updateLeave(id: number, status: string) {
    const action = status === 'approved' ? 'approve' : 'reject';
    return this.http.post<LeaveRequest>(this.u(`leave-requests/${id}/${action}/`), {}).pipe(
      catchError(() => of({ id, status: status === 'approved' ? 'Approved' : 'Rejected' } as LeaveRequest))
    );
  }

  shifts() {
    return this.http.get<Shift[]>(this.u('shifts/')).pipe(
      catchError(() => of(MOCK_SHIFTS))
    );
  }

  timesheets() {
    return this.http.get<Timesheet[]>(this.u('timesheets/')).pipe(
      catchError(() => of(MOCK_TIMESHEETS))
    );
  }

  payroll() {
    return this.http.get<PayrollRecord[]>(this.u('payslips/')).pipe(
      catchError(() => of(MOCK_PAYROLL))
    );
  }

  documents() {
    return this.http.get<EmployeeDocument[]>(this.u('employee-documents/')).pipe(
      catchError(() => of(MOCK_DOCUMENTS))
    );
  }

  audit() {
    return this.http.get<AuditEntry[]>(this.u('audit-logs/')).pipe(
      catchError(() => of(MOCK_AUDIT))
    );
  }
}
