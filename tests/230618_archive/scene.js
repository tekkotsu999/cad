import { Camera } from "./camera.js";
import { World } from "./world.js";
import { Renderer } from "./renderer.js";

// シーンを表すクラス
// world, camera, rendererを管理する
export class Scene {
    constructor(canvasRenderingContext) {
        this.context = canvasRenderingContext;
        this.camera = new Camera;
        this.world = new World;
        this.renderer = new Renderer(this.context, this.camera);
    }

    renderScene() {
        const objects = this.world.getObjects();
        for (let obj of objects) {
            this.renderer.renderObject(obj);
        }
    }
}