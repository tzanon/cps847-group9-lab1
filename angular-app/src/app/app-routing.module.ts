import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AboutUsComponent } from './about-us/about-us.component';
import { OurCustomersComponent } from './our-customers/our-customers.component';
import { OurServicesComponent } from './our-services/our-services.component';

const routes: Routes = [
  { path: 'aboot-us', component: AboutUsComponent },
  { path: 'our-customers', component: OurCustomersComponent },
  { path: 'our-services', component: OurServicesComponent },
  { path: '', redirectTo: '/aboot-us', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
