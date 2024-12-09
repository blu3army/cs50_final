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
        return `hace ${ Math.round(diff * 60) } minutos`;
      } 
      else if(diff <= 0.02){
        return 'recién';
      }
      else {
        return `hace ${Math.round(diff)} horas`;
      }
    } else {
      return `El ${this.getDay()} ${
        this.date.getDate()
      } de ${this.getMonth()} ${this.date.getFullYear()}`;
    }
  }

  getHoursDiff() {
    let now = Date.now();    
    return ((now - this.timestamp) / 3600000);
  }

  getDay() {
    switch (this.date.getDay()) {
      case 0:
        return "domingo";

      case 1:
        return "lunes";

      case 2:
        return "martes";

      case 3:
        return "miércoles";

      case 4:
        return "jueves";

      case 5:
        return "viernes";

      case 6:
        return "sábado";
    }
  }

  getMonth() {
    switch (this.date.getMonth()) {
      case 0:
        return "enero";

      case 1:
        return "febrero";

      case 2:
        return "marzo";

      case 3:
        return "abril";

      case 4:
        return "mayo";

      case 5:
        return "junio";

      case 6:
        return "julio";

      case 7:
        return "agosto";

      case 8:
        return "septiembre";

      case 9:
        return "octubre";

      case 10:
        return "noviembre";

      case 11:
        return "diciembre";
    }
  }
}
  