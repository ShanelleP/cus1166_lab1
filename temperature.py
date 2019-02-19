from flask import request
from app.api import api_bp
from app.models import Billing
import json, ipaddress
from app import db

@api_bp.route('/c2f/<float:value>', methods=['GET'])
def c2f(value):
    get_ip = request.remote_addr
    ip = str(ipaddress.IPv4Address(get_ip))
    record_ip = Billing.query.filter_by(ip=ip).first()
    update(record_ip)
    return c2f(value)

@api_bp.route('/f2c/<float:value>', methods=['GET'])
def f2c(value):
    get_ip = request.remote_addr
    ip = str(ipaddress.IPv4Address(get_ip))
    record_ip = Billing.query.filter_by(ip=ip).first()
    update(record_ip)
    return f2c(value)

def c2f(value):
    c2f_dict = {
	   "conversionType" : "TEMP",
		"from" : "Celsius",
		"fromValue": value,
		"to" : "Farenheit",
		"toValue" : ((value*9/5) + 32)

    }
    return json.dumps(c2f_dict)

def f2c(value):
    f2c_dict ={
        "conversionType" : "TEMP",
	    "from" : "Farenheit",
		"fromValue": value,
		"to" : "Celsius",
		"toValue" : ((value-32)*(5/9))
        }
    return json.dumps(f2c_dict)

def update(ip):
    if ip is None:
        get_ip = request.remote_addr
        ip = str(ipaddress.IPv4Address(get_ip))
        rec = Billing(ip=ip, temperature = 1, weight = 0, currency = 0, totalCount = 1, cost = 0.05)
        db.session.add(rec)
        db.session.commit()
    else:
        ip.temperature = ip.temperature + 1
        ip.totalCount = ip.totalCount + 1
        ip.cost = ip.cost + 0.05
        db.session.commit()
