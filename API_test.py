import pystac_client
import planetary_computer

from odc.stac import stac_load
import matplotlib.pyplot as plt

lower_left = (40.75, -74.01)
upper_right = (40.88, -73.86)
# lower_left = (12.96, 77.70)
# upper_right = (12.99, 77.71)

# bounds = (min_lon, min_lat, max_lon, max_lat)
bounds = (lower_left[1], lower_left[0], upper_right[1], upper_right[0])

time_window = "2025-01-01/2025-03-01"

stac = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")

search = stac.search(
    bbox=bounds,
    datetime=time_window,
    collections=["sentinel-2-l2a"],
    query={"eo:cloud_cover": {"lt": 30}},
)

items = list(search.get_items())
print('This is the number of scenes that touch our region:',len(items))

signed_items = [planetary_computer.sign(item).to_dict() for item in items]

resolution = 10  # meters per pixel
scale = resolution / 111320.0 # degrees per pixel for crs=4326

data = stac_load(
    items,
    bands=["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B11", "B12"],
    crs="EPSG:4326", # Latitude-Longitude
    resolution=scale, # Degrees
    chunks={"x": 2048, "y": 2048},
    dtype="uint16",
    patch_url=planetary_computer.sign,
    bbox=bounds
)

# Plot sample images from the time series
plot_data = data[["B04","B03","B02"]].to_array()
plot_data.plot.imshow(col='time', col_wrap=4, robust=True, vmin=0, vmax=2500)
plt.savefig(r'C:\Users\anand\Projects\Blazing-Hot\fig')

print('done')