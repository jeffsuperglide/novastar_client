from collections import defaultdict

input_path = "/Users/rdcrljsg/Documents/repositories/novastar_client/stations_returned_data.md"  # station, tag, parameter, interval, name
output_toml = (
    "/Users/rdcrljsg/Documents/repositories/novastar_client/stations_returned_data.out"
)


def split_markdown_row(line):
    # Strip leading/trailing whitespace and '|' characters, then split
    line = line.strip()
    if not line or not line.startswith("|"):
        return None
    # Remove leading and trailing '|' then split on '|'
    parts = line.strip("|").split("|")
    # Strip spaces inside each cell
    parts = [p.strip() for p in parts]
    return parts


stations = defaultdict(lambda: {"description": None, "series": []})

with open(input_path, encoding="utf-8") as f:
    # Skip the very first line (header titles)
    next(f, None)

    for line in f:
        # Skip the markdown separator line (e.g. "| :----: | :--- | ...")
        # if ":" in line and "---" in line:
        #     continue

        cells = split_markdown_row(line)
        if not cells:
            continue

        # Adjust these indices if your column order differs
        station_id = cells[0]
        station_tag = cells[1]
        parameter_full = cells[2]  # e.g. "Precip-Total"
        interval = cells[3]  # e.g. "5Minute"
        station_name = cells[4]

        # derive parameter/statistic from "Precip-Total"
        if "-" in parameter_full:
            base, stat = parameter_full.split("-", 1)
        else:
            base, stat = parameter_full, ""

        # pick units
        base_lower = base.lower()
        if "precip" in base_lower:
            units = "mm"
        elif "waterlevel" in base_lower or "level" in base_lower:
            units = "ft"
        elif "discharge" in base_lower or "flow" in base_lower:
            units = "cfs"
        else:
            units = "ft"  # fallback if something unexpected

        st = stations[station_id]
        if st["description"] is None:
            st["description"] = station_name

        st["series"].append(
            {
                "tag": station_tag,
                "parameter": base,
                "statistic": stat,
                "interval": interval,
                "units": units,
            }
        )

with open(output_toml, "w", encoding="utf-8") as out:
    out.write("# Generated NovaStar5 time series configuration\n\n")
    for sid, data in sorted(stations.items(), key=lambda x: int(x[0])):
        out.write(f'[station."{sid}"]\n')
        out.write('network = "NovaStar5"\n')
        out.write(f'description = "{data["description"]}"\n\n')
        for s in data["series"]:
            out.write(f'  [[station."{sid}".series]]\n')
            tag = s["tag"]
            out.write(f'  tag       = "{tag}"\n')
            out.write(f'  parameter = "{s["parameter"]}"\n')
            out.write(f'  statistic = "{s["statistic"]}"\n')
            out.write(f'  interval  = "{s["interval"]}"\n')
            out.write(f'  units     = "{s["units"]}"\n')
            out.write("  enabled   = true\n\n")
