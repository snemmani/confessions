import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable, Subscribable} from 'rxjs';
import {Confession} from './models/confession';


@Injectable({
  providedIn: 'root'
})
export class ConfessionService {

  constructor(private httpClient: HttpClient) { }

  public getConfessions(): Observable<Confession> {
    return this.httpClient.get<Confession>('/api/confession');
  }
}
