// カメラクラス
class Camera {
  constructor(conversionRate) {
    this.position = { x: 0, y: 0 }; // カメラの位置（CAD座標系）
    this.scale = 1; // スケール
    this.conversionRate = conversionRate; // mmからpxへの変換率
    // console.log("conversionRate = ", conversionRate);
  }

  // CAD座標系からCanvas座標系への変換行列
  // X方向にズーム
  // Y方向にズーム（反転）
  // カメラの位置に応じた平行移動
  toCanvas(x, y) {
    const matrix = [
      [this.scale * this.conversionRate, 0,          -this.position.x * this.scale * this.conversionRate],
      [0,          -this.scale * this.conversionRate, this.position.y * this.scale * this.conversionRate]
    ];
    const newX = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2];
    const newY = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2];
    return { x: newX, y: newY };
  }

  // Canvas座標系からCAD座標系への変換行列
  // X方向のズームの逆変換
  // Y方向のズームの逆変換（反転）
  // 平行移動の逆変換
  toCAD(x, y, isDelta = false) {
    if (isDelta) {
      return {
        x: x / (this.scale * this.conversionRate),
        y: -y / (this.scale * this.conversionRate)
      };
    }
    
    const invScale = 1 / (this.scale * this.conversionRate);
    const matrix = [
      [invScale, 0,        this.position.x],
      [0,        -invScale, this.position.y]
    ];
    const newX = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2];
    const newY = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2];
    return { x: newX, y: newY };
  }

  move(dx, dy) {
    // カメラの移動
    this.position.x += dx;
    this.position.y += dy;
  }

  zoomIn(factor, mouseX, mouseY) {
    const beforeZoomCAD = this.toCAD(mouseX, mouseY);
    this.scale *= factor;
    const afterZoomCAD = this.toCAD(mouseX, mouseY);
    this.move(beforeZoomCAD.x - afterZoomCAD.x, beforeZoomCAD.y - afterZoomCAD.y);
  }

  zoomOut(factor, mouseX, mouseY) {
    const beforeZoomCAD = this.toCAD(mouseX, mouseY);
    this.scale /= factor;
    const afterZoomCAD = this.toCAD(mouseX, mouseY);
    this.move(beforeZoomCAD.x - afterZoomCAD.x, beforeZoomCAD.y - afterZoomCAD.y);
  }
}

// =================================================================================

// 再描画関数
function draw() {
  console.log("I'm in draw().");

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // グリッド線の描画
  drawGrid(ctx);

  // キャッシュから描画（ちらつき防止）
  drawShapesFromCache();

  // バックエンドから全て図形情報を取得し、描画
  getShapesFromBackend();

  // CAD座標系の表示
  displayCADCoordinates();

}


function drawGrid(ctx) {
  console.log("I'm in drawGrid().");

  // グリッド線の間隔（CAD座標系上の100mm）
  const gridSpacing = 100;

  // Canvasの左上と右下のCAD座標
  const leftTopCAD = camera.toCAD(0, 0);
  const rightBottomCAD = camera.toCAD(canvas.width, canvas.height);

  // 通常のグリッド線の描画（薄いグレー）
  ctx.strokeStyle = 'lightgrey';
  drawGridLines(ctx, leftTopCAD, rightBottomCAD, gridSpacing);

  // X=0とY=0のグリッド線の描画（濃い黒）
  ctx.strokeStyle = 'black';
  drawAxisLine(ctx, leftTopCAD, rightBottomCAD, 0, true); // X=0
  drawAxisLine(ctx, leftTopCAD, rightBottomCAD, 0, false); // Y=0
}



function drawGridLines(ctx, leftTopCAD, rightBottomCAD, gridSpacing) {
  console.log("I'm in drawGridLines()");

  // X方向のグリッド線
  for (let x = Math.floor(leftTopCAD.x / gridSpacing) * gridSpacing; x <= rightBottomCAD.x; x += gridSpacing) {
    const start = camera.toCanvas(x, leftTopCAD.y);
    const end = camera.toCanvas(x, rightBottomCAD.y);
    ctx.beginPath();
    ctx.moveTo(start.x, start.y);
    ctx.lineTo(end.x, end.y);
    ctx.stroke();
  }

  // Y方向のグリッド線
  for (let y = Math.floor(rightBottomCAD.y / gridSpacing) * gridSpacing; y <= leftTopCAD.y; y += gridSpacing) {
    const start = camera.toCanvas(leftTopCAD.x, y);
    const end = camera.toCanvas(rightBottomCAD.x, y);
    ctx.beginPath();
    ctx.moveTo(start.x, start.y);
    ctx.lineTo(end.x, end.y);
    ctx.stroke();
  }
}



