import os
from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory

import urllib.request
import urllib.parse
import urllib.error

import json

if os.environ.get('FLASK_ENV') == 'development':
    app = Flask(__name__, static_url_path='')


    @app.route('/aesthetics/<path:path>')
    def aesthetics(path):
        return send_from_directory('aesthetics', path)

else:
    app = Flask(__name__)


def safe_get(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.URLError as error:
        print('Error! {}'.format(error))
    return None


@app.route('/')
def root():
    return render_template('home.html', title='My Project')


@app.route('/results', strict_slashes=False)
def results(potential_breed=None):

    base_url = 'https://dog.ceo/api/'
    user_input = request.args.get('breed').lower()

    dog_results = []
    if user_input.lower() == "german shepherd":
        user_input = "germanshepherd"
    # print(user_input)
    breeds = user_input.split(' ') if potential_breed is None else potential_breed.lower().split(' ')
    # print(breeds)
    if len(breeds) > 2:
        return render_template('error.html')
    if len(breeds) == 2:
        sub_breed = breeds[0]
        main_breed = breeds[1]
    else:
        sub_breed = None
        main_breed = breeds[0]

    # Check if main breed exists
    request_url = '{}breed/{}/list'.format(base_url, main_breed)
    response_data = safe_get(request_url)
    if response_data is None:
        return render_template('error.html')
    breed_data = json.loads(response_data.read())
    sub_breeds = breed_data['message']
    if sub_breed is not None and sub_breed in sub_breeds:
        sub_breeds = [sub_breed]
    if len(sub_breeds) > 0:
        for breed in sub_breeds:
            raw_sub_breed_data = safe_get('{}breed/{}/{}/images'.format(base_url, main_breed, breed))
            if raw_sub_breed_data is None:
                return render_template('error.html')
            sub_breed_data = json.loads(raw_sub_breed_data.read())
            dog_results.append({
                'name': '{} {}'.format(breed.capitalize(), main_breed.capitalize()),
                'images': sub_breed_data['message']
            })
    else:
        raw_sub_breed_data = safe_get('{}breed/{}/images'.format(base_url, main_breed))
        if raw_sub_breed_data is None:
            return render_template('error.html')
        sub_breed_data = json.loads(raw_sub_breed_data.read())
        dog_results.append({
            'name': '{}'.format(main_breed.capitalize()),
            'images': sub_breed_data['message']
        })
    title = 'Results!' if potential_breed is None else 'More Pictures!'
    individual = False if potential_breed is None else True
    return render_template('results.html', title=title, data=dog_results, individual=individual)


@app.route('/picture-page', strict_slashes=False)
def pics():
    return results(request.args.get('breed').lower())

if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)

