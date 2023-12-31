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
// 状態（モード）を管理するクラス
class ModeManager {
  constructor() {
    this.currentMode = 'select_mode';  // 初期モードは選択モード
  }

  setMode(newMode) {
    this.currentMode = newMode;
  }

  getMode() {
    return this.currentMode;
  }
}

// =================================================================================

function getShapesFromBackend() {
  //console.log("I'm in getShapesFromBackend()");
  //console.trace();

  // fetch関数で非同期通信を行う
  fetch('/get_shapes')
    // 通信が成功したら、レスポンスをJSON形式に変換
    .then(response => response.json())
    // JSONデータを受け取った後の処理
    .then(data => {
      shapesCache = data; // ローカルキャッシュに保存
      drawShapesFromCache(); // キャッシュから描画
      // console.log('shapesCache:', shapesCache);
    });
}

function drawShapesFromCache() {
  //console.log("I'm in drawShapesFromCache()");
  //console.trace();
  //console.log(shapesCache);

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // グリッド線の描画
  drawGrid(ctx);

  // CAD座標系の表示
  displayCADCoordinates();

  // shapesCacheに格納されているshapeを全て描画
  shapesCache.forEach(shape => {

    if (shape.shape_type === 'Point') {
      // 点を描画

      // 描画色を設定（選択されている場合は水色、それ以外は黒）
      ctx.fillStyle = shape.is_selected ? 'lightblue' : 'black';
      ctx.strokeStyle = shape.is_selected ? 'lightblue' : 'black';

      const canvasCoordinates = camera.toCanvas(shape.x, shape.y);
      ctx.beginPath();
      ctx.arc(canvasCoordinates.x, canvasCoordinates.y, 3, 0, 2 * Math.PI);
      ctx.fill();

    } else if (shape.shape_type === 'Line') {
      // 線を描画

      // 描画色を設定（選択されている場合は水色、それ以外は黒）
      ctx.fillStyle = shape.is_selected ? 'lightblue' : 'black';
      ctx.strokeStyle = shape.is_selected ? 'lightblue' : 'black';

      const p1CanvasCoordinates = camera.toCanvas(shape.p1.x, shape.p1.y);
      const p2CanvasCoordinates = camera.toCanvas(shape.p2.x, shape.p2.y);
      ctx.beginPath();
      ctx.moveTo(p1CanvasCoordinates.x, p1CanvasCoordinates.y);
      ctx.lineTo(p2CanvasCoordinates.x, p2CanvasCoordinates.y);
      ctx.stroke();

      // p1が選択されていた場合は、p1を水色で描画
      if(shape.p1.is_selected){
        ctx.fillStyle = 'lightblue';
        ctx.strokeStyle =  'lightblue';
        const canvasCoordinates = camera.toCanvas(shape.p1.x, shape.p1.y);
        ctx.beginPath();
        ctx.arc(canvasCoordinates.x, canvasCoordinates.y, 3, 0, 2 * Math.PI);
        ctx.fill();
      }

      // p2が選択されていた場合は、p2を水色で描画
      if(shape.p2.is_selected){
        ctx.fillStyle = 'lightblue';
        ctx.strokeStyle =  'lightblue';
        const canvasCoordinates = camera.toCanvas(shape.p2.x, shape.p2.y);
        ctx.beginPath();
        ctx.arc(canvasCoordinates.x, canvasCoordinates.y, 3, 0, 2 * Math.PI);
        ctx.fill();
      }


    }
    // 他の図形の描画もここに追加できます
  });
}


function drawGrid(ctx) {
  //console.log("I'm in drawGrid().");

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
  //console.log("I'm in drawGridLines()");

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
  //console.log("I'm in drawAxisLine()");
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
  //console.log("I'm in displayCADCoordinates()");
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


function addShape(shape_type, cadCoordinates) {
    //console.log("I'm in sendShapeToBackend()");

    // Ajaxを使用してバックエンドにPOSTリクエストを送信
    fetch('/add_shape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ shape_type: shape_type, coordinates: cadCoordinates }),
    })
    .then(response => response.json())
    .then(data => {            
        if (data.status === 'success') {
            shapesCache = data.shapes_data;
            drawShapesFromCache();
            console.log("shape added:", data);
        }
    });
}


