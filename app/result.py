from flask import jsonify

def Result(status,data,status_code):
    return (
        jsonify(
            {
                "author": "fajrul falah",
                "status": status,
                "data": data,
            }
        ),
        status_code,
    )