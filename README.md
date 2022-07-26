# Pyanair

Basic app using Ryanair endpoint and requests library to get flights on given day

## Setup

To install, simply download the repo and install requests library using pip
"""pip install requests"""

## Example of usage

"""
/path/to/script/main.py 1 0 0 0 KTW ATH RT 2022-08-03 2022-08-15
"""

Where following parameters are:
Adult, Teen, Children, Infant, Origin, Destination, trip type (RT, OW), Date of flight, Date of back flight

Example response might look like this:
"""
[
    {
        "Type": "RT",
        "flights": [
            {
                "Heading": "To",
                "Adults": 1,
                "Teens": 0,
                "Children": 0,
                "Currency": "PLN",
                "Price": 1481.0,
                "Origin": "KTW",
                "Destination": "ATH",
                "Departure": "2022-08-04 09:55:00.000",
                "Arrival": "2022-08-04 13:15:00.000",
                "Duration": "02:20",
                "Carrier": "FR",
                "Flightnumber": "2615",
                "Segments": [
                    {
                        "segment_nr": 0,
                        "segment_origin": "KTW",
                        "segment_destination": "ATH",
                        "segment_flight_number": "FR 2615",
                        "segment_out": "2022-08-04 09:55:00.000",
                        "segment_in": "2022-08-04 13:15:00.000",
                        "segment_duration": "02:20"
                    }
                ]
            },
            {
                "Heading": "Back",
                "Adults": 1,
                "Teens": 0,
                "Children": 0,
                "Currency": "PLN",
                "Price": 1653.88,
                "Origin": "ATH",
                "Destination": "KTW",
                "Departure": "2022-08-14 10:25:00.000",
                "Arrival": "2022-08-14 11:55:00.000",
                "Duration": "02:30",
                "Carrier": "FR",
                "Flightnumber": "2614",
                "Segments": [
                    {
                        "segment_nr": 0,
                        "segment_origin": "ATH",
                        "segment_destination": "KTW",
                        "segment_flight_number": "FR 2614",
                        "segment_out": "2022-08-14 10:25:00.000",
                        "segment_in": "2022-08-14 11:55:00.000",
                        "segment_duration": "02:30"
                    }
                ]
            }
        ]
    }
]
"""


