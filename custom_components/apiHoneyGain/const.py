""" Constants """
import datetime

ISSUE_URL="https://github.com/luke2063/apiHoneyGain/issues"

DOMAIN = "apiHoneyGain"

# delai pour l'update http, toutes les 3 heures
SCAN_INTERVAL_http = datetime.timedelta(seconds=60*60*3)

__VERSION__ = "1.0.0.0"

__name__ = "apiHoneyGain"