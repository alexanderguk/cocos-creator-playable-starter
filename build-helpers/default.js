const defaultBootListener = (event) => {
  startTheGame();
  window.removeEventListener("readyToStart", defaultBootListener);
};

window.addEventListener("readyToStart", defaultBootListener);
