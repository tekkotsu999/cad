import { Vector } from './vector.js';

// カメラを表すクラス。ビューポートの位置、スケール、および回転を管理します。Transformクラスを使用して変換を行う
export class Camera {
  constructor() {
      this.transform = new Transform();
  }
}

// 変換（平行移動、回転、スケーリング）を表すクラス。変換行列を管理し、座標変換を行う
class Transform {
  constructor() {
      this.position = new Vector(0, 0);
      this.scale = 1;
  }

  worldToScreen(worldPosition, camera) {
      return new Vector(
          (worldPosition.x - camera.transform.position.x) * camera.transform.scale,
          (worldPosition.y - camera.transform.position.y) * camera.transform.scale
      );
  }
}