from flask import Blueprint
from flask_socketio import SocketIO
from app.views.game_state import init, update_health, inventory_update, update_xp
from app.views.create import create_player, create_save, create_item
from flaskTests import delete_player, delete_save, delete_item, delete_inventory_slot
from app.views.generate_rooms import dummy_room

socketio = SocketIO()
main = Blueprint("main", __name__)

# example of using the rest api (this should be removed at some point, all endpoints should be made in the views folder
@main.route("/", methods=['GET'])
def default():
    return "<p> Hello World! </p>"

# websocket endpoints
socketio.on_event("create_player", create_player)
socketio.on_event("create_save", create_save)
socketio.on_event("create_item", create_item)
socketio.on_event("update_inventory", inventory_update)
socketio.on_event("init", init)
socketio.on_event("update_health", update_health)
socketio.on_event("update_xp", update_xp)

# test websockets that'll likely never be used ouside of testing
socketio.on_event("delete_player", delete_player)
socketio.on_event("delete_save", delete_save)
socketio.on_event("delete_inventory_slot", delete_inventory_slot)
socketio.on_event("delete_item", delete_item)

main.add_url_rule('/rooms/<int:id>', view_func=dummy_room)
