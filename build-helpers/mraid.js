// Wait for the SDK to become ready
if (mraid.getState() === "loading") {
  mraid.addEventListener("ready", onSdkReady);
} else {
  onSdkReady();
}
function viewableChangeHandler(viewable) {
  // start/pause/resume gameplay, stop/play sounds
  if (viewable) {
    if (!isBooted) {
      isMRAIDready = true;
      if (isReadyToBoot && isMRAIDready) {
        startTheGame();
      }
    } else {
      cc.game.resume();
    }
  } else {
    if (isBooted) {
      cc.game.pause();
    }
  }
}

function onSdkReady() {
  mraid.addEventListener("viewableChange", viewableChangeHandler);
  // Wait for the ad to become viewable for the first time
  if (mraid.isViewable()) {
    viewableChangeHandler(true);
  }
}

const mraidBootListener = (event) => {
  isReadyToBoot = true;
  window.removeEventListener("readyToStart");

  if (isReadyToBoot && isMRAIDready) {
    startTheGame();
  }

  window.removeEventListener("readyToStart", mraidBootListener);
};

window.addEventListener("readyToStart", mraidBootListener);
