import os
import pytest

import matplotlib
matplotlib.use("Agg")

from matplotlib.testing.compare import compare_images, ImageComparisonFailure  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

import skyproj  # noqa: E402


ROOT = os.path.abspath(os.path.dirname(__file__))


@pytest.mark.parametrize("lon_0", [0.0, 180.0])
def test_lines_polygons_mcbryde(tmp_path, lon_0):
    """Test drawing lines and polygons."""
    plt.rcParams.update(plt.rcParamsDefault)

    # This code draws a bunch of geodesics and polygons that are
    # both empty and filled, and cross over the boundary, to ensure
    # that features are working as intended.
    fig = plt.figure(1, figsize=(8, 5))
    fig.clf()
    ax = fig.add_subplot(111)
    m = skyproj.McBrydeSkyproj(ax=ax, lon_0=lon_0)

    # Draw two geodesics, one of which will wrap around.
    m.plot([-10., 45.], [-10., 45.], 'r-', label='One')
    m.plot([170., 210.], [-10., 45.], 'b--', label='Two')

    # Draw two unfilled polygons, one of which will wrap around.
    m.draw_polygon([-20, 20, 20, -20], [20, 20, 40, 40],
                   edgecolor='magenta', label='Three')
    m.draw_polygon([160, 200, 200, 160], [20, 20, 40, 40],
                   edgecolor='black', label='Four')

    # Draw two filled polygons, one of which will wrap around.
    m.draw_polygon([-20, 20, 20, -20], [-20, -20, -40, -40],
                   edgecolor='black', facecolor='red', linestyle='--', label='Five')
    m.draw_polygon([160, 200, 200, 160], [-20, -20, -40, -40],
                   edgecolor='red', facecolor='black', linestyle='-', label='Six')
    m.legend()
    fname = f'lines_and_polygons_{lon_0}.png'
    fig.savefig(tmp_path / fname)
    err = compare_images(os.path.join(ROOT, 'data', fname), tmp_path / fname, 10.0)
    if err:
        raise ImageComparisonFailure(err)


@pytest.mark.parametrize("lonlatplonp", [(0.0, 45.0, -90.0),
                                         (100.0, 80.0, -90.0)])
def test_lines_polygons_obmoll(tmp_path, lonlatplonp):
    """Test drawing lines and polygons on an Oblique Mollweide map."""
    plt.rcParams.update(plt.rcParamsDefault)

    lon_0, lat_p, lon_p = lonlatplonp

    # This code draws a bunch of geodesics and polygons that are
    # both empty and filled, and cross over the boundary, to ensure
    # that features are working as intended.
    fig = plt.figure(1, figsize=(8, 5))
    fig.clf()
    ax = fig.add_subplot(111)
    m = skyproj.ObliqueMollweideSkyproj(ax=ax, lon_0=lon_0, lat_p=lat_p, lon_p=lon_p)

    # Draw two geodesics, one of which will wrap around.
    m.plot([-10., 45.], [-10., 45.], 'r-', label='One')
    m.plot([170., 210.], [-10., 45.], 'b--', label='Two')

    # Draw two unfilled polygons, one of which will wrap around.
    m.draw_polygon([-20, 20, 20, -20], [20, 20, 40, 40],
                   edgecolor='magenta', label='Three')
    m.draw_polygon([160, 200, 200, 160], [20, 20, 40, 40],
                   edgecolor='black', label='Four')

    # Draw two filled polygons, one of which will wrap around.
    # Note that wrapped filled polygons do not currently work with oblique transforms.
    m.draw_polygon([-20, 20, 20, -20], [-20, -20, -40, -40],
                   edgecolor='black', facecolor='red', linestyle='--', label='Five')
    m.draw_polygon([160, 200, 200, 160], [-20, -20, -40, -40],
                   edgecolor='red', facecolor='black', linestyle='-', label='Six')

    m.legend()
    fname = f'lines_and_polygons_obmoll_{lon_0}_{lat_p}_{lon_p}.png'
    fig.savefig(tmp_path / fname)
    err = compare_images(os.path.join(ROOT, 'data', fname), tmp_path / fname, 10.0)
    if err:
        raise ImageComparisonFailure(err)
