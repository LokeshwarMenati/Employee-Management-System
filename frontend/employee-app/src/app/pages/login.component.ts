import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../core/auth.service';
import { NgIf } from '@angular/common';

@Component({
  standalone: true,
  imports: [FormsModule, NgIf],
  template: `
    <div class="login-page">
      <div class="login-card">
        <div class="brand login-brand">
          <span class="brand-mark">E</span><span>EMPLOYEE<span>HUB</span></span>
        </div>
        <h1>Welcome back</h1>
        <p class="muted">Sign in to manage your workforce</p>
        
        <form (ngSubmit)="submit()">
          <label>Username
            <input name="username" [(ngModel)]="form.username" placeholder="user" autocomplete="username">
          </label>
          <label>Password
            <input name="password" type="password" [(ngModel)]="form.password" placeholder="user" autocomplete="current-password">
          </label>
          
          <div class="alert error" *ngIf="error">{{error}}</div>
          
          <button class="primary full" type="submit" [disabled]="loading">
            {{loading ? 'Signing in…' : 'Sign in'}}
          </button>

          <button type="button" class="secondary full" style="margin-top: 10px;" (click)="quickDemoLogin()" [disabled]="loading">
            ⚡ 1-Click Demo Sign In
          </button>
        </form>

        <div style="margin-top: 16px; padding: 12px; border-radius: 8px; background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.2); font-size: 13px; color: #94a3b8; text-align: center;">
          Demo credentials pre-filled: <strong style="color: #60a5fa;">user</strong> / <strong style="color: #60a5fa;">user</strong>
        </div>
      </div>
    </div>
  `
})
export class LoginComponent {
  auth = inject(AuthService);
  router = inject(Router);
  form = { username: 'user', password: 'user' };
  loading = false;
  error = '';

  quickDemoLogin() {
    this.form = { username: 'user', password: 'user' };
    this.submit();
  }

  submit() {
    // If username or password were left empty, automatically use demo credentials
    if (!this.form.username || !this.form.username.trim()) {
      this.form.username = 'user';
    }
    if (!this.form.password) {
      this.form.password = 'user';
    }

    this.loading = true;
    this.error = '';
    this.auth.login(this.form).subscribe({
      next: () => this.router.navigate(['/dashboard']),
      error: e => {
        this.error = e.error?.detail || 'Unable to sign in. Check your credentials.';
        this.loading = false;
      }
    });
  }
}
