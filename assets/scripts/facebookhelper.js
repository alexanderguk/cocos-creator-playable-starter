cc.Class({
  extends: cc.Component,

  properties: {},

  start() {},

  onClick() {
    if (typeof FbPlayableAd !== "undefined") {
      FbPlayableAd.onCTAClick();
    }
  },
});
