// canvas要素の取得
let canvas = document.getElementById('myCanvas');
let ctx = canvas.getContext('2d');

// 初期データ（CAD座標系で定義）
let data = {
    a: {x: 300, y: 300},
    b: {x: 300, y: 500},
    c: {x: 500, y: 400},
    d: {x: 500, y: 300},
    displacement: [0, 0]
};

// マウスの動きを検出
canvas.addEventListener('mousemove', (event) => {
    // マウスの座標を取得
    let mouseX = event.clientX - canvas.offsetLeft;
    let mouseY = event.clientY - canvas.offsetTop;

    // 座標変換を適用
    let { x : transformed_mouse_x, y : transformed_mouse_y } = transformCoordinatesToCAD(mouseX, mouseY);

    // c点とマウスカーソルの位置との相対位置を計算
    data.displacement[0] = transformed_mouse_x - data.c.x;
    data.displacement[1] = transformed_mouse_y - data.c.y;
    // console.log( data.displacement[0] );
    // console.log( data.displacement[1] );

    // /optimize エンドポイントにデータを送信
    fetch('/optimize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(r_data => {
        // 最適化後の新しい座標を取得
        let newCoordinates = r_data;

        // canvasをクリア
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // canvas座標系に変換
        let transformed_newCoordinates = {
            a : transformCoordinatesToCanvas( newCoordinates.a.x, newCoordinates.a.y ),
            b : transformCoordinatesToCanvas( newCoordinates.b.x, newCoordinates.b.y ),
            c : transformCoordinatesToCanvas( newCoordinates.c.x, newCoordinates.c.y ),
            d : transformCoordinatesToCanvas( newCoordinates.d.x, newCoordinates.d.y )
        };
        // console.log(transformed_newCoordinates)

        // 新しい座標をcanvasに描画
        ctx.beginPath();
        ctx.moveTo( transformed_newCoordinates.a.x, transformed_newCoordinates.a.y);
        ctx.lineTo( transformed_newCoordinates.b.x, transformed_newCoordinates.b.y);
        ctx.lineTo( transformed_newCoordinates.c.x, transformed_newCoordinates.c.y);
        ctx.lineTo( transformed_newCoordinates.d.x, transformed_newCoordinates.d.y);
        ctx.lineTo( transformed_newCoordinates.a.x, transformed_newCoordinates.a.y);
        ctx.stroke();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

// CAD座標系に座標変換する関数
function transformCoordinatesToCAD(x, y) {
  // console.log("x=", x );
  // console.log("y=", y);

  // ここで座標変換のロジックを実装
  let transformed_x = x / 2; // 例: x座標を半分に
  let transformed_y = y / 2; // 例: y座標を半分に
  // console.log("transformed_x=", transformed_x);
  // console.log("transformed_y=", transformed_y);

  return { x : transformed_x, y : transformed_y };
}

// Canvas座標系に座標変換する関数
function transformCoordinatesToCanvas(x, y) {
  let transformed_x = x * 2; // 例: x座標を2倍
  let transformed_y = y * 2; // 例: y座標を2倍
  return { x : transformed_x, y : transformed_y };
}