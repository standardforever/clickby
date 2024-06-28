export function roundToTwoDP(num = 0) {
  
    return Number(num);
    // return Number(num.toFixed(2));
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
  if (number === null || isNaN(number)) {
    return "0";
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

export function trimString(str, maxLength) {
  if (str.length > maxLength) {
    return str.substring(0, maxLength) + '...';
  }
  return str;
}

export function formatDate(date) { //"YYYY-MM-DD hh:mm:ss"
  const d = new Date(date);
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  const hh = String(d.getHours()).padStart(2, '0');
  const min = String(d.getMinutes()).padStart(2, '0');
  const ss = String(d.getSeconds()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd} ${hh}:${min}:${ss}`;
}