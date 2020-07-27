import { Component, OnInit } from '@angular/core';
import {ConfessionService} from '../confession.service';
import {Confession} from "../models/confession";

@Component({
  selector: 'app-confession-home',
  templateUrl: './confession-home.component.html',
  styleUrls: ['./confession-home.component.scss']
})
export class ConfessionHomeComponent implements OnInit {
  confessions: Confession;
  constructor(private service: ConfessionService) { }

  ngOnInit(): void {
    this.service.getConfessions().subscribe((confessions: Confession) => {
      this.confessions = confessions;
      console.log(confessions);
    });
  }

}
