from astropy.coordinates import get_body, solar_system_ephemeris
from astropy.time import Time
import numpy as np
import pandas as pd

# Set time range (example: 2022-06-01 to 2023-01-15)
dates = Time(np.arange(Time('2023-06-01').jd, Time('2027-01-16').jd, 5), format='jd')

# Use JPL ephemeris (usually DE422 or DE440 under the hood)
with solar_system_ephemeris.set('jpl'):
    ra_list = []
    dec_list = []
    date_list = []

    for date in dates:
        jupiter = get_body('jupiter', date)
        ra_list.append(jupiter.ra.hour)   # Right Ascension in hours
        dec_list.append(jupiter.dec.deg)  # Declination in degrees
        date_list.append(date.iso)

# Create and save to CSV
df = pd.DataFrame({
    'date': date_list,
    'ra_hours': ra_list,
    'dec_deg': dec_list
})
df.to_csv("astropy_jupiter_positions.csv", index=False)

import matplotlib.pyplot as plt

# Load your CSV
df = pd.read_csv("astropy_jupiter_positions.csv")

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




