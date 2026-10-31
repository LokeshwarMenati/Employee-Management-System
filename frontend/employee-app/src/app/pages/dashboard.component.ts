import { Component, inject } from '@angular/core';
import { DatePipe, NgFor, NgIf, UpperCasePipe } from '@angular/common';
import { ApiService } from '../core/api.service';
import { Dashboard } from '../core/models';

@Component({
  standalone: true,
  imports: [NgFor, NgIf, DatePipe, UpperCasePipe],
  template: `
    <div class="page-head dashboard-head">
      <div>
        <div class="eyebrow">{{today | date:'EEEE, MMMM d, y' | uppercase}}</div>
        <h1>Good morning, <span>team.</span></h1>
        <p class="muted">Here is what is happening across your organisation today.</p>
      </div>
      <a class="primary" href="/attendance">+ Record attendance</a>
    </div>

    <div class="stats" *ngIf="data">
      <div class="stat stat-blue"><div class="stat-icon">♙</div><div><strong>{{data.total_employees || 0}}</strong><span>Active employees</span><small>+8.2% this month</small></div></div>
      <div class="stat stat-purple"><div class="stat-icon">▤</div><div><strong>{{data.total_departments || 0}}</strong><span>Departments</span><small>Across the organisation</small></div></div>
      <div class="stat stat-green"><div class="stat-icon">✓</div><div><strong>{{data.attendance_rate || 0}}%</strong><span>Attendance rate</span><small>{{data.present_today || 0}} present today</small></div></div>
      <div class="stat stat-orange"><div class="stat-icon">◷</div><div><strong>{{data.late_today || 0}}</strong><span>Late arrivals</span><small>Needs attention today</small></div></div>
    </div>

    <div class="dashboard-grid">
      <div class="panel analytics-panel">
        <div class="panel-head"><div><h2>Attendance overview</h2><p class="muted">Last 7 days performance</p></div><span class="period-pill">This week ▾</span></div>
        <div class="chart">
          <div class="chart-y"><span>6</span><span>4</span><span>2</span><span>0</span></div>
          <div class="bars"><div class="bar-group" *ngFor="let day of data?.weekly_attendance"><div class="bar-stack"><i class="bar present-bar" [style.height.%]="height(day.present)"></i><i class="bar late-bar" [style.height.%]="height(day.late)"></i></div><span>{{day.date | date:'EEE'}}</span></div></div>
        </div>
        <div class="legend"><span><i class="legend-dot present-dot"></i>Present</span><span><i class="legend-dot late-dot"></i>Late</span></div>
      </div>
      <div class="panel distribution-panel">
        <div class="panel-head"><div><h2>Team distribution</h2><p class="muted">People by department</p></div></div>
        <div class="distribution" *ngFor="let department of data?.department_breakdown">
          <div class="distribution-label"><span>{{department.name}}</span><strong>{{department.employee_count}}</strong></div>
          <div class="progress"><i [style.width.%]="departmentWidth(department.employee_count)"></i></div>
        </div>
        <a class="text-link" href="/departments">Manage departments →</a>
      </div>
    </div>

    <div class="panel activity-panel">
      <div class="panel-head"><div><h2>Recent attendance</h2><p class="muted">Latest activity from your team</p></div><a class="text-link" href="/attendance">View all →</a></div>
      <div class="table-wrap"><table><thead><tr><th>Employee</th><th>Date</th><th>Status</th><th>Check in</th><th>Check out</th></tr></thead><tbody><tr *ngFor="let a of data?.recent_attendance"><td><div class="employee-cell"><span class="mini-avatar">{{initial(a.employee_name || a.employee)}}</span><strong>{{name(a.employee_name || a.employee)}}</strong></div></td><td>{{a.date|date:'MMM d, y'}}</td><td><span class="badge" [class]="a.status.toLowerCase()">{{a.status}}</span></td><td>{{a.check_in||'—'}}</td><td>{{a.check_out||'—'}}</td></tr><tr *ngIf="!data?.recent_attendance?.length"><td colspan="5" class="empty">No recent attendance records.</td></tr></tbody></table></div>
    </div>
  `
})
export class DashboardComponent {
  api = inject(ApiService);
  data: Dashboard | null = null;
  today = new Date();
  ngOnInit() { this.api.dashboard().subscribe({ next: d => this.data = d, error: () => this.data = {} }); }
  height(value: number) { return Math.min(100, Math.max(8, value * 15)); }
  departmentWidth(value: number) { return Math.min(100, value * 30 + 8); }
  name(employee: any) { return typeof employee === 'object' ? `${employee?.first_name || ''} ${employee?.last_name || ''}`.trim() || 'Unknown employee' : String(employee || 'Unknown employee'); }
  initial(employee: any) { return this.name(employee).charAt(0).toUpperCase(); }
}
