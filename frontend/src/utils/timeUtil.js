/**
 * prettyDate - prettied datetime display
 * @param {String} time - the JSON formatted time string
 */
export function prettyDate(time) {
  let date = new Date((time || "").replace(/-/g, "/").replace(/[TZ]/g, " ")),
    diff = (new Date().getTime() - date.getTime()) / 1000,
    day_diff = Math.floor(diff / 86400);

  // return date for anything greater than a week
  if (isNaN(day_diff) || day_diff < 0 || day_diff > 7) {
    const pad = (n) => (n.toString().length < 2 ? "0" + n : n);
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(
      date.getDate()
    )}`;
  }

  return (
    (day_diff == 0 &&
      ((diff < 60 && "刚刚") ||
        (diff < 120 && "1 分钟前") ||
        (diff < 3600 && Math.floor(diff / 60) + " 分钟前") ||
        (diff < 7200 && "1 小时前") ||
        (diff < 86400 && Math.floor(diff / 3600) + " 小时前"))) ||
    (day_diff == 1 && "昨天") ||
    (day_diff < 7 && day_diff + " 天前") ||
    (day_diff < 31 && Math.ceil(day_diff / 7) + " 周前")
  );
}
