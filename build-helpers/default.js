const defaultBootListener = (event) => {
  boot();
  window.removeEventListener("readyToBoot", defaultBootListener);
};

window.addEventListener("readyToBoot", defaultBootListener);
