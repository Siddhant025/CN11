import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration


sentry_sdk.init(
    "https://267f5785ce3f415e949ae24472730923@o1143346.ingest.sentry.io/6203675",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

app = Flask(__name__)


@app.route('/')
def trigger_error():
    division_by_zero = 1 / 0


@app.route()
def value_error():
    raise ValueError()


@app.route('/test')
def test_error_in_errorhandler(sentry_init, capture_events, app):
    sentry_init(integrations=[flask_sentry.FlaskIntegration()])

    app.debug = False
    app.testing = False

    @app.route("/")
    def index():
        raise ValueError()

    @app.errorhandler(500)
    def error_handler(err):
        1 / 0

    events = capture_events()

    client = app.test_client()

    with pytest.raises(ZeroDivisionError):
        client.get("/")

    event1, event2 = events

    (exception,) = event1["exception"]["values"]
    assert exception["type"] == "ValueError"

    exception = event2["exception"]["values"][-1]
    assert exception["type"] == "ZeroDivisionError"


if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
