import { Drawable,Line,Circle } from "./drawable.js";

// このクラスは、キャンバスの描画コンテキストとカメラを受け取り、オブジェクトを描画します。
export class Renderer {
    constructor(canvasRenderingContext, camera) {
        this.context = canvasRenderingContext;
        this.camera = camera;
    }

    renderObject(object) {
        if (object instanceof Line) {
            const screenStart = this.camera.transform.worldToScreen(object.start, this.camera);
            const screenEnd = this.camera.transform.worldToScreen(object.end, this.camera);

            this.context.beginPath();
            this.context.moveTo(screenStart.x, screenStart.y);
            this.context.lineTo(screenEnd.x, screenEnd.y);
            this.context.stroke();
        } else if (object instanceof Circle) {
            const screenCenter = this.camera.transform.worldToScreen(object.center, this.camera);

            this.context.beginPath();
            this.context.arc(screenCenter.x, screenCenter.y, object.radius * this.camera.transform.scale, 0, 2 * Math.PI);
            this.context.stroke();
        }
        // ... handle other drawable types ...
    }
}