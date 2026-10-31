import { Dashboard, Employee, Department, Attendance, LeaveRequest, Shift, Timesheet, PayrollRecord, EmployeeDocument, AuditEntry } from './models';

export const MOCK_DEPARTMENTS: Department[] = [
  { id: 1, name: 'Engineering', description: 'Software engineering, DevOps and infrastructure', employee_count: 3 },
  { id: 2, name: 'People Operations', description: 'HR, recruiting, and culture', employee_count: 1 },
  { id: 3, name: 'Finance', description: 'Accounting, payroll, and financial operations', employee_count: 1 },
  { id: 4, name: 'Customer Success', description: 'Client support and account management', employee_count: 1 }
];

export const MOCK_EMPLOYEES: Employee[] = [
  { id: 1, employee_id: 'EMP-1001', first_name: 'Aarav', last_name: 'Sharma', email: 'aarav.sharma@example.com', phone: '+91 98765 10001', position: 'Senior Software Engineer', department: 1, hire_date: '2026-05-04', salary: 125000, is_active: true },
  { id: 2, employee_id: 'EMP-1002', first_name: 'Maya', last_name: 'Patel', email: 'maya.patel@example.com', phone: '+91 98765 10002', position: 'Frontend Specialist', department: 1, hire_date: '2026-06-15', salary: 110000, is_active: true },
  { id: 3, employee_id: 'EMP-1003', first_name: 'Rohan', last_name: 'Verma', email: 'rohan.verma@example.com', phone: '+91 98765 10003', position: 'Backend Engineer', department: 1, hire_date: '2026-07-01', salary: 105000, is_active: true },
  { id: 4, employee_id: 'EMP-1004', first_name: 'Ananya', last_name: 'Reddy', email: 'ananya.reddy@example.com', phone: '+91 98765 10004', position: 'HR Business Partner', department: 2, hire_date: '2026-04-10', salary: 98000, is_active: true },
  { id: 5, employee_id: 'EMP-1005', first_name: 'Vikram', last_name: 'Singh', email: 'vikram.singh@example.com', phone: '+91 98765 10005', position: 'Financial Analyst', department: 3, hire_date: '2026-03-20', salary: 102000, is_active: true },
  { id: 6, employee_id: 'EMP-1006', first_name: 'Diya', last_name: 'Nair', email: 'diya.nair@example.com', phone: '+91 98765 10006', position: 'Customer Success Lead', department: 4, hire_date: '2026-08-01', salary: 95000, is_active: true }
];

export const MOCK_ATTENDANCE: Attendance[] = [
  { id: 1, employee: 1, employee_id: 'EMP-1001', employee_name: 'Aarav Sharma', date: '2026-10-31', check_in: '09:00:00', check_out: '17:30:00', status: 'present' },
  { id: 2, employee: 2, employee_id: 'EMP-1002', employee_name: 'Maya Patel', date: '2026-10-31', check_in: '09:00:00', check_out: '17:30:00', status: 'present' },
  { id: 3, employee: 3, employee_id: 'EMP-1003', employee_name: 'Rohan Verma', date: '2026-10-31', check_in: '09:00:00', check_out: '18:00:00', status: 'late' },
  { id: 4, employee: 4, employee_id: 'EMP-1004', employee_name: 'Ananya Reddy', date: '2026-10-31', check_in: undefined, check_out: undefined, status: 'absent' },
  { id: 5, employee: 5, employee_id: 'EMP-1005', employee_name: 'Vikram Singh', date: '2026-10-31', check_in: undefined, check_out: undefined, status: 'leave' },
  { id: 6, employee: 6, employee_id: 'EMP-1006', employee_name: 'Diya Nair', date: '2026-10-31', check_in: '09:00:00', check_out: '17:30:00', status: 'present' }
];

export const MOCK_DASHBOARD: Dashboard = {
  total_employees: 6,
  active_employees: 6,
  total_departments: 4,
  present_today: 3,
  late_today: 1,
  absent_today: 1,
  leave_today: 1,
  attendance_rate: 66.7,
  department_breakdown: [
    { id: 1, name: 'Engineering', employee_count: 3 },
    { id: 2, name: 'People Operations', employee_count: 1 },
    { id: 3, name: 'Finance', employee_count: 1 },
    { id: 4, name: 'Customer Success', employee_count: 1 }
  ],
  weekly_attendance: [
    { date: '2026-10-25', present: 5, late: 0, absent: 1, leave: 0 },
    { date: '2026-10-26', present: 6, late: 0, absent: 0, leave: 0 },
    { date: '2026-10-27', present: 5, late: 1, absent: 0, leave: 0 },
    { date: '2026-10-28', present: 4, late: 1, absent: 1, leave: 0 },
    { date: '2026-10-29', present: 6, late: 0, absent: 0, leave: 0 },
    { date: '2026-10-30', present: 5, late: 0, absent: 0, leave: 1 },
    { date: '2026-10-31', present: 3, late: 1, absent: 1, leave: 1 }
  ],
  recent_attendance: MOCK_ATTENDANCE
};

export const MOCK_LEAVE_REQUESTS: LeaveRequest[] = [
  { id: 1, employee: 5, employee_name: 'Vikram Singh', leave_type: 'Annual Leave', start_date: '2026-10-31', end_date: '2026-11-02', reason: 'Family vacation', status: 'Approved' },
  { id: 2, employee: 3, employee_name: 'Rohan Verma', leave_type: 'Sick Leave', start_date: '2026-11-05', end_date: '2026-11-06', reason: 'Medical appointment', status: 'Pending' }
];

export const MOCK_SHIFTS: Shift[] = [
  { id: 1, name: 'General Shift', start_time: '09:00:00', end_time: '18:00:00', grace_minutes: 15 },
  { id: 2, name: 'Early Shift', start_time: '07:00:00', end_time: '16:00:00', grace_minutes: 15 }
];

export const MOCK_TIMESHEETS: Timesheet[] = [
  { id: 1, employee: 1, date: '2026-10-31', shift: 'General Shift', hours: 8.5, status: 'Approved' },
  { id: 2, employee: 2, date: '2026-10-31', shift: 'General Shift', hours: 8.5, status: 'Submitted' }
];

export const MOCK_PAYROLL: PayrollRecord[] = [
  { id: 1, employee: 1, period: 'October 2026', gross_pay: 125000, deductions: 12500, net_pay: 112500, status: 'Processed' },
  { id: 2, employee: 2, period: 'October 2026', gross_pay: 110000, deductions: 11000, net_pay: 99000, status: 'Processed' }
];

export const MOCK_DOCUMENTS: EmployeeDocument[] = [
  { id: 1, employee: 1, document_type: 'Passport / ID', name: 'Identity Proof.pdf', expires_on: '2030-12-31', status: 'Verified' },
  { id: 2, employee: 2, document_type: 'Employment Contract', name: 'Contract_Maya_Patel.pdf', status: 'Active' }
];

export const MOCK_AUDIT: AuditEntry[] = [
  { id: 1, actor: 'user', action: 'Sign In', resource: 'Authentication', created_at: '2026-10-31T22:30:00Z', details: 'User signed in successfully' },
  { id: 2, actor: 'user', action: 'Approve Leave', resource: 'Leave Request #1', created_at: '2026-10-31T20:15:00Z', details: 'Annual Leave approved' }
];
