"""Implement tests for BLAST match counting functionality.

This module verifies the BLAST match counting tool's components, including:
- Configuration handling and validation
- BLAST file processing and filtering
- Match length calculations
- Statistical analysis of BLAST results
- Edge cases and error handling
"""

from pathlib import Path

import pandas as pd
import pytest
import typer

from tc_utils.tools.blast.blast_match_count import (
    BlastConfig,
    calculate_match_statistics,
    filter_blast_results,
    get_blast_files,
    process_blast_file,
)


@pytest.fixture
def sample_blast_data():
    """创建示例 BLAST 数据."""
    return pd.DataFrame(
        {
            "id": ["seq1", "seq1", "seq2", "seq3"],
            "identity": [98, 95, 100, 92],
            "match_len": [100, 80, 120, 90],
            "mismatch": [2, 4, 0, 7],
            "gapopen": [0, 1, 0, 1],
        }
    )


@pytest.fixture
def temp_blast_dir(tmp_path):
    """创建临时 BLAST 文件目录."""
    blast_dir = tmp_path / "blast_results"
    blast_dir.mkdir()

    sample_data = (
        "seq1\tgene123\t98.75\t240\t3\t0\t1\t240\t15\t254\t3.2e-120\t432.5\n"
        "seq2\tgene456\t95.32\t320\t12\t2\t5\t324\t10\t325\t1.7e-98\t356.8\n"
        "seq3\tgene789\t99.15\t180\t1\t1\t20\t199\t45\t224\t5.6e-105\t380.2\n"
    )

    test_file = blast_dir / "test1.blast"
    test_file.write_text(sample_data)

    return blast_dir


@pytest.fixture
def blast_config():
    """创建测试配置."""
    return BlastConfig(
        min_match_length=24,
        max_match_count=1,
        output_all=False,
        show_max_length=False,
        min_identity=90,
        max_mismatch_count=5,
        max_gap_count=2,
    )


class TestBlastConfig:
    """Verify BLAST configuration handling and validation.

    Test cases for the BlastConfig class, ensuring proper initialization,
    default values, and custom configuration settings.
    """

    def test_default_values(self):
        """测试配置默认值."""
        config = BlastConfig()
        assert config.min_match_length == 24
        assert config.max_match_count == 1
        assert not config.output_all
        assert not config.show_max_length
        assert config.min_identity is None
        assert config.max_mismatch_count is None
        assert config.max_gap_count is None

    def test_custom_values(self):
        """测试自定义配置值."""
        config = BlastConfig(
            min_match_length=30,
            max_match_count=2,
            output_all=True,
            show_max_length=True,
            min_identity=95,
            max_mismatch_count=3,
            max_gap_count=1,
        )
        assert config.min_match_length == 30
        assert config.max_match_count == 2
        assert config.output_all
        assert config.show_max_length
        assert config.min_identity == 95
        assert config.max_mismatch_count == 3
        assert config.max_gap_count == 1


class TestFileProcessing:
    """Verify BLAST file handling and processing operations.

    Test cases for file system operations, including:
    - BLAST file discovery and validation
    - Directory handling and error cases
    - File content processing and parsing
    """

    def test_get_blast_files(self, temp_blast_dir):
        """测试获取 BLAST 文件列表."""
        files = get_blast_files(temp_blast_dir)
        assert len(files) == 1
        assert files[0].suffix == ".blast"

    def test_get_blast_files_empty_dir(self, tmp_path):
        """测试空目录情况."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        with pytest.raises(typer.Exit):
            get_blast_files(empty_dir)

    def test_get_blast_files_nonexistent_dir(self):
        """测试不存在的目录."""
        with pytest.raises(typer.Exit):
            get_blast_files(Path("/nonexistent/dir"))

    def test_process_blast_file(self, temp_blast_dir, blast_config):
        """测试处理单个 BLAST 文件."""
        blast_file = next(temp_blast_dir.glob("*.blast"))
        result = process_blast_file(blast_file, blast_config)
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        assert all(
            col in result.columns
            for col in ["id", "identity", "match_len", "mismatch", "gapopen"]
        )


class TestCalculations:
    """Verify BLAST result calculation and statistical analysis.

    Test cases for computational operations, including:
    - Match length calculations
    - Result filtering and validation
    - Statistical analysis of matches
    - Edge cases and empty dataset handling
    """

    def test_filter_blast_results(self, sample_blast_data, blast_config):
        """测试 BLAST 结果过滤."""
        filtered_df = filter_blast_results(sample_blast_data, blast_config)
        assert len(filtered_df) <= len(sample_blast_data)
        assert all(filtered_df["match_len"] >= blast_config.min_match_length)
        if blast_config.min_identity:
            assert all(filtered_df["identity"] >= blast_config.min_identity)

    def test_calculate_match_statistics(self, sample_blast_data, blast_config):
        """测试匹配统计计算."""
        result = calculate_match_statistics(sample_blast_data, blast_config)

        assert isinstance(result, pd.DataFrame)
        assert "id" in result.columns
        assert "blast_match" in result.columns
        assert "second_max_length" in result.columns

        # 测试空数据框情况
        empty_df = pd.DataFrame(columns=sample_blast_data.columns)
        empty_result = calculate_match_statistics(empty_df, blast_config)
        assert len(empty_result) == 0
        assert all(
            col in empty_result.columns
            for col in ["id", "blast_match", "second_max_length"]
        )

    def test_calculate_match_statistics_with_max_length(
        self, sample_blast_data, blast_config
    ):
        """测试带最大长度的匹配统计计算."""
        blast_config.show_max_length = True
        result = calculate_match_statistics(sample_blast_data, blast_config)

        assert "max_length" in result.columns
        assert all(result["max_length"] >= result["second_max_length"])
