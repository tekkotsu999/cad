export class UIHandler {
  constructor(cadSystem) {
      this.cadSystem = cadSystem;
      this.initializeEventListeners();
  }

  initializeEventListeners() {
      const clearButton = document.getElementById('clear');
      clearButton.addEventListener('click', () => {
          this.cadSystem.clearDrawing();
      });

      // 他のイベントリスナーも同様に追加...
  }
}