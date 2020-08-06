import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {ConfessionsHomeComponent} from './confessions-home/confessions-home.component';

const routes: Routes = [{path: '', component: ConfessionsHomeComponent}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
