# Copyright 2024 Google, LLC. This software is provided as-is,
# without warranty or representation for any use or purpose. Your
# use of it is subject to your agreement with Google.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from typing import List, Dict, Any, Optional

AGENT_LATEST_MESSAGE: Optional[str] = None

def add_status_message(message: str) -> None:
    """
    Sets the latest status message and prints to console.
    This message is intended to be accessed by a web endpoint.
    """
    global AGENT_LATEST_MESSAGE
    print(message)  # Log to console
    AGENT_LATEST_MESSAGE = message

def get_status_messages() -> List[str]:
    """Returns the current latest status message as a list."""
    if AGENT_LATEST_MESSAGE is None:
        return []
    return [AGENT_LATEST_MESSAGE]

# Example for serving messages with Flask (optional, can be in a separate server file)
# from flask import Flask, jsonify

# def create_flask_app():
#     app = Flask(__name__)

#     @app.route('/status', methods=['GET'])
#     def status():
#         return jsonify(get_status_messages())

#     return app

# if __name__ == '__main__':
#     # This is for testing the Flask app directly
#     # In a real package, you'd import and run this from a different script
#     # or use a production server like Gunicorn.
#     # For the package, we'll focus on providing the functions.
#     # The Flask app part would be an example of how to use it.
#     # app = create_flask_app()
#     # app.run(debug=True, port=5001) # Example port
#     pass
