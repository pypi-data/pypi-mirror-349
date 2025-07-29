from pathlib import Path

import pandas as pd
import pytest
from hypothesis import given
from hypothesis.strategies import fixed_dictionaries, integers

from tc_utils.tools.vcf.genome_similarity import (
    analyze_vcf_to_table,
    classify_genotype,
    compute_similarity,
)

# -------------------------------
# 单元测试：classify_genotype
# -------------------------------


@pytest.mark.parametrize(
    "gt,expected",
    [
        ((0, 0), "ref_hom"),
        ((1, 1), "alt_hom"),
        ((0, 1), "het"),
        ((1, 0), "het"),
        ((None, None), None),
        ((0, None), None),
        (None, None),
    ],
)
def test_classify_genotype(gt, expected):
    assert classify_genotype(gt) == expected


# -------------------------------
# 单元测试 + hypothesis: compute_similarity
# -------------------------------


@given(
    fixed_dictionaries(
        {
            "ref_hom": integers(min_value=0, max_value=100),
            "alt_hom": integers(min_value=0, max_value=100),
            "het": integers(min_value=0, max_value=100),
        }
    )
)
def test_compute_similarity_with_hypothesis(row_dict):
    row = pd.Series(row_dict)
    row["total"] = row["ref_hom"] + row["alt_hom"] + row["het"]
    sim = compute_similarity(row)
    assert 0.0 <= sim <= 1.0


def test_compute_similarity_zero_total():
    row = pd.Series({"ref_hom": 0, "alt_hom": 0, "het": 0, "total": 0})
    assert compute_similarity(row) == 0


def test_compute_similarity_example():
    row = pd.Series({"ref_hom": 2, "alt_hom": 1, "het": 1, "total": 4})
    assert abs(compute_similarity(row) - 0.625) < 1e-6


# -------------------------------
# 集成测试：analyze_vcf_to_table
# -------------------------------

VCF_HEADER = """\
##fileformat=VCFv4.2
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tsample1\tsample2
"""

VCF_BODY = """\
chr1\t100\t.\tA\tG\t.\t.\t.\tGT\t0/0\t0/1
chr1\t200\t.\tC\tT\t.\t.\t.\tGT\t1/1\t1/1
chr1\t300\t.\tG\tA\t.\t.\t.\tGT\t0/1\t0/0
chr1\t400\t.\tT\tC\t.\t.\t.\tGT\t./.\t0/0
"""


@pytest.fixture
def vcf_file(tmp_path: Path) -> Path:
    vcf_path = tmp_path / "test.vcf"
    with open(vcf_path, "w") as f:
        f.write(VCF_HEADER)
        f.write(VCF_BODY)
    return vcf_path


def test_analyze_vcf_to_table(vcf_file: Path):
    df = analyze_vcf_to_table(vcf_file)

    # 确保列存在
    assert list(df.columns) == ["ref_hom", "alt_hom", "het", "total", "similarity"]
    assert set(df.index) == {"sample1", "sample2"}

    row1 = df.loc["sample1"]
    # sample1: 0/0, 1/1, 0/1, ./.
    # => ref_hom=1, alt_hom=1, het=1
    assert row1["ref_hom"].item() == 1
    assert row1["alt_hom"].item() == 1
    assert row1["het"].item() == 1
    assert row1["total"].item() == 3

    assert abs(row1["similarity"].item() - (1 + 0.5 * 1) / 3) < 1e-6

    row2 = df.loc["sample2"]
    # sample2: 0/1, 1/1, 0/0, 0/0
    # => ref_hom=2, alt_hom=1, het=1
    assert row2["ref_hom"].item() == 2
    assert row2["alt_hom"].item() == 1
    assert row2["het"].item() == 1
    assert row2["total"].item() == 4
    assert abs(row2["similarity"].item() - (2 + 0.5 * 1) / 4) < 1e-6
