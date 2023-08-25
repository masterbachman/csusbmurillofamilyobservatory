from flask import Flask, jsonify
import clr

# Add a reference to the specific path of the ASCOM.DriverAccess.dll
clr.AddReference("C:\\Program Files (x86)\\Common Files\\ASCOM\\.net\\ASCOM.DriverAccess.dll")
clr.AddReference("C:\\Program Files (x86)\\Common Files\\ASCOM\\.net\\ASCOM.Utilities.dll")

from ASCOM.DriverAccess import Camera, Dome, Telescope

app = Flask(__name__)

# Initialize devices at the module level
camera = Camera("ASCOM.Simulator.Camera")
dome = Dome("ASCOM.Simulator.Dome")
telescope = Telescope("ASCOM.Simulator.Telescope")

def ensure_connected(device):
    if not device.Connected:
        try:
            device.Connected = True
        except Exception as e:
            print(f"Error connecting to device: {e}")

@app.route('/status')
def get_status():
    ensure_connected(camera)
    ensure_connected(dome)
    ensure_connected(telescope)
    
    try:
        camera_status = {
            'connected': camera.Connected,
            'camera_name': camera.Description if camera.Connected else "Not connected"
        }

        dome_status = {
            'connected': dome.Connected,
            'dome_name': dome.Description if dome.Connected else "Not connected",
            'dome_azimuth': dome.Azimuth if dome.Connected else None
        }

        telescope_status = {
            'connected': telescope.Connected,
            'mount_name': telescope.Description if telescope.Connected else "Not connected",
            'right_ascension': telescope.RightAscension if telescope.Connected else None,
            'declination': telescope.Declination if telescope.Connected else None
        }


        status = {
            'camera': camera_status,
            'dome': dome_status,
            'telescope': telescope_status
        }

        return jsonify(status), 200

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500

@app.teardown_appcontext
def disconnect_devices(exception=None):
    if camera.Connected:
        camera.Connected = False
    if dome.Connected:
        dome.Connected = False
    if telescope.Connected:
        telescope.Connected = False

if __name__ == '__main__':
    app.run(debug=True)
