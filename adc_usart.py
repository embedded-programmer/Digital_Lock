from machine import Pin,UART
import utime

num_readings = 10000

# Configure ADC pins
adc_pin_1 = machine.ADC(2)  # ADC channel 2
adc_pin_2 = machine.ADC(1)  # ADC channel 1
adc_pin_3 = machine.ADC(0)  # ADC channel 0

# Configure UART (USART) pins
uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))  # UART0, baudrate 9600, TX=GPIO0, RX=GPIO1

while True:
    # Read ADC values
    adc_sum_1 = sum(adc_pin_1.read_u16()>> 6 for _ in range(num_readings))
    adc_sum_2 = sum(adc_pin_2.read_u16()>> 6 for _ in range(num_readings))
    adc_sum_3 = sum(adc_pin_3.read_u16()>> 6 for _ in range(num_readings))


    # Calculate averages
    adc_average_1 = adc_sum_1 // num_readings
    adc_average_2 = adc_sum_2 // num_readings
    adc_average_3 = adc_sum_3 // num_readings 
    
    # Format the data as a string (you can modify this based on your requirements)
    data_string = f"{adc_average_1:04d},{adc_average_2:04d},{adc_average_3:04d}"

    # Send data over UART
    uart0.write(data_string)
    print(data_string)
    # Wait for some time before reading again (adjust as needed)
    utime.sleep_ms(10)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    















    
