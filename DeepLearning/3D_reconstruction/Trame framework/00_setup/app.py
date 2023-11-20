from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout

# -----------------------------------------------------------------------------
# Get a server to work with
# -----------------------------------------------------------------------------

server = get_server()
server.client_type = "vue2"

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:
    layout.title.set_text("VasculAR: Cardiac 3D reconstruction")

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
