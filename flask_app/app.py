import logging
from flask import Flask, Response

app = Flask(__name__)

# Configure logging to capture StatsD logs
statsd_logger = logging.getLogger('statsd')
statsd_logger.setLevel(logging.DEBUG)

# Create a custom handler to capture the logs

metrics=[]
class StatsDHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        global metrics
        metrics.append(log_entry)
        # You can store the log_entry in a list, database, or display it on a webpage
        # For simplicity, we will print it to the console
        print(log_entry)

# Add the custom handler to the StatsD logger
statsd_logger.addHandler(StatsDHandler())


@app.route("/")
def hello_world():
    app.logger.error("Hello, World!")
    return "Hello, World!"


@app.route("/io_task")
def io_task():
    app.logger.error("io_task")
    # ... your io_task logic here ...
    return "IO bound task finish!"


@app.route("/cpu_task")
def cpu_task():
    app.logger.error("cpu_task")
    # ... your cpu_task logic here ...
    return "CPU bound task finish!"


@app.route("/random_sleep")
def random_sleep():
    app.logger.error("random_sleep")
    # ... your random_sleep logic here ...
    return "Random sleep"


@app.route("/random_status")
def random_status():
    app.logger.error("random_status")
    # ... your random_status logic here ...
    status_code = random.choice([200] * 6 + [300, 400, 400, 500])
    return Response("Random status", status=status_code)


@app.route("/statsd_metrics")
def display_statsd_metrics():
    # Retrieve the captured StatsD metrics from the custom handler
    #metrics = ['Metric 1', 'Metric 2', 'Metric 3']  # Replace with your captured StatsD metrics
    global metrics

    # Generate an HTML page to display the metrics
    html = '<h1>StatsD Metrics</h1>'
    for metric in metrics:
        html += '<p>{}</p>'.format(metric)

    return html


if __name__ != '__main__':
    # Use gunicorn's logger to replace flask's default logger
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)