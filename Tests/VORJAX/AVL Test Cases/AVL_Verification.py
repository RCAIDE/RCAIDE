from pathlib import Path

from RCAIDE.Framework.Interfaces.AVL import parse_avl_file, convert_to_RCAIDE

if __name__ == "__main__":

    # Read in AVL Geometry Files

    avl_path = Path("~/dev/avl3.52/runs/").expanduser()
    avl_test_files = list(avl_path.glob("*.avl"))
    avl_data = {f.stem: parse_avl_file(f) for f in avl_test_files}

    # Eliminate Irrelevant Test Cases

    def filter_test_cases(name):
        keep = True
        if "hershey" in name.lower() or "hersey" in name.lower(): # Exclude Hershey Bar Cases
            keep = False
        if "supra" in name.lower():
            keep = False
        if "bubble" in name.lower():
            keep = False
        if "vanilla" in name.lower():
            keep = False
        if "test" in name.lower():
            keep = False
        if "wing" in name.lower():
            keep = False

        return keep

    avl_data = {k: v for k, v in avl_data.items() if filter_test_cases(v['name'])}

    vehicles = {k: convert_to_RCAIDE(data) for k, data in avl_data.items()}

    print("Done!")