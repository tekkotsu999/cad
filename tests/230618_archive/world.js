
// ワールド座標系
// ワールド座標系内にあるオブジェクトを管理する
export class World {
  constructor() {
      this.objects = [];
  }

  addObject(object) {
      this.objects.push(object);
  }

  getObjects() {
      return this.objects;
  }
}