function drawAxisLine(ctx, leftTopCAD, rightBottomCAD, value, isXAxis) {
  console.log("I'm in drawAxisLine()");
  const start = isXAxis ? camera.toCanvas(value, leftTopCAD.y) : camera.toCanvas(leftTopCAD.x, value);
  const end = isXAxis ? camera.toCanvas(value, rightBottomCAD.y) : camera.toCanvas(rightBottomCAD.x, value);
  ctx.beginPath();
  ctx.moveTo(start.x, start.y);
  ctx.lineTo(end.x, end.y);
  ctx.stroke();
}


// Canvas要素の現在のスケールを表示する
// Canvas要素の左上と右下がCAD座標系においてどこなのかをHTML上に表示する
function displayCADCoordinates() {
  console.log("I'm in displayCADCoordinates()");
  let canvas = document.getElementById('myCanvas');

  // Canvasの左上と右下の座標
  const leftTopCanvas = { x: 0, y: 0 };
  const rightBottomCanvas = { x: canvas.width, y: canvas.height };

  // CAD座標系への変換
  const leftTopCAD = camera.toCAD(leftTopCanvas.x, leftTopCanvas.y);
  const rightBottomCAD = camera.toCAD(rightBottomCanvas.x, rightBottomCanvas.y);

  // 小数点以下3桁にフォーマット
  const leftTopX = leftTopCAD.x.toFixed(3);
  const leftTopY = leftTopCAD.y.toFixed(3);
  const rightBottomX = rightBottomCAD.x.toFixed(3);
  const rightBottomY = rightBottomCAD.y.toFixed(3);
  const currentScale = camera.scale.toFixed(3);

  // HTMLに表示
  document.getElementById('leftTop').innerText = `Left Top Coordinate: (${leftTopX}, ${leftTopY})`;
  document.getElementById('rightBottom').innerText = `Right Bottom Coordinate: (${rightBottomX}, ${rightBottomY})`;
  document.getElementById('scale').innerText = `Current Scale: ${currentScale}`;
}


function sendShapeToBackend(shape, cadCoordinates) {
    console.log("I'm in sendShapeToBackend()");

    // Ajaxを使用してバックエンドにPOSTリクエストを送信
    fetch('/add_shape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ shape: shape, coordinates: cadCoordinates }),
    });
}


function getShapesFromBackend() {
  console.log("I'm in getShapesFromBackend()");
  //console.trace();

  fetch('/get_shapes')
    .then(response => response.json())
    .then(data => {
      shapesCache = data; // ローカルキャッシュに保存
      console.log(shapesCache);
      drawShapesFromCache(); // キャッシュから描画
    });
}


function drawShapesFromCache() {
  console.log("I'm in drawShapesFromCache()");
  console.trace();
  console.log(shapesCache);

  shapesCache.forEach(shape => {
    if (shape.type === 'Point') {
      // 点を描画
      const canvasCoordinates = camera.toCanvas(shape.x, shape.y);
      ctx.beginPath();
      ctx.arc(canvasCoordinates.x, canvasCoordinates.y, 5, 0, 2 * Math.PI);
      ctx.fill();
    } else if (shape.type === 'Line') {
      // 線を描画
      const p1CanvasCoordinates = camera.toCanvas(shape.p1.x, shape.p1.y);
      const p2CanvasCoordinates = camera.toCanvas(shape.p2.x, shape.p2.y);
      ctx.beginPath();
      ctx.moveTo(p1CanvasCoordinates.x, p1CanvasCoordinates.y);
      ctx.lineTo(p2CanvasCoordinates.x, p2CanvasCoordinates.y);
      ctx.stroke();
    }
    // 他の図形の描画もここに追加できます
  });
}

// **************************************************************

// DPIから変換率を計算
//var dpr = window.devicePixelRatio || 1;
//console.log("dpr=",dpr);

