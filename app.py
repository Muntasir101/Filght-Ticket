from flask import Flask, render_template, request
from datetime import datetime, date, timedelta

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('calculate.html')


@app.route('/calculator', methods=['GET', 'POST'])
def flight_cost_calculator():
    if request.method == 'POST':
        distance = int(request.form['distance'])
        departure_date = request.form['departure_date']
        baggage = int(request.form['baggage'])
        cost = 0

        if distance < 500:
            cost = 100
        elif 500 <= distance <= 1000:
            departure_date = convert_date(departure_date)
            if departure_date_within_days(departure_date, 7):
                cost = distance * 0.10
            elif departure_date_within_days(departure_date, 30):
                cost = distance * 0.08
            elif departure_date_within_days(departure_date, 90):
                cost = distance * 0.06
        else:
            departure_date = convert_date(departure_date)
            if departure_date_within_days(departure_date, 7):
                cost = distance * 0.30
            elif departure_date_within_days(departure_date, 30):
                cost = distance * 0.25
            elif departure_date_within_days(departure_date, 90):
                cost = distance * 0.20

            seat_class = request.form['seat_class']
            if seat_class == 'Business':
                cost *= 2
            elif seat_class == 'First':
                cost *= 3

        if distance >= 500 and distance <= 1000:
            extra_baggage_cost = baggage * 25
        elif distance > 1000:
            extra_baggage_cost = baggage * 50
        else:
            extra_baggage_cost = 0

        cost += extra_baggage_cost

        tax = cost * 0.10
        total_cost = cost + tax

        if total_cost > 1000:
            total_cost -= total_cost * 0.05
        if total_cost > 2000:
            total_cost -= total_cost * 0.10

        return render_template('result.html', cost=cost, tax=tax, total_cost=total_cost)


def convert_date(date_string):
    # Convert the date_string to a datetime object
    date_object = datetime.strptime(date_string, '%Y-%m-%d').date()
    return date_object


def departure_date_within_days(departure_date, num_days):
    today = date.today()
    difference = departure_date - today
    return 0 <= difference.days <= num_days


if __name__ == '__main__':
    app.run(debug=True)
