import config

def decoding_space(text):
    return text.replace(' ','+')

def get_request(bus,bus_name,bus_number,time,start_station,stop_station):
    bus_name = decoding_space(bus_name)
    bus_number = decoding_space(bus_number)
    time = decoding_space(time)
    start_station = decoding_space(start_station)
    stop_station = decoding_space(stop_station)
    request = f'{config.URL}/?bus={bus}&busName={bus_name}&number={bus_number}&time={time}&startStation={start_station}&stopStation={stop_station}'
    print(request)
    return request
