// カメラクラス
class Camera {
  constructor() {
    this.position = { x: 0, y: 0 }; // カメラの位置
    this.zoom = 1; // ズームレベル
  }

  // CAD座標系からCanvas座標系への変換行列
  // X方向にズーム
  // Y方向にズーム（反転）
  // カメラの位置に応じた平行移動
  toCanvas(x, y) {
    const matrix = [
      [this.zoom, 0,          -this.position.x * this.zoom],
      [0,         -this.zoom,  this.position.y * this.zoom]
    ];
    const newX = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2];
    const newY = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2];
    return { x: newX, y: newY };
  }

  // Canvas座標系からCAD座標系への変換行列
  // X方向のズームの逆変換
  // Y方向のズームの逆変換（反転）
  // 平行移動の逆変換
  toCAD(x, y) {
    const invZoom = 1 / this.zoom;
    const matrix = [
      [invZoom, 0,        this.position.x],
      [0,       -invZoom, this.position.y]
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
    this.zoom *= factor;
    const afterZoomCAD = this.toCAD(mouseX, mouseY);
    this.move(beforeZoomCAD.x - afterZoomCAD.x, beforeZoomCAD.y - afterZoomCAD.y);
  }

  zoomOut(factor, mouseX, mouseY) {
    const beforeZoomCAD = this.toCAD(mouseX, mouseY);
    this.zoom /= factor;
    const afterZoomCAD = this.toCAD(mouseX, mouseY);
    this.move(beforeZoomCAD.x - afterZoomCAD.x, beforeZoomCAD.y - afterZoomCAD.y);
  }
}


// canvas要素の取得
let canvas = document.getElementById('myCanvas');
let ctx = canvas.getContext('2d');

// Camera
const camera = new Camera();

// CAD座標系の点を例として
const cadPoint = { x: 30, y: 20 };


// 再描画関数
function draw() {
  //let canvas = document.getElementById('myCanvas');
  //let ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  //const camera = new Camera();

  // CAD座標系の点を例として
  // const cadPoint = { x: 30, y: 20 };

  // グリッド線の描画
  drawGrid(ctx);

  // 描画関数内で変換
  const canvasPoint = camera.toCanvas(cadPoint.x, cadPoint.y);

  // 描画
  ctx.beginPath();
  ctx.arc(canvasPoint.x, canvasPoint.y, 5, 0, 2 * Math.PI);
  ctx.fill();

  // CAD座標系の表示
  displayCADCoordinates();

}



function drawGrid(ctx) {
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
  const start = isXAxis ? camera.toCanvas(value, leftTopCAD.y) : camera.toCanvas(leftTopCAD.x, value);
  const end = isXAxis ? camera.toCanvas(value, rightBottomCAD.y) : camera.toCanvas(rightBottomCAD.x, value);
  ctx.beginPath();
  ctx.moveTo(start.x, start.y);
  ctx.lineTo(end.x, end.y);
  ctx.stroke();
}

// ズームイン、ズームアウト
canvas.addEventListener('wheel', (event) => {
  const rect = canvas.getBoundingClientRect();
  const mouseX = event.clientX - rect.left;
  const mouseY = event.clientY - rect.top;

  if (event.deltaY < 0) {
    camera.zoomIn(1.1, mouseX, mouseY);
  } else {
    camera.zoomOut(1.1, mouseX, mouseY);
  }
  draw(); // 再描画
});


// Canvas要素の左上と右下がCAD座標系においてどこなのかをHTML上に表示する
function displayCADCoordinates() {
  let canvas = document.getElementById('myCanvas');

  // Canvasの左上と右下の座標
  const leftTopCanvas = { x: 0, y: 0 };
  const rightBottomCanvas = { x: canvas.width, y: canvas.height };

  // CAD座標系への変換
  const leftTopCAD = camera.toCAD(leftTopCanvas.x, leftTopCanvas.y);
  const rightBottomCAD = camera.toCAD(rightBottomCanvas.x, rightBottomCanvas.y);

  // HTMLに表示
  document.getElementById('leftTop').innerText = `Left Top Coordinate: (${leftTopCAD.x}, ${leftTopCAD.y})`;
  document.getElementById('rightBottom').innerText = `Right Bottom Coordinate: (${rightBottomCAD.x}, ${rightBottomCAD.y})`;
}


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