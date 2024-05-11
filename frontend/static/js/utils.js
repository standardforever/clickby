export function roundToTwoDP(num) {
    return Number(num.toFixed(2));
  }

  export function breakDate(dateString) {
    var parts = dateString.split(' ');
    var datePart = parts[0];
    var timePart = parts[1];
    return {
        date: datePart,
        time: timePart
    };
}