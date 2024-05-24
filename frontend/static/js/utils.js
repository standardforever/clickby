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

export function formatNumber(number) {
  if (isNaN(number)) {
      return "Invalid number";
  }

  let formattedNumber = number.toFixed(2);

  formattedNumber = formattedNumber.replace(/\B(?=(\d{3})+(?!\d))/g, ",");

  return formattedNumber;
}

export function formatPercentage(number) {
  if (isNaN(number)) {
      return "Invalid number";
  }

  let roundedNumber = Math.round(number);

  return roundedNumber + "%";
}

export function formatNumberWithoutDecimals(number) {
  if (isNaN(number)) {
      return "Invalid number";
  }
  let formattedNumber = Math.round(number).toString();
  formattedNumber = formattedNumber.replace(/\B(?=(\d{3})+(?!\d))/g, ",");

  return formattedNumber;
}