import { Component, OnInit, AfterViewInit } from '@angular/core'
import { PanelsService } from '../panels.service'
import { Panel } from '../panel.interface'
import { CommonModule } from "@angular/common";

@Component({
  selector: 'app-panel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './panel.component.html',
  styleUrl: './panel.component.scss'
})
export class PanelComponent implements OnInit, AfterViewInit {

  public panels: Panel[] = [];
  public activatedPanel: Panel | null = null;

  private ctx: CanvasRenderingContext2D | null = null;

  constructor(private panelsService: PanelsService) {}

  ngOnInit(): void {
    this.panelsService.getPanels().subscribe((panels:any) => {
      this.panels = panels;
      console.log(panels);
    });
  }

  ngAfterViewInit(): void {
    this.drawCanvas();
    this.drawAxes();
  }

  openPanel(id: string): void {
    this.panelsService.getPanel(id).subscribe((panel:any) => {

      this.activatedPanel = panel;
      this.clearCavnas();
      this.drawYields();
      console.log(panel);
    });
  }

  clearCavnas(): void {
    let ctx = this.ctx;
    if (!ctx) return;

    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    this.drawCanvas();
    this.drawAxes();
  }

  drawCanvas(): void {
    const canvas = document.getElementById('yieldCanvas') as HTMLCanvasElement;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    this.ctx = ctx;
  }

  drawAxes(): void {
    let ctx = this.ctx;
    if (!ctx) return;

    const width = ctx.canvas.width;
    const height = ctx.canvas.height;

    // Draw X axis
    ctx.beginPath();
    ctx.moveTo(0, height - 1); // Start at the bottom of the canvas
    ctx.lineTo(width, height - 1); // Draw to the right
    ctx.stroke();

    // Draw Y axis
    ctx.beginPath();
    ctx.moveTo(1, 0); // Start at the top of the canvas
    ctx.lineTo(1, height); // Draw downwards
    ctx.stroke();

    // Draw small lines every 5 pixels on the axes
    for (let i = 0; i < width; i += 5) {
      ctx.beginPath();
      ctx.moveTo(i, height - 1);
      ctx.lineTo(i, height - 6); // Small line on the X axis
      ctx.stroke();
    }

    for (let j = 0; j < height; j += 5) {
      ctx.beginPath();
      ctx.moveTo(1, j);
      ctx.lineTo(6, j); // Small line on the Y axis
      ctx.stroke();
    }
  }

  drawYields(): void {
    let ctx = this.ctx;
    if (!ctx == null) return;

    let offsetX = 0;
    const circleRadius = 3; // Adjust the circle radius as needed

    this.activatedPanel?.todaysYieldsW?.forEach((yieldEntry, index) => {
      if(!ctx) return;

      const x = 5 + offsetX; // Start at 5 pixels and move 5 pixels to the right for each entry
      const y = ctx.canvas.height - yieldEntry.yield; // Calculate y position based on the yield value

      ctx.beginPath();
      ctx.arc(x, y, circleRadius, 0, Math.PI * 2);
      ctx.fillStyle = 'black';
      ctx.fill();

      offsetX += 15; // Move to the right for the next circle
    });

    if (this.activatedPanel?.todaysYieldsW?.length) {
      if(!ctx) return;

      ctx.beginPath();
      for(let i = 0; i < this.activatedPanel.todaysYieldsW.length - 1; i++) {
        const x1 = 5 + 15 * i;
        const y1 = ctx.canvas.height - this.activatedPanel.todaysYieldsW[i].yield;
        const x2 = 5 + 15 * (i + 1);
        const y2 = ctx.canvas.height - this.activatedPanel.todaysYieldsW[i + 1].yield;

        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
      }
      ctx.stroke();

    }
  }
}
