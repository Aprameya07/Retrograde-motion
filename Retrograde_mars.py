from astropy.coordinates import get_body, solar_system_ephemeris
from astropy.time import Time
import numpy as np
import pandas as pd

# Generate list of dates (June 1, 2022 to mid-Jan 2023)
dates = Time(np.arange(Time('2024-06-01').jd, Time('2026-01-16').jd, 7), format='jd')

# Set ephemeris to JPL (uses high-precision data, typically DE440 or DE422)
with solar_system_ephemeris.set('jpl'):
    ra_list = []
    dec_list = []
    date_list = []

    for date in dates:
        mars = get_body('mars', date)
        ra_list.append(mars.ra.hour)      # RA in hours
        dec_list.append(mars.dec.deg)     # Dec in degrees
        date_list.append(date.iso)

# Create DataFrame and save to CSV
df = pd.DataFrame({
    'date': date_list,
    'ra_hours': ra_list,
    'dec_deg': dec_list
})
df.to_csv("astropy_mars_positions_de422.csv", index=False)

import matplotlib.pyplot as plt

# Load your CSV
df = pd.read_csv("astropy_mars_positions_de422.csv")

# Convert RA if it's in hours
df['ra_deg'] = df['ra_hours'] * 15

# Ensure RA is wrapped within 0–360°
df['ra_deg'] = df['ra_deg'] % 360

plt.figure(figsize=(10, 6))

plt.plot(df['ra_deg'], df['dec_deg'], 'o-', markersize=3, color='deepskyblue', label='Object Path')

# Optional: annotate some key dates
for i in range(0, len(df), max(len(df)//10, 1)):
    plt.annotate(df['date'][i], (df['ra_deg'][i], df['dec_deg'][i]), fontsize=6)

# Invert X-axis to mimic the celestial sphere
plt.gca().invert_xaxis()

plt.xlabel('Right Ascension (degrees)')
plt.ylabel('Declination (degrees)')
plt.title('Simulated Apparent Orbit (RA/Dec Path)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
