export interface User { id?: number; username: string; first_name?: string; last_name?: string; email?: string; role?: string; is_staff?: boolean; }
export interface Employee { id?: number; employee_id?: string; first_name: string; last_name: string; email: string; phone?: string; position?: string; department?: number | { id: number; name: string }; hire_date?: string; salary?: number; is_active?: boolean; }
export interface Department { id?: number; name: string; description?: string; employee_count?: number; }
export interface Attendance { id?: number; employee: number | Employee; employee_name?: string; employee_id?: string; date: string; status: string; check_in?: string; check_out?: string; notes?: string; }
export interface Dashboard { total_employees?: number; active_employees?: number; total_departments?: number; present_today?: number; late_today?: number; absent_today?: number; leave_today?: number; attendance_rate?: number; recent_attendance?: Attendance[]; department_breakdown?: { id: number; name: string; employee_count: number }[]; weekly_attendance?: { date: string; present: number; late: number; absent: number; leave: number }[]; }
export interface LeaveRequest { id?: number; employee: number | Employee; employee_name?: string; leave_type: string; start_date: string; end_date: string; reason?: string; status: 'Pending'|'Approved'|'Rejected'; }
export interface Shift { id?: number; name: string; start_time: string; end_time: string; grace_minutes?: number; }
export interface Timesheet { id?: number; employee: number | Employee; date: string; shift?: string; hours: number; status: string; }
export interface PayrollRecord { id?: number; employee: number | Employee; period: string; gross_pay: number; deductions: number; net_pay: number; status: string; }
export interface EmployeeDocument { id?: number; employee: number | Employee; document_type: string; name: string; expires_on?: string; status: string; }
export interface AuditEntry { id?: number; actor?: string; action: string; resource: string; created_at: string; details?: string; }
