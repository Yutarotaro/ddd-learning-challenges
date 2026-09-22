import argparse
from pathlib import Path

import yaml

from presentation.http.app import app


def main() -> None:
    parser = argparse.ArgumentParser(description="FastAPIのOpenAPI定義をYAMLで出力する")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        yaml.safe_dump(app.openapi(), allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
