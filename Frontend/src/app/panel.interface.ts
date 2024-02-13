export interface Panel {
  curYieldW: number;
  dailyYieldW: number;
  serial_number: number;
  totalYieldW: number;
  todaysYieldsW?: YieldsW[];
  dailyYieldsW?: YieldsW[];
}

export interface YieldsW {
  date: string;
  yield: number;
}
