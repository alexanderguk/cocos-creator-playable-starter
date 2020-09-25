cc.Class({
  extends: cc.Component,

  properties: {},

  start() {},

  onClick() {
    if (typeof dapi !== "undefined") {
      if (cc.sys.os == cc.sys.OS_ANDROID) {
        dapi.openStoreUrl(
          "https://play.google.com/store/apps/details?id=yourgame"
        );
      } else if (cc.sys.os == cc.sys.OS_IOS) {
        dapi.openStoreUrl(
          "https://apps.apple.com/us/app/yourgamename/yourgameid"
        );
      } else {
        dapi.openStoreUrl();
      }
    }
  },
});
