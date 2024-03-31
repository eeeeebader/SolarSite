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
  public sumDaily: number = 0;
  public sumTotal: number = 0;
  public activatedPanel: Panel | null = null;

  //private ctx: CanvasRenderingContext2D | null = null;

  constructor(private panelsService: PanelsService) {}

  ngOnInit(): void {
    this.panelsService.getPanels().subscribe((panels:any) => {
      this.panels = panels;
      this.interpolateDaily();
      this.sumDaily = this.sumUpDaily(panels);
      this.sumTotal = this.sumUpTotal(panels);
    });
  }

  ngAfterViewInit(): void {
    //this.drawCanvas();
  }

  /* this function does temporal interpolation of the daily yield values, because of an tracking error on the solar panels */
  interpolateDaily(): void {
    this.panels.forEach((panel: Panel) => {
      let dailyYieldW: number = 0;
      let totalYieldW: number = 0;
      let lastYield: number = 0;
      let lastTimestamp: number = 0;

      panel.todaysYieldsW?.forEach((yieldEntry, index) => {
        if (index == 0) {
          lastYield = yieldEntry.yield;
          // convert yieldEntry.date; to timestamp
          lastTimestamp = Date.parse(yieldEntry.date);
          dailyYieldW += yieldEntry.yield;
          totalYieldW += yieldEntry.yield;
        } else {
          let timeDiff = Date.parse(yieldEntry.date) - lastTimestamp;
          let yieldDiff = yieldEntry.yield - lastYield;
          let dailyYield = yieldDiff / timeDiff * 1000 * 60 * 60 * 24;
          dailyYieldW += dailyYield;
          totalYieldW += yieldEntry.yield;
          lastYield = yieldEntry.yield;
          lastTimestamp = Date.parse(yieldEntry.date);
        }
      });
      panel.dailyYieldW = dailyYieldW;
      panel.totalYieldW = totalYieldW;
    });
  }

  sumUpDaily(pnls: Panel[]): number {
    let sum: number = 0;
    for (let panel of pnls) {
      sum += panel.dailyYieldW;
    }
    return sum;
  }

  sumUpTotal(pnls: Panel[]): number {
    let sum: number = 0;
    for (let panel of pnls) {
      sum += panel.totalYieldW;
    }
    return sum;
  }

  /*
  openPanel(id: string): void {
    this.panelsService.getPanel(id).subscribe((panel:any) => {

      this.activatedPanel = panel;
      this.clearCavnas();
      this.drawYields();
    });
  }

  clearCavnas(): void {
    let ctx = this.ctx;
    if (!ctx) return;

    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
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

    ctx.strokeStyle = '#c9c9c9';
    ctx.lineWidth = 1;
    ctx.fillStyle = '#616161'; // For the text color
    ctx.font = '10px Arial'; // Set the font for the Y-axis labels

    const width = ctx.canvas.width;
    const height = ctx.canvas.height;
    const axisOffsetX = 20; // Offset the X axis 20 pixels to the right
    const labelFrequencyY = 50; // Distance between labels on the Y axis

    for (let j = 0; j < height; j += 25) {
      ctx.beginPath();
      ctx.moveTo(axisOffsetX, j);
      ctx.lineTo(axisOffsetX + width - axisOffsetX, j); // Small line on the Y axis
      ctx.stroke();

      // Draw Y-axis labels every 45 pixels
      if (j % labelFrequencyY === 0) {
        if (j == 0) continue;
        ctx.fillText(`${height - j}`, 0, j + 3); // Adjust text position as needed
      }
    }
  }


  drawYields(): void {
    let ctx = this.ctx;
    if (!ctx == null) return;

    let offsetX = 20;
    const circleRadius = 3; // Adjust the circle radius as needed

    if (this.activatedPanel?.todaysYieldsW?.length) {
      if(!ctx) return;

      // define the color to be #aba0fa and the line thinckness to be 3
      ctx.strokeStyle = '#aba0fa';
      ctx.lineWidth = 3;

      let offsetX = 20;
      let step = ctx.canvas.width / (this.activatedPanel.todaysYieldsW.length - 1);

      ctx.beginPath();
      for(let i = 0; i < this.activatedPanel.todaysYieldsW.length - 1; i++) {
        const x1 = 5 + step * i + offsetX;
        const y1 = ctx.canvas.height - this.activatedPanel.todaysYieldsW[i].yield;
        const x2 = 5 + step * (i + 1) + offsetX;
        const y2 = ctx.canvas.height - this.activatedPanel.todaysYieldsW[i + 1].yield;

        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
      }
      ctx.stroke();

    }
    */

    /* this.activatedPanel?.todaysYieldsW?.forEach((yieldEntry, index) => {
      if(!ctx) return;

      const x = 5 + offsetX; // Start at 5 pixels and move 5 pixels to the right for each entry
      const y = ctx.canvas.height - yieldEntry.yield; // Calculate y position based on the yield value

      ctx.beginPath();
      ctx.arc(x, y, circleRadius, 0, Math.PI * 2);
      ctx.fillStyle = 'black';
      ctx.fill();

      offsetX += 15; // Move to the right for the next circle
    }); */
  // }
}
