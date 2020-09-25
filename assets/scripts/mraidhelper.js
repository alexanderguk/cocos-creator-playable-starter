cc.Class({
  extends: cc.Component,

  properties: {},

  start() {},

  onClick() {
    if (typeof mraid !== "undefined") {
      if (cc.sys.os == cc.sys.OS_ANDROID) {
        mraid.open("https://play.google.com/store/apps/details?id=yourgame");
      } else if (cc.sys.os == cc.sys.OS_IOS) {
        mraid.open("https://apps.apple.com/us/app/yourgamename/yourgameid");
      } else {
        mraid.open();
      }
    }
  },
});
