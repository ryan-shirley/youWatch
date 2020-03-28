from flask import Flask
import rq_dashboard
import os

# Setup Flask sever & Cron
app = Flask(__name__)

# Setup Redis Dashboard
redis_host = os.getenv('REDIS_HOST', 'localhost')
app.config["RQ_DASHBOARD_REDIS_HOST"] = redis_host
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

# Flask Routes
from app import views
from app import background