// 96DPIは、基準解像度
// 基準解像度に、dprを掛け合わせることで、「１インチあたりの物理ピクセル数」を計算できる
// 例えば、高解像度デバイスを使っていてdpr=1.25の場合、1インチあたり120(=96*125)物理ピクセルになる
// var dpi = dpr * 96;

console.log("script.js was started.#1");

// 「1ミリ当たりの物理ピクセル数」の計算
var dpi = 100;
var conversionRate = dpi / 25.4;

// canvas要素の取得
let canvas = document.getElementById('myCanvas');

// コンテキストのスケールを調整
var ctx = canvas.getContext('2d');

// 描画する図形の種類の取得
const shapeSelect = document.getElementById('shapeSelect');

// Camera
const camera = new Camera(conversionRate);

// バックエンドから取得した図形情報のローカルキャッシュ
let shapesCache = [];

// マウス座標を表示するためのdivを取得
const mouseCoordinatesCanvasDiv = document.getElementById('mouse-coordinates-canvas');
const mouseCoordinatesCadDiv = document.getElementById('mouse-coordinates-cad');

console.log("script.js was started.#2");
draw();

// **************************************************************
// 以下、イベントリスナー

// 線の始点と終点を保存する変数を追加
let p1Point = null;
let p2Point = null;

// マウス左クリックイベントのリスナー
canvas.addEventListener('click', (event) => {
    // shapeの選択
    const shape = shapeSelect.value;

    //// 共通のマウス位置取得処理
    // canvasの絶対位置を一度取得して変数に格納
    const rect = canvas.getBoundingClientRect();
    // canvas内での相対座標を計算
    const canvasX = event.clientX - rect.left;
    const canvasY = event.clientY - rect.top;
    // canvas座標をCAD座標に変換
    const cadCoordinates = camera.toCAD(canvasX, canvasY);
    
    if (shape === 'Point') {
        // 点の描画
        sendShapeToBackend(shape, cadCoordinates);
    } else if (shape === 'Line') {
        if (p1Point === null) {
            // 始点を設定
            p1Point = cadCoordinates;
        } else {
            // 終点を設定
            p2Point = cadCoordinates;

            // ここでバックエンドに線の始点と終点を送信
            sendShapeToBackend(shape, {p1: p1Point, p2: p2Point});

            // 始点と終点をリセット
            p1Point = null;
            p2Point = null;
        }
    }
    // ここでバックエンドに送信
    //sendShapeToBackend(shape, cadCoordinates);

    // 描画
    draw();
});


// ズームイン、ズームアウト
canvas.addEventListener('wheel', (event) => {

  // イベントのデフォルト動作（スクロール）を無効化
  event.preventDefault();

  const rect = canvas.getBoundingClientRect();
  const mouseX = event.clientX - rect.left;
  const mouseY = event.clientY - rect.top;

  if (event.deltaY < 0) {
    camera.zoomOut(1.1, mouseX, mouseY);
  } else {
    camera.zoomIn(1.1, mouseX, mouseY);
  }
  draw(); // 再描画
}, { passive: false }); // passiveオプションをfalseに設定して、preventDefaultが効くようにします。


let isDragging = false;
let lastMousePosition = null;


// 右クリックでのドラッグ開始
canvas.addEventListener('mousedown', (event) => {
  if (event.button === 2) { // 右クリック
    isDragging = true;

    // Canvas要素に対する相対座標を取得する
    const rect = canvas.getBoundingClientRect();
    lastMousePosition = { x: event.clientX - rect.left, y: event.clientY - rect.top };
  }
});


// ドラッグ中のマウス移動
canvas.addEventListener('mousemove', (event) => {
  // canvasの絶対位置を取得
  const rect = canvas.getBoundingClientRect();

  // canvas内での相対座標を計算
  const canvasX = event.clientX - rect.left;
  const canvasY = event.clientY - rect.top;

  // CAD座標上での座標を計算
  const cadCoordinates = camera.toCAD(canvasX, canvasY);
  
  // 座標をHTMLに出力
  mouseCoordinatesCanvasDiv.innerHTML = `Canvas X: ${canvasX}, Canvas Y: ${canvasY}`;
  mouseCoordinatesCadDiv.innerHTML = `Cad X: ${cadCoordinates.x.toFixed(3)}, Cad Y: ${cadCoordinates.y.toFixed(3)}`;


  if (isDragging) {
    // Canvas座標系上でのマウスの移動量
    const dxCanvas = canvasX - lastMousePosition.x;
    const dyCanvas = canvasY - lastMousePosition.y;

    // CAD座標系上での移動量に変換
    const movementCAD = camera.toCAD(-dxCanvas, -dyCanvas, true);

    // カメラを移動
    camera.move(movementCAD.x, movementCAD.y);

    // マウス位置の更新
    lastMousePosition = { x: canvasX, y: canvasY };

    // 再描画
    draw();
  }
});