function changeMode(newMode) {
  modeManager.setMode(newMode);

  // 既にアクティブなボタンがあれば、そのスタイルを元に戻す
  if (activeButton) {
    activeButton.classList.remove('active');
  }

  // 新しく選択されたモードのボタンをアクティブにする
  activeButton = document.getElementById(`${newMode}_Button`);
  activeButton.classList.add('active');
}

// **************************************************************

// 現在アクティブなボタンを保持（初期状態は、Select mode）
let activeButton = document.getElementById(`select_mode_Button`);

// 「1ミリ当たりの物理ピクセル数」の計算
var dpi = 100;
var conversionRate = dpi / 25.4;

// canvas要素の取得
let canvas = document.getElementById('myCanvas');

// コンテキストのスケールを調整
var ctx = canvas.getContext('2d');

// Camera
const camera = new Camera(conversionRate);

// ModeManager
const modeManager = new ModeManager();

// バックエンドから取得した図形情報のローカルキャッシュ
let shapesCache = [];

// マウス座標を表示するためのdivを取得
const mouseCoordinatesCanvasDiv = document.getElementById('mouse-coordinates-canvas');
const mouseCoordinatesCadDiv = document.getElementById('mouse-coordinates-cad');

getShapesFromBackend();
//console.log("script.js was started.#2");

// **************************************************************
// 以下、イベントリスナー

// 線の始点と終点を保存する変数
let p1Point = null;
let p2Point = null;

// 線を描画中かどうかを示すフラグ
let isDrawingLine = false;

// ホイールボタンをドラッグしているかどうかを示すフラグ
let isDragging = false;

// 画面移動時の、マウス位置を格納する変数
let lastMousePosition = null;

// 点をドラッグしているかどうかを示すフラグ
let isDraggingPoint = false;

// ドラッグしている点のidを格納する変数
let selectedPointId = null;

// ------------------------------------------------------------------------
// click
// マウス左クリックイベントのリスナー
canvas.addEventListener('click', (event) => {

    //// 共通の処理：マウス位置取得処理
    // canvasの絶対位置を一度取得して変数に格納
    const rect = canvas.getBoundingClientRect();
    // canvas内での相対座標を計算
    const canvasX = event.clientX - rect.left;
    const canvasY = event.clientY - rect.top;
    // canvas座標をCAD座標に変換
    const cadCoordinates = camera.toCAD(canvasX, canvasY);
    
    // 現在のモードを取得
    const currentMode = modeManager.getMode();

    if (currentMode === 'point_mode') {
        // 点を描画する処理
        addShape('Point', cadCoordinates);
        
    } else if (currentMode === 'line_mode') {
        // 線を描画する処理
        if (p1Point === null) {
            // 始点を設定
            p1Point = cadCoordinates;
            isDrawingLine = true;  // 線の描画を開始
        } else {
            // 終点を設定
            p2Point = cadCoordinates;
            
            //console.log("p1:",p1Point);
            //console.log("p2:",p2Point);
            
            // ここでバックエンドに線の始点と終点を送信
            addShape('Line', {p1: p1Point, p2: p2Point});
            
            // 始点と終点をリセット
            p1Point = null;
            p2Point = null;
            
            // 線の描画を終了
            isDrawingLine = false;
            
        }
    } else if (currentMode === 'select_mode') {
        // 画面上での許容値（5pt）をCAD座標系に変換
        // この変換にはcamera.scaleとcamera.conversionRateを使用
        const toleranceInCAD = 5 / (camera.scale * camera.conversionRate);

        // マウスでクリックした座標と許容値をバックエンドに送信
        fetch('/select_shape', {
            method: 'POST',
            body: JSON.stringify({ coordinates: cadCoordinates, tolerance: toleranceInCAD }),
            headers: { 'Content-Type': 'application/json' }
        }).then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 点を水色でハイライト（描画関数内で処理）
                console.log("shape selected:", data);
                shapesCache = data.shapes_data
                drawShapesFromCache();
            }
        });
    }
});

