from flask import Flask, render_template, request
import weather_logic
import journey_logic
import place_logic

app = Flask(__name__)


@app.route('/')
@app.route('/home')
@app.route('/homepage')
def home():
    return render_template('home.html')


@app.route('/journey', methods=['GET'])
def journey():
    # Form Values.
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    overview = request.args.get('overview')
    display_steps = request.args.get('display_steps')
    dist = request.args.get('dist_unit')

    # API Request.
    journey_info, steps = journey_logic.get_journey(departure, destination)

    return render_template('journey.html', journey=journey_info, steps=steps,
                           dist=dist, overview=overview,
                           display_steps=display_steps)


@app.route('/weather', methods=['GET'])
def weather():
    # Form Values.
    weather_place = request.args.get('weather_place')
    temp = request.args.get('temp_unit')
    speed = request.args.get('speed_unit')

    # API Requests.
    today = weather_logic.get_current_weather(weather_place)
    forecast = weather_logic.get_forecast_weather(weather_place)

    return render_template('weather.html', today=today, forecast=forecast,
                           temp=temp, speed=speed)


@app.route('/places', methods=['GET'])
def places():
    # Form Values.
    city_name = request.args.get('city_name')
    place_type = request.args.get('place_type')
    sort_by = request.args.get('sort_by')
    try:
        city_name = city_name.title()
    except AttributeError:  # May return as None.
        pass

    # API Request.
    p_info = place_logic.get_places(city_name, place_type)

    # Sort the list of dictionaries if the request was successful.
    if p_info is not None:
        if sort_by == 'rating_a':
            p_info = sorted(p_info, key=lambda k: k['rating'])
        elif sort_by == 'rating_d':
            p_info = sorted(p_info, key=lambda k: k['rating'], reverse=True)
        elif sort_by == 'number':
            p_info = sorted(p_info, key=lambda k: k['total'], reverse=True)

    return render_template('places.html', places=p_info, city=city_name)


@app.errorhandler(404)
def invalid_page(error):
    return render_template('invalid_page.html', error=error)


if __name__ == '__main__':
    app.run()