// ドラッグ終了
canvas.addEventListener('mouseup', (event) => {
  if (event.button === 2) { // 右クリック
    isDragging = false;
  }
});

// 右クリックメニューの無効化
canvas.addEventListener('contextmenu', (event) => {
  event.preventDefault();
});

// **************************************************************

// 初期データ（CAD座標系で定義）
//let data = {
//    a: {x: 300, y: 300},
//    b: {x: 300, y: 500},
//    c: {x: 500, y: 400},
//    d: {x: 500, y: 300},
//    displacement: [0, 0]
//};

// マウスの動きを検出
//canvas.addEventListener('mousemove', (event) => {
//    // マウスの座標を取得
//    let mouseX = event.clientX - canvas.offsetLeft;
//    let mouseY = event.clientY - canvas.offsetTop;
//
//    // 座標変換を適用
//    let { x : transformed_mouse_x, y : transformed_mouse_y } = transformCoordinatesToCAD(mouseX, mouseY);
//
//    // c点とマウスカーソルの位置との相対位置を計算
//    data.displacement[0] = transformed_mouse_x - data.c.x;
//    data.displacement[1] = transformed_mouse_y - data.c.y;
//    // console.log( data.displacement[0] );
//    // console.log( data.displacement[1] );
//
//    // /optimize エンドポイントにデータを送信
//    fetch('/optimize', {
//        method: 'POST',
//        headers: { 'Content-Type': 'application/json' },
//        body: JSON.stringify(data)
//    })
//    .then(response => response.json())
//    .then(r_data => {
//        // 最適化後の新しい座標を取得
//        let newCoordinates = r_data;
//
//        // canvasをクリア
//        ctx.clearRect(0, 0, canvas.width, canvas.height);
//        
//        // canvas座標系に変換
//        let transformed_newCoordinates = {
//            a : transformCoordinatesToCanvas( newCoordinates.a.x, newCoordinates.a.y ),
//            b : transformCoordinatesToCanvas( newCoordinates.b.x, newCoordinates.b.y ),
//            c : transformCoordinatesToCanvas( newCoordinates.c.x, newCoordinates.c.y ),
//            d : transformCoordinatesToCanvas( newCoordinates.d.x, newCoordinates.d.y )
//        };
//        // console.log(transformed_newCoordinates)
//
//        // 新しい座標をcanvasに描画
//        ctx.beginPath();
//        ctx.moveTo( transformed_newCoordinates.a.x, transformed_newCoordinates.a.y);
//        ctx.lineTo( transformed_newCoordinates.b.x, transformed_newCoordinates.b.y);
//        ctx.lineTo( transformed_newCoordinates.c.x, transformed_newCoordinates.c.y);
//        ctx.lineTo( transformed_newCoordinates.d.x, transformed_newCoordinates.d.y);
//        ctx.lineTo( transformed_newCoordinates.a.x, transformed_newCoordinates.a.y);
//        ctx.stroke();
//    })
//    .catch((error) => {
//        console.error('Error:', error);
//    });
//});

// CAD座標系に座標変換する関数
//function transformCoordinatesToCAD(x, y) {
//  // console.log("x=", x );
//  // console.log("y=", y);
//
//  // ここで座標変換のロジックを実装
//  let transformed_x = x / 2; // 例: x座標を半分に
//  let transformed_y = y / 2; // 例: y座標を半分に
//  // console.log("transformed_x=", transformed_x);
//  // console.log("transformed_y=", transformed_y);
//
//  return { x : transformed_x, y : transformed_y };
//}

// Canvas座標系に座標変換する関数
//function transformCoordinatesToCanvas(x, y) {
//  let transformed_x = x * 2; // 例: x座標を2倍
//  let transformed_y = y * 2; // 例: y座標を2倍
//  return { x : transformed_x, y : transformed_y };
//}