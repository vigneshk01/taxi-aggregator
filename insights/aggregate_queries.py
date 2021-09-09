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

taxi_daily_projections =[
    {
        '$addFields': {
            '1': {
                '$toDate': '$booked_time'
            },
            '2': {
                '$toDate': '$end_time'
            },
            '3': {
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
    }, {
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
            'total_ridein_mins': {
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
            'total_ridein mins': '$total_ridein_mins'
        }
    }
]