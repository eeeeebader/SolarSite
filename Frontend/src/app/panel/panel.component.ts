import { Component, OnInit } from '@angular/core'
import { PanelsService } from '../panels.service'
import { Panel } from '../panel.interface'
import {CommonModule} from "@angular/common";

@Component({
  selector: 'app-panel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './panel.component.html',
  styleUrl: './panel.component.scss'
})
export class PanelComponent implements OnInit {
  panel: Panel[] = [];

  constructor(private panelsService: PanelsService) {}

  ngOnInit(): void {
    this.panelsService.getPanels().subscribe((panels:any) => {
      this.panel = panels;
      console.log(panels);
    });
  }
}
