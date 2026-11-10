import rasterio
import numpy as np

def calculate_ndvi(red_path, nir_path, out_path):
    with rasterio.open(red_path) as src_red:
        red = src_red.read(1).astype(np.float32)
        meta = src_red.profile

    with rasterio.open(nir_path) as src_nir:
        nir = src_nir.read(1).astype(np.float32)

    np.seterr(divide='ignore', invalid='ignore')
    ndvi = (nir - red) / (nir + red)
    ndvi = np.nan_to_num(ndvi, nan=0.0, posinf=0.0, neginf=0.0)

    meta.update(dtype=rasterio.float32, count=1)

    with rasterio.open(out_path, 'w', **meta) as dst:
        dst.write(ndvi.astype(rasterio.float32), 1)

if __name__ == "__main__":
    calculate_ndvi("red.tif", "nir.tif", "ndvi_out.tif")
