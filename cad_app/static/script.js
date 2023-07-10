let canvas = document.getElementById('myCanvas');
let ctx = canvas.getContext('2d');
let data = {
    a: {x: 300, y: 300},
    b: {x: 300, y: 500},
    c: {x: 500, y: 400},
    d: {x: 500, y: 300},
    displacement: [0, 0]
};

canvas.addEventListener('mousemove', (event) => {
    // マウスカーソルの位置を取得
    let mouseX = event.clientX - canvas.offsetLeft;
    let mouseY = event.clientY - canvas.offsetTop;

    // c点とマウスカーソルの位置との相対位置を計算
    data.displacement[0] = mouseX - data.c.x;
    data.displacement[1] = mouseY - data.c.y;

    // /optimize エンドポイントにデータを送信
    fetch('/optimize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(r_data => {
        // 最適化後の新しい座標を取得
        let newCoordinates = r_data;

        // canvasをクリア
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 新しい座標をcanvasに描画
        ctx.beginPath();
        ctx.moveTo(data.a.x, data.a.y);
        ctx.lineTo(newCoordinates.b.x, newCoordinates.b.y);
        ctx.lineTo(newCoordinates.c.x, newCoordinates.c.y);
        ctx.lineTo(data.d.x, data.d.y);
        ctx.lineTo(data.a.x, data.a.y);
        ctx.stroke();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
