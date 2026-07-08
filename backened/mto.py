"""
mto.py

Generate Material Take-Off from AI extracted data.
"""

from typing import Dict, List


def add_item(mto, item, description, size, quantity):
    mto.append({
        "Item": item,
        "Description": description,
        "Size": size,
        "Quantity": quantity
    })


def generate_mto(ai_data: Dict):

    print("\n========== AI DATA RECEIVED ==========")
    print(ai_data)

    mto = []

    pipe_size = ai_data.get("pipe_size") or "Unknown"

    material = ai_data.get("material") or "Unknown"

    pipe_length = ai_data.get("pipe_length") or "Unknown"

    # Pipe
    add_item(
        mto,
        "Pipe",
        material,
        pipe_size,
        pipe_length
    )

    # Valves
    valves = ai_data.get("valves", [])

    if isinstance(valves, list):
        for valve in valves:
            add_item(
                mto,
                "Valve",
                valve,
                pipe_size,
                1
            )

    # Components
    components = [
        ("Elbow", ai_data.get("elbows", 0)),
        ("Tee", ai_data.get("tees", 0)),
        ("Reducer", ai_data.get("reducers", 0)),
        ("Flange", ai_data.get("flanges", 0)),
        ("Support", ai_data.get("supports", 0)),
        ("Gasket", ai_data.get("gaskets", 0)),
        ("Bolt", ai_data.get("bolts", 0)),
        ("Nut", ai_data.get("nuts", 0)),
    ]

    for component, qty in components:

        try:
            qty = int(qty)
        except:
            qty = 0

        if qty > 0:
            add_item(
                mto,
                component,
                component,
                pipe_size,
                qty
            )

    print("\n========== GENERATED MTO ==========")
    print(mto)

    return mto