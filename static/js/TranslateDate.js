class TranslateDate {
  //Fecha determinada -> un momento en el tiempo
  timestamp;
  date;

  constructor(){
    this.timestamp = Date.now();
    this.date = new Date(this.timestamp);
  }
  
  getStringDate(timestamp) {

    this.timestamp = timestamp;
    this.date = new Date(timestamp);


    const diff = this.getHoursDiff();

    if (diff <= 24) {
      if (diff < 1 && diff > 0.02) {
        return `${ Math.round(diff * 60) } minutes ago`;
      } 
      else if(diff <= 0.02){
        return 'recently';
      }
      else {
        return `${Math.round(diff)} hours ago`;
      }
    } else {
      return `${this.getDay()} ${this.getMonth()} ${this.date.getDate()},  ${this.date.getFullYear()}`;
    }
  }

  getHoursDiff() {
    let now = Date.now();    
    return ((now - this.timestamp) / 3600000);
  }

  getDay() {
    switch (this.date.getDay()) {
      case 0:
        return "sunday";

      case 1:
        return "monday";

      case 2:
        return "tuesday";

      case 3:
        return "wednesday";

      case 4:
        return "thursday";

      case 5:
        return "friday";

      case 6:
        return "saturday";
    }
  }

  getMonth() {
    switch (this.date.getMonth()) {
      case 0:
        return "january";

      case 1:
        return "february";

      case 2:
        return "march";

      case 3:
        return "april";

      case 4:
        return "may";

      case 5:
        return "june";

      case 6:
        return "july";

      case 7:
        return "august";

      case 8:
        return "september";

      case 9:
        return "october";

      case 10:
        return "november";

      case 11:
        return "december";
    }
  }
}
  