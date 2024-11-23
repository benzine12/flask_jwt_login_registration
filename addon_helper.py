import logging
import functools
from collections import defaultdict
from models import IPAddres
from extensions import db

# add to blacklist
def blacklist_ip(ip_address):
    try:
        # Check if the IP address already exists in the database
        existing_ip = IPAddres.query.filter_by(ip_address=ip_address).first()
        if existing_ip:
            if not existing_ip.blacklist:
                existing_ip.blacklist = True
                db.session.commit()
                logging.info(f"IP {ip_address} blacklisted.")
        else:
            # Add the new IP address to the database
            new_ip = IPAddres(ip_address=ip_address, blacklist=True)
            db.session.add(new_ip)
            db.session.commit()
            logging.info(f"IP {ip_address} added to the blacklist.")
    except Exception as e:
        logging.error(f"Error blacklisting IP {ip_address}: {e}")

logger = logging.getLogger(__name__)

# Global error counter
error_counts = defaultdict(lambda: {"401": 0})
ip_409_counts = defaultdict(int)


def FuncLogger(func):
    """
    Python decorator function, FuncLogger, which adds logging functionality to any function it wraps.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        username = None
        # Attempt to log the username if available in the request
        try:
            from flask import request,jsonify

            blacklisted_ip = IPAddres.query.filter_by(ip_address=request.remote_addr, blacklist=True).first()
            if blacklisted_ip:
                logging.warning(f"Blocked request from blacklisted IP: {request.remote_addr}")
                return jsonify({
                    "msg": "Your IP address has been blacklisted due to suspicious activity.",
                    "error": "Forbidden"
                }), 403  # Return HTTP 403 Forbidden
            
            if request.is_json:
                username = request.json.get('username', None)
                if username:
                    logging.info(f"Username provided: {username}")
                else:
                    logging.warning("Username not found in JSON.")
            else:
                logging.warning("Request is not JSON.")
        except Exception as e:
            logging.warning(f"Could not extract username: {e}")

        try:
            # Execute the function
            result = func(*args, **kwargs)

            # Check for tuple response (Response object, status_code)
            from flask import Response
            status_code = None
            if isinstance(result, tuple):
                response, status_code = result
                # logging.debug(f"Response is a tuple: {response}, {status_code}")
            elif isinstance(result, Response):
                response = result
                status_code = response.status_code
            else:
                response = result

            # Handle error status codes
            if status_code == 401 and username:
                error_counts[username]["401"] += 1
                print(f"401 Count for {username}: {error_counts[username]['401']}")
                if error_counts[username]["401"] >= 3:
                    logging.critical(f"Potential BruteForce attack detected on username - {username} from the IP - {request.remote_addr}")
                    blacklist_ip(request.remote_addr)
                    return jsonify({"msg": "Invalid username or password",
                        "error": "Something went wrong"
                        }), 401 # fake error

            elif status_code == 409 and request.remote_addr:
                ip_409_counts[request.remote_addr] += 1
                print(f"409 Count for IP {request.remote_addr}: {ip_409_counts[request.remote_addr]}")
                if ip_409_counts[request.remote_addr] >= 3:
                    logging.critical(f"Potential Username Scraping detected : username - {username} from the IP - {request.remote_addr}")
                    blacklist_ip(request.remote_addr)
                    return jsonify({"msg": "Username already exists",
                            "error": "Something went wrong"
                            }), 409 # fake error

            # Log the return value
            logging.info(f"{func.__name__} returned {response} with status {status_code}")
            return result
        except Exception as e:
            # Log any exceptions raised during function execution
            logging.error(f"{func.__name__} raised an exception: {e}")
            raise  # Re-raise the exception for proper handling
    return wrapper