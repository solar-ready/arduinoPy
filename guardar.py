import serial
import mysql.connector 

# Configure the MySQL connection object
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="",
  database="arduino_pap"
)

# Configure the Serial object
ser = serial.Serial('COM3', 9600)

try:
    # Loop infinitely to read the data from the serial port and insert into the database
    while True:

        line = ser.readline().decode('utf-8').strip()
        print("Mostrar o line --------")
        print(line)

        # split the line into humidity, temperature, and servo position
        parts = line.split(", ")
        parts = list(map(int, parts[0].split()))
        print("Mostrar os parts -------")
        print(parts)

        # check if the line has at least four elements
        if len(parts) < 4:
            print("parts sao menores que 4 --------")
            continue
        difference = parts[2]
        servoSet = parts[3]
        eastLRD = parts[0]
        westLRD = parts[1]
        print("A tentar mostrar os dados ------")
        print(f"Difference: {difference} | servoSet: {servoSet} | eastLRD: {eastLRD} | westLRD: {westLRD}")
        print("antes de inserir dados")
        sql = "INSERT INTO graficos (sensorE, sensorD, diferenca, servo ) VALUES (%s, %s, %s, %s)"
        val = (eastLRD, westLRD, difference, servoSet)
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")

except KeyboardInterrupt:
    # Delete all records from the table after stopping the loop
    mycursor.execute("DELETE FROM graficos")
    mydb.commit()
    print(mycursor.rowcount, "records deleted.")
