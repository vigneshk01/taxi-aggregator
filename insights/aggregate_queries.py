vehicle_daily_rating_avg = [
    {
        '$match': {}
    }, {
        '$group': {
            '_id': {
                'date': '$booked_time', 
                'vehicle_num': '$vehicle_num'
            }, 
            'avg': {
                '$avg': {
                    '$toInt': '$passenger_rating'
                }
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'date': '$_id.date', 
            'vehicle_num': '$_id.vehicle_num', 
            'avg': '$avg'
        }
    }
]

hourly_booking_Aggr = [
    {
        '$match': {
            'booked_time': {
                '$gte': '2021-09-05T00:00:00.000', 
                '$lt': '2021-09-06T00:00:00.000'
            }
        }
    }, {
        '$group': {
            '_id': {
                'date': {
                    '$dateFromParts': {
                        'year': {
                            '$year': {
                                '$toDate': '$booked_time'
                            }
                        }, 
                        'month': {
                            '$month': {
                                '$toDate': '$booked_time'
                            }
                        }, 
                        'day': {
                            '$dayOfMonth': {
                                '$toDate': '$booked_time'
                            }
                        }, 
                        'hour': {
                            '$hour': {
                                '$toDate': '$booked_time'
                            }
                        }
                    }
                }
            }, 
            'hourly_ride_count': {
                '$sum': 1
            }, 
            'vehicle_num': {
                '$addToSet': '$vehicle_num'
            }
        }
    }, {
        '$sort': {
            '_id.date': 1
        }
    }, {
        '$project': {
            'date': '$_id.date', 
            'hourly_ride_count': '$hourly_ride_count', 
            'vehicle_num': '$vehicle_num'
        }
    }
]

taxi_daily_projections = [
    {
        '$group': {
            '_id': {
                'vehicle_num': '$vehicle_num', 
                'date': {
                    '$dateToString': {
                        'format': '%Y-%m-%d', 
                        'date': {
                            '$toDate': '$booked_time'
                        }
                    }
                }
            }, 
            'total_rides': {
                '$sum': 1
            }, 
            'income': {
                '$sum': '$cost'
            }, 
            'total_ridetime_in_mins': {
                '$sum': {
                    '$divide': [
                        {
                            '$subtract': [
                                {
                                    '$toDate': '$end_time'
                                }, {
                                    '$toDate': '$booked_time'
                                }
                            ]
                        }, 60000
                    ]
                }
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'vehicle_num': '$_id.vehicle_num', 
            'date': '$_id.date', 
            'total_rides': '$total_rides', 
            'income': '$income', 
            'total_ridetime_in_mins': '$total_ridetime_in_mins'
        }
    }
]