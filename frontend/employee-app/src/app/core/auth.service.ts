import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { tap, catchError, of } from 'rxjs';
import { environment } from '../../environments/environment';
import { User } from './models';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private router = inject(Router);
  token = localStorage.getItem('ems_token');
  user: User | null = JSON.parse(localStorage.getItem('ems_user') || 'null');

  login(c: { username: string; password: string }) {
    const creds = {
      username: (c.username || 'user').trim(),
      password: c.password || 'user'
    };

    return this.http.post<{ token: string; user?: User }>(`${environment.apiUrl}/login/`, creds).pipe(
      tap(r => {
        this.token = r.token;
        this.user = r.user || { username: creds.username };
        localStorage.setItem('ems_token', r.token);
        localStorage.setItem('ems_user', JSON.stringify(this.user));
      }),
      catchError(err => {
        // Fallback for demo mode or when running on Vercel without hosted backend
        if (creds.username === 'user' && creds.password === 'user') {
          const demoToken = 'demo-token-6ef8cc6f69cf6b10df0143ba8d8d500c1d54994a';
          const demoUser: User = {
            id: 1,
            username: 'user',
            email: 'user@example.com',
            first_name: 'Demo',
            last_name: 'Admin'
          };
          this.token = demoToken;
          this.user = demoUser;
          localStorage.setItem('ems_token', demoToken);
          localStorage.setItem('ems_user', JSON.stringify(demoUser));
          return of({ token: demoToken, user: demoUser });
        }
        throw err;
      })
    );
  }

  logout() {
    this.http.post(`${environment.apiUrl}/logout/`, {}).pipe(catchError(() => of(null))).subscribe(() => this.clear());
  }

  clear() {
    this.token = null;
    this.user = null;
    localStorage.removeItem('ems_token');
    localStorage.removeItem('ems_user');
    this.router.navigate(['/login']);
  }

  isAuthenticated() {
    return !!this.token;
  }

  profile() {
    return this.http.get<User>(`${environment.apiUrl}/profile/`).pipe(
      tap(u => {
        this.user = u;
        localStorage.setItem('ems_user', JSON.stringify(u));
      }),
      catchError(() => {
        const fallback = this.user || { username: 'user', first_name: 'Demo', last_name: 'Admin' };
        return of(fallback);
      })
    );
  }

  updateProfile(d: Partial<User>) {
    return this.http.patch<User>(`${environment.apiUrl}/profile/`, d).pipe(
      tap(u => {
        this.user = u;
        localStorage.setItem('ems_user', JSON.stringify(u));
      }),
      catchError(() => {
        this.user = { ...(this.user || { username: 'user' }), ...d };
        localStorage.setItem('ems_user', JSON.stringify(this.user));
        return of(this.user as User);
      })
    );
  }

  changePassword(d: { old_password: string; new_password: string }) {
    return this.http.post<{ token: string }>(`${environment.apiUrl}/profile/change-password/`, d).pipe(
      tap(r => {
        this.token = r.token;
        localStorage.setItem('ems_token', r.token);
      }),
      catchError(() => of({ token: this.token || 'demo-token' }))
    );
  }
}
