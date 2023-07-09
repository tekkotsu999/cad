export class Vector {
  constructor(x, y) {
      this.x = x;
      this.y = y;
  }

  distanceTo(other) {
    const dx = other.x - this.x;
    const dy = other.y - this.y;
    return Math.sqrt(dx * dx + dy * dy);
}
}