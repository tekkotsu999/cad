import { Vector } from './vector.js';

export class Drawable {
  constructor() {
      this.position = new Vector(0, 0); // World coordinates
  }
}

export class Line extends Drawable {
  constructor(start, end) {
      super();
      this.start = start; // World coordinates
      this.end = end; // World coordinates
  }
}

export class Circle extends Drawable {
  constructor(center, radius) {
      super();
      this.center = center; // World coordinates
      this.radius = radius;
  }
}