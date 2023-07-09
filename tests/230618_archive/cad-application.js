import { Scene } from "./scene.js";
import { Line, Circle } from "./drawable.js";
import { Vector } from "./vector.js";

export class CADApplication {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.context = this.canvas.getContext('2d');

    // シーンの初期化
    // このコンストラクタでworld, camera, rendererが生成され、シーンの中で管理される。
    this.scene = new Scene(this.context);
    
    // 状態変数の初期化
    this.drawingMode = "none";
    this.startPoint = null;

    // イベントリスナーの追加
    this.canvas.addEventListener('mousedown', (event) => this.onMouseDown(event));
    this.canvas.addEventListener('mousemove', (event) => this.onMouseMove(event));
  }

  onMouseDown(event) {
    if (this.drawingMode === "none") {
      // 図形の始点を設定
      this.startPoint = this.getMousePosition(event);
      this.drawingMode = "line"; // または "line" など、選択された図形に応じて変更
    } else if (this.drawingMode === "line") {
      // 直線の終点を設定して描画
      const endPoint = this.getMousePosition(event);
      const line = new Line(this.startPoint, endPoint);
      this.scene.world.addObject(line);
      this.scene.renderScene();
      this.drawingMode = "none";
    } else if (this.drawingMode === "circle") {
      // 円の半径を設定して描画
      const endPoint = this.getMousePosition(event);
      const radius = this.startPoint.distanceTo(endPoint);
      const circle = new Circle(this.startPoint, radius);
      this.scene.world.addObject(circle);
      this.scene.renderScene();
      this.drawingMode = "none";
    }
  }

  onMouseMove(event) {
    const context = this.context;
    context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.scene.renderScene(); // 既存の図形を再描画

    const endPoint = this.getMousePosition(event);

    if (this.drawingMode === "line") {
      // マウスの位置に直線を描画
      const tempLine = new Line(this.startPoint, endPoint);
      this.scene.renderer.renderObject(tempLine);
    } else if (this.drawingMode === "circle") {
      // マウスの位置に円を描画
      const radius = this.startPoint.distanceTo(endPoint);
      const tempCircle = new Circle(this.startPoint, radius);
      this.scene.renderer.renderObject(tempCircle);
    }
  }

  getMousePosition(event) {
    const rect = this.canvas.getBoundingClientRect();
    return new Vector(event.clientX - rect.left, event.clientY - rect.top);
  }
}

