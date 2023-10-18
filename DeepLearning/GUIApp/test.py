import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor

# Create a QApplication instance
app = QApplication([])

# Set the color of the title bar and window frame
palette = QPalette()
palette.setColor(QPalette.Window, QColor("black"))
app.setPalette(palette)

# Create a figure and a plot
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
plt.style.use('dark_background')

# Show the figure
plt.show()