// ------------------------------------------------------------------------
// mousedown
// 画面の並行移動時に、右クリックでのドラッグ開始
canvas.addEventListener('mousedown', (event) => {
  // 現状プログラムでは、modeに依存しないため、modeの取得は行わない

  if (event.button === 1) { // ホイールボタン
    isDragging = true;

    // Canvas要素に対する相対座標を取得する
    const rect = canvas.getBoundingClientRect();
    lastMousePosition = { x: event.clientX - rect.left, y: event.clientY - rect.top };
  }
  if (event.button === 2) {  // 右クリック

    // Canvas要素に対する相対座標を取得する
    const rect = canvas.getBoundingClientRect();

    // canvas内での相対座標を計算
    const canvasX = event.clientX - rect.left;
    const canvasY = event.clientY - rect.top;

    // canvas座標をCAD座標に変換
    const cadCoordinates = camera.toCAD(canvasX, canvasY);

    // 画面上での許容値（5pt）をCAD座標系に変換
    // この変換にはcamera.scaleとcamera.conversionRateを使用
    const toleranceInCAD = 5 / (camera.scale * camera.conversionRate);

    // マウスでクリックした座標と許容値をバックエンドに送信
    fetch('/select_shape', {
        method: 'POST',
        body: JSON.stringify({ coordinates: cadCoordinates, tolerance: toleranceInCAD }),
        headers: { 'Content-Type': 'application/json' }
    }).then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            isDraggingPoint = true;
            selectedPointId = data.selected_shape.id;
            console.log(data);
        }
    });
  }

});

// ------------------------------------------------------------------------
// mouseup
// ドラッグ終了
canvas.addEventListener('mouseup', (event) => {
  // 現状プログラムでは、modeに依存しないため、modeの取得は行わない

  if (event.button === 1) { // ホイールボタン
    isDragging = false;
  }
  if (event.button === 2) { // 右クリック
    isDraggingPoint = false;
    requestId = 0;
    
    // バックエンドにリクエストidをリセットするリクエストを送る
    fetch("/reset_request_id", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({})  // 任意のデータを送る場合はここに記述
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            console.log('reset_request_id:', data);
            drawShapesFromCache();
        } else {
            // 失敗した場合の処理（例：エラーメッセージの表示）
        }
    });

  }

});

// ------------------------------------------------------------------------
// mousemove
// 画面の平行移動時と、線の描画時
let requestId = 0;  // リクエストIDの初期値

canvas.addEventListener('mousemove', (event) => {
  // canvasの絶対位置を取得
  const rect = canvas.getBoundingClientRect();

  // canvas内でのマウスの相対座標を計算
  const canvasX = event.clientX - rect.left;
  const canvasY = event.clientY - rect.top;

  // CAD座標上でのマウス座標を計算
  const cadCoordinates = camera.toCAD(canvasX, canvasY);
  
  // マウス座標をHTMLに出力（Canvas座標とCAD座標それぞれ）
  mouseCoordinatesCanvasDiv.innerHTML = `Canvas X: ${canvasX}, Canvas Y: ${canvasY}`;
  mouseCoordinatesCadDiv.innerHTML = `Cad X: ${cadCoordinates.x.toFixed(3)}, Cad Y: ${cadCoordinates.y.toFixed(3)}`;

  // 現在のモードを取得
  const currentMode = modeManager.getMode();

  // ホイールボタンでドラッグしているとき
  // mode依存なし
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
    drawShapesFromCache();
  }

  // 点をドラッグしているとき
  if (isDraggingPoint) {
    requestId++;  // リクエストIDをインクリメント
    console.log(requestId);

    // 新しい点の座標と目標とする点のIDを送信する
    const newPoint = { x: cadCoordinates.x, y: cadCoordinates.y };
    const targetPointId = selectedPointId;  // 選択された点のID

    debouncedSendPostRequest(newPoint, targetPointId, requestId);
//    fetch('/move_point', {
//      method: 'POST',
//      body: JSON.stringify({ new_point: newPoint, target_point_id: targetPointId, request_id: requestId}),
//      headers: { 'Content-Type': 'application/json' }
//    })
//    .then(response => response.json())
//    .then(data => {
//        if (data.status === 'success') {
//            console.log('point moved:',requestId);
//            shapesCache = data.shapes_data;
//            drawShapesFromCache();
//        } else if (data.status === 'ignored') {
//            console.log('このリクエストは無視されました');
//        }
//    });
  }


  // 線を描画中かどうかを判定
  // Line modeのみで有効
  if (currentMode === 'line_mode' && isDrawingLine && p1Point !== null) {
    // 一旦キャンバスをクリア
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // 既存図形やグリッド線の描画
    drawShapesFromCache();

    // 始点から現在のマウス位置までの線を描画
    const p1CanvasCoordinates = camera.toCanvas(p1Point.x, p1Point.y);
    const p2CanvasCoordinates = camera.toCanvas(cadCoordinates.x, cadCoordinates.y);
    ctx.beginPath();
    ctx.moveTo(p1CanvasCoordinates.x, p1CanvasCoordinates.y);
    ctx.lineTo(p2CanvasCoordinates.x, p2CanvasCoordinates.y);
    ctx.stroke();
  }

  // 他のモードでのmousemove処理をこちらに追加
  // 例: if (currentMode === 'select') { /* 選択モードでの処理 */ }

});

