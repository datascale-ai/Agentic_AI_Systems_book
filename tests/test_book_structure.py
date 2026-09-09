from pathlib import Path
import re
import tomllib

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

EXPECTED_PARTS = {
    1: (1, 4), 2: (5, 8), 3: (9, 13), 4: (14, 17), 5: (18, 21),
    6: (22, 25), 7: (26, 30), 8: (31, 35), 9: (36, 39),
}
EXPECTED_OWNERS = {
    **{n: "A" for n in (1, 2, 3, 4, 26, 27)},
    **{n: "B" for n in (5, 6, 7, 8, 28, 29, 30)},
    **{n: "C" for n in (9, 10, 11, 12, 13, 31, 32)},
    **{n: "D" for n in (14, 15, 16, 17, 33, 34, 35)},
    **{n: "E" for n in (18, 19, 20, 21, 36, 37)},
    **{n: "F" for n in (22, 23, 24, 25, 38, 39)},
}


def chapter_files(locale: str):
    return sorted((DOCS / locale).glob("part*/ch*.md"))


def test_bilingual_chapter_set_is_complete_and_aligned():
    zh = chapter_files("zh")
    en = chapter_files("en")
    assert len(zh) == len(en) == 39
    assert {p.relative_to(DOCS / "zh") for p in zh} == {
        p.relative_to(DOCS / "en") for p in en
    }
    numbers = [int(re.search(r"ch(\d{2})_", p.name).group(1)) for p in zh]
    assert numbers == list(range(1, 40))


def test_part_boundaries_and_owner_continuity():
    for part, (start, end) in EXPECTED_PARTS.items():
        files = sorted((DOCS / "zh" / f"part{part}").glob("ch*.md"))
        nums = [int(re.search(r"ch(\d{2})_", p.name).group(1)) for p in files]
        assert nums == list(range(start, end + 1))
        for path in files:
            number = int(re.search(r"ch(\d{2})_", path.name).group(1))
            text = path.read_text(encoding="utf-8")
            assert f'owner: "{EXPECTED_OWNERS[number]}"' in text
            assert "Writing scaffold" not in text  # Chinese source has Chinese marker
            assert len(text.strip()) > 500


def test_front_matter_appendices_and_public_assets_exist():
    required = {
        "index.md", "preface.md", "reader_guide.md", "abbreviations.md",
        "authors.md", "figures_tables.md", "asset_contract.md", "acknowledgements.md",
        "afterword.md",
        "appendix_a_terms.md", "appendix_b_metrics.md", "appendix_c_schemas.md",
        "appendix_d_deployment.md", "appendix_e_config.md", "appendix_f_security.md",
        "appendix_g_failures.md", "appendix_h_reading.md",
    }
    for locale in ("zh", "en"):
        actual = {p.name for p in (DOCS / locale).glob("*.md")}
        assert required <= actual


def test_mkdocs_config_and_python_project_metadata_are_valid():
    config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
    assert config["theme"]["name"] == "material"
    assert config["plugins"][-1]["i18n"]["languages"][0]["locale"] == "zh"
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert project["project"]["name"] == "agentic-ai-systems-book"
    assert project["project"]["requires-python"] == ">=3.11"


def test_private_materials_are_ignored():
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for pattern in ("private_materials/", "editorial/", "*.pdf", "学生任务单/"):
        assert pattern in ignore
