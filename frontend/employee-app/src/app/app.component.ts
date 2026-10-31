import { Component, inject } from '@angular/core';
import { NgIf } from '@angular/common';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { AuthService } from './core/auth.service';

@Component({
  selector: 'app-root', standalone: true, imports: [RouterOutlet, RouterLink, RouterLinkActive, NgIf],
  template: `
    <ng-container *ngIf="auth.isAuthenticated(); else public">
      <aside class="sidebar" [class.open]="menu">
        <div class="brand"><span class="brand-mark">E</span><span>EMPLOYEE<span>HUB</span></span></div>
        <div class="workspace-label">WORKSPACE</div>
        <nav>
          <a routerLink="/dashboard" routerLinkActive="active" (click)="menu=false"><b>⌂</b><span>Overview</span></a>
          <ng-container *ngIf="canManage">
            <a routerLink="/employees" routerLinkActive="active" (click)="menu=false"><b>♙</b><span>People & lifecycle</span></a>
            <a routerLink="/attendance" routerLinkActive="active" (click)="menu=false"><b>◷</b><span>Attendance</span></a>
            <a routerLink="/timesheets" routerLinkActive="active" (click)="menu=false"><b>▦</b><span>Shifts & timesheets</span></a>
            <a routerLink="/leave" routerLinkActive="active" (click)="menu=false"><b>✓</b><span>Leave approvals</span></a>
            <a routerLink="/payroll" routerLinkActive="active" (click)="menu=false"><b>▤</b><span>Payroll</span></a>
            <a routerLink="/documents" routerLinkActive="active" (click)="menu=false"><b>▣</b><span>Documents</span></a>
            <a routerLink="/reports" routerLinkActive="active" (click)="menu=false"><b>↗</b><span>Reports & export</span></a>
            <a routerLink="/audit" routerLinkActive="active" (click)="menu=false"><b>◉</b><span>Audit log</span></a>
          </ng-container>
        </nav>
        <div class="sidebar-bottom"><div class="workspace-label">ACCOUNT</div>
          <a routerLink="/self-service" routerLinkActive="active"><b>♙</b><span>My self-service</span></a>
          <a routerLink="/profile" routerLinkActive="active"><b>⚙</b><span>My profile</span></a>
          <button (click)="auth.logout()"><b>↪</b><span>Sign out</span></button>
        </div>
      </aside>
      <main class="main"><header><button class="mobile-menu" (click)="menu=!menu">☰</button><div class="header-title"><span>Workspace</span><strong> / Employee Management</strong></div><div class="user-chip"><span class="status-dot"></span><span class="avatar">{{(auth.user?.first_name||auth.user?.username||'U').charAt(0).toUpperCase()}}</span><span>{{auth.user?.first_name||auth.user?.username}}</span></div></header><section class="content"><router-outlet></router-outlet></section></main>
    </ng-container>
    <ng-template #public><router-outlet></router-outlet></ng-template>
  `
})
export class AppComponent {
  auth = inject(AuthService);
  menu = false;
  get canManage() { const role = (this.auth.user?.role || '').toLowerCase(); return !role || !!this.auth.user?.is_staff || ['admin', 'hr', 'manager'].includes(role); }
}