let timeoutID; // タイムアウトIDを保存する変数

function debounce(func, wait) {
  return function(...args) {
    clearTimeout(timeoutID); // 既存のタイマーをクリア
    timeoutID = setTimeout(() => func(...args), wait); // 新しいタイマーを設定
  };
}

// POSTリクエストを送信する関数
function sendPostRequest(newPoint, targetPointId, requestId) {
  fetch('/move_point', {
    method: 'POST',
    body: JSON.stringify({ new_point: newPoint, target_point_id: targetPointId, request_id: requestId}),
    headers: { 'Content-Type': 'application/json' }
  })
  .then(response => response.json())
  .then(data => {
      if (data.status === 'success') {
          console.log('point moved:', requestId);
          shapesCache = data.shapes_data;
          drawShapesFromCache();
      } else if (data.status === 'ignored') {
          console.log('このリクエストは無視されました');
      }
  });
}

// debounce関数でラッピング
const debouncedSendPostRequest = debounce(sendPostRequest, 10); // 10ms後にリクエストを送信



// ------------------------------------------------------------------------
// wheel
// ズームイン、ズームアウト
canvas.addEventListener('wheel', (event) => {
  // 現状プログラムでは、modeに依存しないため、modeの取得は行わない

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

  drawShapesFromCache();  // 再描画

}, { passive: false }); // passiveオプションをfalseに設定して、preventDefaultが効くようにします。

// ------------------------------------------------------------------------
// contextmenu
// 右クリックメニューの無効化
canvas.addEventListener('contextmenu', (event) => {
  // 現状プログラムでは、modeに依存しないため、modeの取得は行わない

  event.preventDefault();
});


// ------------------------------------------------------------------------
// "Apply FixedPointConstraint" ボタンがクリックされたときの処理
document.getElementById("apply-fixed-point-constraint").addEventListener("click", function() {
    // バックエンドに拘束条件を適用するリクエストを送る
    fetch("/apply_fixed_point_constraint", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({})  // 任意のデータを送る場合はここに記述
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            console.log('apply_fixed_point_constraint:', data);
            shapesCache = data.shapes_data;
            drawShapesFromCache();
        } else {
            // 失敗した場合の処理（例：エラーメッセージの表示）
        }
    });
});

// ------------------------------------------------------------------------
// "Apply FixedLengthConstraint" ボタンがクリックされたときの処理
document.getElementById("apply-fixed-length-constraint").addEventListener("click", function() {
    // バックエンドに拘束条件を適用するリクエストを送る
    fetch("/apply_fixed_length_constraint", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({})  // 任意のデータを送る場合はここに記述
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            console.log('apply_fixed_length_constraint:', data);
            shapesCache = data.shapes_data;
            drawShapesFromCache();
        } else {
            // 失敗した場合の処理（例：エラーメッセージの表示）
        }
    });
});
