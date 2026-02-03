import marimo

__generated_with = "0.10.0"
app = marimo.App(width="full", app_title="SDSS-V Sky Map")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        # SDSS-V Sky Coverage Map

        Interactive all-sky visualization of sources with APOGEE spectra from ApogeeReduction.jl.
        
        - **Projection:** Mollweide (Galactic coordinates)
        - **Interaction:** Pan by dragging, zoom with scroll wheel
        - **Click on a point** to see detailed source information below
        """
    )
    return


@app.cell(hide_code=True)
def _():
    import h5py as h5
    import numpy as np
    import os
    from pathlib import Path
    return Path, h5, np, os


@app.cell(hide_code=True)
def _(Path, os):
    # Configuration - modify DATA_DIR if needed
    DATA_DIR = Path(os.environ.get("DATA_DIR", os.path.expanduser("~/../sdssv/ceph/work/scifest/0.2.0")))
    EXPOSURES_FILE = DATA_DIR / "exposures.h5"
    return DATA_DIR, EXPOSURES_FILE


@app.cell(hide_code=True)
def _():
    # Field name definitions for source data
    SOURCE_IDENTIFIER_FIELDS = (
        "sdss_id", "catalogid", "gaia_dr3_source", "tic_v8", "twomass_designation",
    )
    
    SOURCE_DISPLAY_FIELDS = (
        "gaia_ra", "gaia_dec", "gaia_parallax", "gaia_parallax_error",
        "gaia_pmra", "gaia_pmra_error", "gaia_pmdec", "gaia_pmdec_error",
        "gaia_phot_g_mean_mag", "gaia_phot_bp_mean_mag", "gaia_phot_rp_mean_mag",
        "gaia_radial_velocity", "gaia_radial_velocity_error",
        "gaia_teff_gspphot", "gaia_logg_gspphot", "gaia_mh_gspphot",
        "gaia_distance_gspphot",
        "twomass_j_m", "twomass_h_m", "twomass_k_m",
    )
    return SOURCE_IDENTIFIER_FIELDS, SOURCE_DISPLAY_FIELDS


@app.cell(hide_code=True)
def _(EXPOSURES_FILE, h5, mo, np):
    # Load unique sources from exposures file
    mo.stop(not EXPOSURES_FILE.exists(), mo.md(f"❌ **Error:** Exposures file not found at `{EXPOSURES_FILE}`"))
    
    with h5.File(EXPOSURES_FILE, "r", locking=False) as fp:
        # Load the columns we need for the map
        sdss_id_all = fp["sdss_id"][:]
        ra_all = fp["gaia_ra"][:]
        dec_all = fp["gaia_dec"][:]
    
    # Get unique sources (first occurrence of each sdss_id)
    unique_sdss_ids, unique_indices = np.unique(sdss_id_all, return_index=True)
    
    sdss_id = sdss_id_all[unique_indices]
    ra = ra_all[unique_indices]
    dec = dec_all[unique_indices]
    
    # Filter out invalid coordinates
    valid_mask = np.isfinite(ra) & np.isfinite(dec)
    sdss_id = sdss_id[valid_mask]
    ra = ra[valid_mask]
    dec = dec[valid_mask]
    
    # Build lookup: sdss_id -> count of exposures
    unique_ids, counts = np.unique(sdss_id_all, return_counts=True)
    exposure_counts = dict(zip(unique_ids, counts))
    
    n_sources = len(sdss_id)
    n_total_exposures = len(sdss_id_all)
    
    mo.md(f"""
    **Loaded:** {n_sources:,} unique sources from {n_total_exposures:,} total exposures
    """)
    return (
        dec, exposure_counts, n_sources, n_total_exposures, 
        ra, sdss_id, sdss_id_all, unique_sdss_ids
    )


@app.cell(hide_code=True)
def _(mo, np, ra, dec, sdss_id, n_sources):
    # Prepare data for display, with subsampling if needed
    MAX_POINTS = 100000
    
    if n_sources > MAX_POINTS:
        rng = np.random.default_rng(42)
        sample_idx = rng.choice(n_sources, MAX_POINTS, replace=False)
        display_ra = ra[sample_idx]
        display_dec = dec[sample_idx]
        display_sdss_id = sdss_id[sample_idx]
        display_note = f"Showing {MAX_POINTS:,} of {n_sources:,} sources (random sample)"
    else:
        display_ra = ra
        display_dec = dec
        display_sdss_id = sdss_id
        display_note = f"Showing all {n_sources:,} sources"
    
    # Create JSON for JavaScript
    sources_json = "[\n"
    for i in range(len(display_ra)):
        sources_json += f'  {{"ra": {display_ra[i]:.6f}, "dec": {display_dec[i]:.6f}, "sdss_id": {display_sdss_id[i]}}}'
        if i < len(display_ra) - 1:
            sources_json += ","
        sources_json += "\n"
    sources_json += "]"
    
    mo.md(f"_{display_note}_")
    return sources_json, display_note


@app.cell(hide_code=True)
def _(mo):
    # State for selected source - using a text input that JS can update
    selected_source_input = mo.ui.text(
        value="",
        label="",
        full_width=False,
    )
    # Hide the input - it's just for JS communication
    return (selected_source_input,)


@app.cell(hide_code=True)
def _(mo, sources_json, selected_source_input):
    # Create the Aladin Lite viewer with click handler
    # Bidirectional: click updates input, input change pans map
    
    input_id = selected_source_input._id if hasattr(selected_source_input, '_id') else 'source-selector'
    
    aladin_html = f"""
    <div id="aladin-lite-div" style="width: 100%; height: 650px; border-radius: 8px; overflow: hidden;"></div>
    
    <link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.min.css" />
    <script type="text/javascript" src="https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js" charset="utf-8"></script>
    
    <script type="text/javascript">
    (function() {{
        A.init.then(() => {{
            let aladin = A.aladin('#aladin-lite-div', {{
                survey: 'P/2MASS/color',
                projection: 'MOL',
                cooFrame: 'galactic',
                fov: 360,
                showCooGrid: true,
                showCooGridControl: true,
                showSettingsControl: true,
                showShareControl: false,
                showFullscreenControl: true,
                showLayersControl: true,
                showGotoControl: true,
                showZoomControl: true,
                showFrame: true
            }});
            
            // Store aladin instance globally for input handler
            window.sdssAladin = aladin;
            
            let sourceData = {sources_json};
            
            // Build lookup map: sdss_id -> {{ra, dec}}
            window.sdssSourceLookup = {{}};
            sourceData.forEach(s => {{
                window.sdssSourceLookup[s.sdss_id] = {{ra: s.ra, dec: s.dec}};
            }});
            
            let catalog = A.catalog({{
                name: 'SDSS-V Sources',
                sourceSize: 8,
                color: '#ff6b6b',
                shape: 'circle',
                onClick: 'showTable'
            }});
            
            let sources = sourceData.map(s => {{
                return A.source(s.ra, s.dec, {{
                    sdss_id: s.sdss_id,
                    name: 'SDSS ' + s.sdss_id
                }});
            }});
            
            catalog.addSources(sources);
            aladin.addCatalog(catalog);
            
            // Track if we're updating from a click (to avoid feedback loop)
            window.sdssClickUpdating = false;
            
            // Handle source clicks
            aladin.on('objectClicked', function(object) {{
                if (object && object.data && object.data.sdss_id) {{
                    let sdssId = object.data.sdss_id;
                    window.sdssClickUpdating = true;
                    
                    // Update marimo text input
                    document.querySelectorAll('input[type="text"]').forEach(input => {{
                        if (input.closest('.marimo-ui-text')) {{
                            input.value = String(sdssId);
                            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}
                    }});
                    
                    setTimeout(() => {{ window.sdssClickUpdating = false; }}, 100);
                }}
            }});
            
            // Watch for manual input changes and pan to source
            function setupInputWatcher() {{
                document.querySelectorAll('input[type="text"]').forEach(input => {{
                    if (input.closest('.marimo-ui-text') && !input.dataset.sdssWatching) {{
                        input.dataset.sdssWatching = 'true';
                        
                        input.addEventListener('change', function(e) {{
                            if (window.sdssClickUpdating) return;
                            
                            let sdssId = parseInt(input.value.trim());
                            if (!isNaN(sdssId) && window.sdssSourceLookup[sdssId]) {{
                                let coords = window.sdssSourceLookup[sdssId];
                                window.sdssAladin.gotoRaDec(coords.ra, coords.dec);
                                window.sdssAladin.setFoV(2);  // Zoom to 2 degree FOV
                            }}
                        }});
                        
                        // Also handle Enter key
                        input.addEventListener('keydown', function(e) {{
                            if (e.key === 'Enter') {{
                                if (window.sdssClickUpdating) return;
                                
                                let sdssId = parseInt(input.value.trim());
                                if (!isNaN(sdssId) && window.sdssSourceLookup[sdssId]) {{
                                    let coords = window.sdssSourceLookup[sdssId];
                                    window.sdssAladin.gotoRaDec(coords.ra, coords.dec);
                                    window.sdssAladin.setFoV(2);
                                }}
                            }}
                        }});
                    }}
                }});
            }}
            
            // Setup watcher initially and on DOM changes
            setupInputWatcher();
            new MutationObserver(setupInputWatcher).observe(document.body, {{
                childList: true, subtree: true
            }});
            
            aladin.gotoRaDec(266.417, -29.008);
        }});
    }})();
    </script>
    """
    
    mo.Html(aladin_html)
    return


@app.cell(hide_code=True)
def _(mo, selected_source_input):
    # Show the input for manual entry too
    mo.hstack([
        mo.md("**Enter SDSS ID:**"),
        selected_source_input,
        mo.md("_(press Enter to pan & zoom, or click a point on the map)_")
    ], justify="start", gap=1)
    return


@app.cell(hide_code=True)
def _(mo, selected_source_input):
    # Determine the selected SDSS ID
    selected_sdss_id = None
    if selected_source_input.value:
        try:
            selected_sdss_id = int(selected_source_input.value.strip())
        except (ValueError, AttributeError):
            pass
    
    if selected_sdss_id is None:
        mo.md("_Click on a source in the map above or enter an SDSS ID to see details._")
    return (selected_sdss_id,)


@app.cell(hide_code=True)
def _(mo, n_sources):
    # Note about subsampling
    _max_pts = 100000
    if n_sources > _max_pts:
        mo.md(f"""
        > **Note:** The map shows a random subset of {_max_pts:,} sources for browser performance. 
        > If you enter an SDSS ID that isn't in the displayed subset, the map won't pan to it, 
        > but the details will still load below.
        """)
    return


@app.cell(hide_code=True)
def _(
    EXPOSURES_FILE, SOURCE_DISPLAY_FIELDS, SOURCE_IDENTIFIER_FIELDS,
    exposure_counts, h5, mo, np, sdss_id_all, selected_sdss_id
):
    # Load and display source details when a source is selected
    mo.stop(selected_sdss_id is None)
    
    # Find all indices for this source
    source_indices = np.where(sdss_id_all == selected_sdss_id)[0]
    
    if len(source_indices) == 0:
        mo.stop(True, mo.md(f"⚠️ **SDSS ID {selected_sdss_id} not found in the dataset.**"))
    
    # Load source data from file
    with h5.File(EXPOSURES_FILE, "r", locking=False) as fp:
        source_data = {}
        
        # Load identifier fields (scalar per source)
        for field in SOURCE_IDENTIFIER_FIELDS:
            if field in fp:
                val = fp[field][source_indices[0]]
                if isinstance(val, bytes):
                    val = val.decode('utf-8').strip()
                elif isinstance(val, np.bytes_):
                    val = val.decode('utf-8').strip()
                source_data[field] = val
        
        # Load display fields (scalar per source)
        for field in SOURCE_DISPLAY_FIELDS:
            if field in fp:
                val = fp[field][source_indices[0]]
                if isinstance(val, (np.floating, float)):
                    if not np.isfinite(val):
                        val = None
                source_data[field] = val
        
        # Load exposure-level data
        exposure_data = {}
        for field in ['mjd', 'snr', 'v_rad', 'e_v_rad', 'observatory', 'exposure']:
            if field in fp:
                vals = fp[field][source_indices]
                if len(vals) > 0 and isinstance(vals[0], bytes):
                    vals = [v.decode('utf-8') if isinstance(v, bytes) else str(v) for v in vals]
                exposure_data[field] = vals
    
    n_exposures = len(source_indices)
    return source_data, exposure_data, source_indices, n_exposures


@app.cell(hide_code=True)
def _():
    # Format helper function (defined once, used by multiple cells)
    def format_value(val, decimals=4):
        if val is None:
            return "—"
        if isinstance(val, float):
            if decimals == 0:
                return f"{val:.0f}"
            return f"{val:.{decimals}f}"
        return str(val)
    return (format_value,)


@app.cell(hide_code=True)
def _(mo, n_exposures, selected_sdss_id, source_data):
    # Display source summary
    mo.stop(selected_sdss_id is None)
    
    _ra = source_data.get('gaia_ra')
    _dec = source_data.get('gaia_dec')
    
    # External links
    _links = []
    if _ra is not None and _dec is not None:
        _links.append(f"[SIMBAD](https://simbad.cds.unistra.fr/simbad/sim-coo?Coord={_ra}+{_dec}&Radius=2&Radius.unit=arcsec)")
        _links.append(f"[VizieR](https://vizier.cds.unistra.fr/viz-bin/VizieR-4?-c={_ra}+{_dec}&-c.rs=2)")
    
    _links_str = " · ".join(_links) if _links else ""
    
    mo.md(f"""
    ---
    
    ## Source: SDSS ID {selected_sdss_id}
    
    **{n_exposures} exposure{'s' if n_exposures != 1 else ''}** · {_links_str}
    """)
    return


@app.cell(hide_code=True)
def _(mo, selected_sdss_id, source_data):
    # Identifiers table
    mo.stop(selected_sdss_id is None)
    
    mo.md(f"""
    ### Identifiers
    
    | Field | Value |
    |-------|-------|
    | **SDSS ID** | {source_data.get('sdss_id', '—')} |
    | **Catalog ID** | {source_data.get('catalogid', '—')} |
    | **Gaia DR3** | {source_data.get('gaia_dr3_source', '—')} |
    | **TIC v8** | {source_data.get('tic_v8', '—')} |
    | **2MASS** | {source_data.get('twomass_designation', '—')} |
    """)
    return


@app.cell(hide_code=True)
def _(format_value, mo, selected_sdss_id, source_data):
    # Astrometry and photometry
    mo.stop(selected_sdss_id is None)
    
    mo.md(f"""
    ### Astrometry & Photometry
    
    | Property | Value | Property | Value |
    |----------|-------|----------|-------|
    | **RA** | {format_value(source_data.get('gaia_ra'), 6)}° | **Dec** | {format_value(source_data.get('gaia_dec'), 6)}° |
    | **Parallax** | {format_value(source_data.get('gaia_parallax'), 3)} ± {format_value(source_data.get('gaia_parallax_error'), 3)} mas | **Distance** | {format_value(source_data.get('gaia_distance_gspphot'), 1)} pc |
    | **PM RA** | {format_value(source_data.get('gaia_pmra'), 3)} ± {format_value(source_data.get('gaia_pmra_error'), 3)} mas/yr | **PM Dec** | {format_value(source_data.get('gaia_pmdec'), 3)} ± {format_value(source_data.get('gaia_pmdec_error'), 3)} mas/yr |
    | **G** | {format_value(source_data.get('gaia_phot_g_mean_mag'), 3)} mag | **BP** | {format_value(source_data.get('gaia_phot_bp_mean_mag'), 3)} mag |
    | **RP** | {format_value(source_data.get('gaia_phot_rp_mean_mag'), 3)} mag | **J** | {format_value(source_data.get('twomass_j_m'), 3)} mag |
    | **H** | {format_value(source_data.get('twomass_h_m'), 3)} mag | **K** | {format_value(source_data.get('twomass_k_m'), 3)} mag |
    """)
    return


@app.cell(hide_code=True)
def _(format_value, mo, selected_sdss_id, source_data):
    # Stellar parameters
    mo.stop(selected_sdss_id is None)
    
    mo.md(f"""
    ### Stellar Parameters (Gaia GSP-Phot)
    
    | Parameter | Value | Parameter | Value |
    |-----------|-------|-----------|-------|
    | **Teff** | {format_value(source_data.get('gaia_teff_gspphot'), 0)} K | **log g** | {format_value(source_data.get('gaia_logg_gspphot'), 2)} |
    | **[M/H]** | {format_value(source_data.get('gaia_mh_gspphot'), 2)} | **RV (Gaia)** | {format_value(source_data.get('gaia_radial_velocity'), 2)} ± {format_value(source_data.get('gaia_radial_velocity_error'), 2)} km/s |
    """)
    return


@app.cell(hide_code=True)
def _(exposure_data, mo, np, selected_sdss_id):
    # Exposure table
    mo.stop(selected_sdss_id is None)
    
    import pandas as _pd
    
    # Build exposure DataFrame
    _exp_df_data = {'#': list(range(1, len(exposure_data.get('mjd', [])) + 1))}
    
    _field_labels = {
        'mjd': 'MJD',
        'observatory': 'Obs',
        'exposure': 'Exposure',
        'snr': 'SNR',
        'v_rad': 'v_rad (km/s)',
        'e_v_rad': 'σ_v_rad'
    }
    
    for _field, _label in _field_labels.items():
        if _field in exposure_data:
            _vals = exposure_data[_field]
            if hasattr(_vals, 'tolist'):
                _vals = _vals.tolist()
            # Round floats
            if len(_vals) > 0 and isinstance(_vals[0], (float, np.floating)):
                _vals = [round(v, 2) if np.isfinite(v) else None for v in _vals]
            _exp_df_data[_label] = _vals
    
    _exp_df = _pd.DataFrame(_exp_df_data)
    
    mo.vstack([
        mo.md("### Exposures"),
        mo.ui.table(_exp_df, selection=None, pagination=True, page_size=10)
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ---
        
        ### Map Controls
        
        | Action | How |
        |--------|-----|
        | **Pan** | Click and drag |
        | **Zoom** | Mouse scroll wheel |
        | **Select source** | Click on a point |
        | **Toggle layers** | Layers control (top right) |
        | **Change survey** | Survey selector (bottom) |
        | **Full screen** | Fullscreen button |
        """
    )
    return


if __name__ == "__main__":
    app.run()
