import argparse
from urllib import response
import requests
import datetime
import json
import re

def roundtrip_to_str_bool(trip: str)-> str:
    return True if trip == 'RT' else False

def date_to_str(date: datetime.date.isoformat)-> str:
    return str(date)

def calculate_flight_price(a_c: int, a_p: int, a_d: int, t_c: int, t_p: int, t_d: int, c_c: int, c_p: int, c_d: int)-> float:
    return round(a_c * a_p - a_d + t_c * t_p - t_d + c_c * c_p - c_d,2)

def fulldate_to_split_str(date: str)-> str:
    return ' '.join(date.split('T'))



parser = argparse.ArgumentParser()

parser.add_argument('ADT', type=int)
parser.add_argument('TEEN', type=int)
parser.add_argument('CHD', type=int)
parser.add_argument('INF', type=int)
parser.add_argument('Origin', type=str)
parser.add_argument('Destination', type=str)
parser.add_argument('RoundTrip', type=str, choices=['RT', 'OW']) # OW, RT
parser.add_argument('DateOut', type=datetime.date.fromisoformat)
parser.add_argument('DateIn', type=datetime.date.fromisoformat)


args = parser.parse_args()

round_trip = args.RoundTrip[:]

args.RoundTrip = roundtrip_to_str_bool(args.RoundTrip)
args.DateOut = date_to_str(args.DateOut)
args.DateIn = date_to_str(args.DateIn)

param_args = vars(args)

param_args['Disc'] = 0
param_args['promoCode'] = ''
param_args['IncludeConnectinFlights'] = 'false'
param_args['FlexDaysBeforeIn'] = 2
param_args['FlexDaysIn'] = 2
param_args['FlexDaysBeforeOut'] = 2
param_args['FlexDaysOut'] = 2
param_args['ToUs'] = 'AGREED'
param_args['ChangeFlight'] = 'undefined'


result = requests.get('https://www.ryanair.com/api/booking/v4/pl-pl/availability?', params=param_args)
empty_flights = 0 
list_of_flights = []

if result.status_code == 404:
    print('No flights found')
else:
    response_dict = json.loads(result.text)
    #print(json.dumps(response_dict, indent=4))
    currency = response_dict['currency']
    trips = response_dict['trips']
    for trip in trips:
        segments = []
        origin = trip['origin']
        destination = trip['destination']
        dates = trip['dates']
        for date in dates:
            if date['flights'] != []:
                for flight in date['flights']:
                    for fare in flight['regularFare']['fares']:
                        if fare['type'] == 'ADT':
                            adults_count = fare['count']
                            adults_price = fare['amount']
                            adults_discount = fare['discountAmount']

                        if fare['type'] == 'TEEN':
                            teen_count = fare['count']
                            teen_price = fare['amount']
                            teen_discount = fare['discountAmount']

                        if fare['type'] == 'CHD':
                            chd_count = fare['count']
                            chd_price = fare['amount']
                            chd_discount = fare['discountAmount']

                    for segment in flight['segments']:
                        segments.append({
                            'segment_nr':segment['segmentNr'],
                            'segment_origin':segment['origin'],
                            'segment_destination':segment['destination'],
                            'segment_flight_number':segment['flightNumber'],
                            'segment_out':fulldate_to_split_str(segment['time'][0]),
                            'segment_in':fulldate_to_split_str(segment['time'][1]),
                            'segment_duration':segment['duration']
                        })
                flight_number = flight['flightNumber']
                time_out = flight['time'][0]
                time_in = flight['time'][1]
                duration = flight['duration']
            else:
                empty_flights += 1

        if empty_flights != 5:
            list_of_flights.append({
                'Type':round_trip,
                'flights':[{
                    'Heading': 'Back' if param_args['Origin'] == destination else 'To', 
                    'Adults':adults_count,
                    'Teens':teen_count,
                    'Children':chd_count,
                    'Currency':currency,
                    'Price':calculate_flight_price(adults_count, adults_price, adults_discount, teen_count, teen_price, teen_discount, chd_count,
                    chd_price, chd_discount),
                    'Origin': origin,
                    'Destination': destination,
                    'Departure': fulldate_to_split_str(time_out),
                    'Arrival': fulldate_to_split_str(time_in),
                    'Duration': duration,
                    'Carrier': re.sub(r'[\s\d]', '', flight_number),
                    'Flightnumber': re.sub(r'[\sa-zA-Z]', '', flight_number),
                    'Segments': segments
                }]
            })
        else:
            list_of_flights.append({
                'Message': f'No flights to {destination} from {param_args["Origin"]} found'
            })

print(json.dumps(list_of_flights, indent=4))

# main.py 1 0 0 0 KTW ATH RT 2022-05-19 2022-06-23