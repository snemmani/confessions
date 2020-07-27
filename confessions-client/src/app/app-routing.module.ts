import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ConfessionHomeComponent } from './confession-home/confession-home.component';

const routes: Routes = [
  {path: 'confession', component: ConfessionHomeComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
