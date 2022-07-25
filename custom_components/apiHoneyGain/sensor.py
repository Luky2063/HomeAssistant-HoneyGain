"""Sensor for my first"""
import logging
import json
from collections import defaultdict
from datetime import timedelta, datetime

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_TOKEN,
    CONF_NAME,
    ATTR_ATTRIBUTION,
    CONF_SCAN_INTERVAL,
)

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from homeassistant.util import slugify
from homeassistant.util.dt import now, parse_date


from .const import (
    DOMAIN,
    __VERSION__,
    __name__,
    SCAN_INTERVAL_http,
)

_LOGGER = logging.getLogger(__name__)
DOMAIN = "luke2063"
ICON = "mdi:package-variant-closed"
SCAN_INTERVAL = timedelta(seconds=1800)
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_TOKEN): cv.string,
    }
)

from . import apiHoneyGain, sensorApiHoneyGain

class myHoneyGain:
    def __init__(self, token, _update_interval):
        self._lastSynchro = None
        self._update_interval = _update_interval
        self._token = token
        self._myHoneyGain = apiHoneyGain.HoneyGain()
        pass


    def update(self,):
        import datetime

        courant = datetime.datetime.now()
        if ( self._lastSynchro == None ) or \
            ( (self._lastSynchro + self._update_interval) < courant ):
            _LOGGER.warning("-update possible- on lance")
            self._myHoneyGain.set_jwt_token( self._token )
            self._lastSynchro = datetime.datetime.now()

    # revoir recupearation valeur
    def getmyHoneyGain(self):
        return self._myHoneyGain

    def getMoney(self):
        money = 0.00
        
        try:
            json = self._myHoneyGain.balances()
            money = round(json['payout']['usd_cents'] / 100,2)
        except:
            money = 0.00
            
        return money
        
    def getTotalMoney(self):
        money = 0.00
        try:
            # Add all payouts
            for payout in self._myHoneyGain.payouts():
                money = money + round(payout['requested_amount'] / 100,2)
            # Add current balance
            json = self._myHoneyGain.balances()
            money = money + round(json['payout']['usd_cents'] / 100,2)
        except:
            money = 0.00
        return money

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the platform."""
    name = config.get(CONF_NAME)
    update_interval = config.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL)
    update_interval_http = SCAN_INTERVAL_http
    try:
        token = config.get(CONF_TOKEN)
        session = []
    except :
        _LOGGER.exception("Could not run my apiMaree Extension miss argument ?")
        return False
    myHG = myHoneyGain( token, update_interval )
    myHG.update()
    add_entities([infoHGSensorMoney(session, name, update_interval, myHG )], True)
    add_entities([infoHGSensorTotalMoney(session, name, update_interval, myHG )], True)

class infoHGSensorMoney(Entity):
    """."""

    def __init__(self, session, name, interval, myHG):
        """Initialize the sensor."""
        self._session = session
        self._name = name
        self._myHG = myHG
        self._attributes = None
        self._state = None
        self.update = Throttle(interval)(self._update)
        self._sAM = sensorApiHoneyGain.manageSensorState()
        self._sAM.init( self._myHG )

    @property
    def name(self):
        """Return the name of the sensor."""
        return "myHoneyGain"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return "$"

    def _update(self):
        """Update device state."""
        self._myHG.update()
        self._state, self._attributes = self._sAM.getstatusMoney()

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return ICON


class infoHGSensorTotalMoney(Entity):
    """."""

    def __init__(self, session, name, interval, myHG):
        """Initialize the sensor."""
        self._session = session
        self._name = name
        self._myHG = myHG
        self._attributes = None
        self._state = None
        self.update = Throttle(interval)(self._update)
        self._sAM = sensorApiHoneyGain.manageSensorState()
        self._sAM.init( self._myHG )

    @property
    def name(self):
        """Return the name of the sensor."""
        return "myHoneyGain.totalMoney"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return "$"

    def _update(self):
        """Update device state."""
        self._myHG.update()
        self._state, self._attributes = self._sAM.getstatusTotalMoney()

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return ICON
