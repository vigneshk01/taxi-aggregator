Dagg_passenger_rating = [
    {
        '$match': {}
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
                        }
                    }
                },
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
    }, {
        '$merge': {
            'into': 'Dagg_passenger_rating'
        }
    }
]

Dagg_vehicle_stats = [
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
            },
            'total_distance_covered_kms': {
                '$sum': {
                    '$add': {
                        '$toInt': {
                            '$arrayElemAt': [
                                '$total_distance_kms', 0
                            ]
                        }
                    }
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
            'total_ridetime_in_mins': '$total_ridetime_in_mins',
            'total_distance_covered_kms': '$total_distance_covered_kms'
        }
    }, {
        '$merge': {
            'into': 'Dagg_vehicle_stats'
        }
    }
]

Hagg_rides_stats = [
    {
        '$match': {}
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
            '_id': 0,
            'date': '$_id.date',
            'hourly_ride_count': '$hourly_ride_count',
            'vehicle_num': '$vehicle_num'
        }
    }, {
        '$merge': {
            'into': 'Hagg_rides_stats'
        }
    }
]