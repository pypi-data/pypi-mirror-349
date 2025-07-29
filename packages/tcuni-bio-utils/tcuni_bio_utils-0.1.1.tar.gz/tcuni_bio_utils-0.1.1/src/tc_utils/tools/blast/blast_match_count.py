"""BLAST match counting and analysis module.

This module provides functionality for processing BLAST output files and
analyzing match statistics. It includes tools for counting matches, filtering
results based on various criteria (match length, identity, gaps), and
calculating match statistics such as best and second-best hits. The module
supports processing of large BLAST output files through chunked reading and
parallel processing.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import pandas as pd
import typer
from tqdm import tqdm

from tc_utils.core.command import CommandBase, CommandMeta, ToolCategory
from tc_utils.core.registry import CommandRegistry

# Define typer arguments at module level
BLAST_DIR_ARG = typer.Argument(..., help="BLAST 结果文件目录")
OUT_FILE_ARG = typer.Argument(..., help="输出文件路径")

# Define typer options at module level
MIN_MATCH_LENGTH_OPTION = typer.Option(24, help="最小匹配长度")
MAX_MATCH_COUNT_OPTION = typer.Option(1, help="最大匹配次数")
PROBE_LENGTH_OPTION = typer.Option(120, help="探针长度")
OUTPUT_ALL_OPTION = typer.Option(False, help="输出所有结果")
SHOW_MAX_LENGTH_OPTION = typer.Option(False, help="显示最大长度")
MIN_IDENTITY_OPTION = typer.Option(None, help="最小一致性")
MAX_MISMATCH_COUNT_OPTION = typer.Option(None, help="最大错配数")
MAX_GAP_COUNT_OPTION = typer.Option(None, help="最大间隔数")


@dataclass
class BlastConfig:
    """BLAST 分析配置类."""

    min_match_length: int = 24
    max_match_count: int = 1
    output_all: bool = False
    show_max_length: bool = False
    min_identity: Optional[int] = None
    max_mismatch_count: Optional[int] = None
    max_gap_count: Optional[int] = None


def get_blast_files(blast_dir: Path) -> List[Path]:
    """获取 BLAST 结果文件列表.

    Args:
        blast_dir: BLAST 结果文件目录

    Returns:
        排序后的文件列表

    Raises:
        typer.Exit: 目录不存在或为空时退出
    """
    if not blast_dir.exists():
        typer.echo(f"目录不存在: {blast_dir}", err=True)
        raise typer.Exit(1)

    files = sorted(blast_dir.glob("*"))
    if not files:
        typer.echo(f"目录为空: {blast_dir}", err=True)
        raise typer.Exit(1)

    return files


def process_blast_file(
    blast_file: Path, config: BlastConfig, chunk_size: int = 10000
) -> pd.DataFrame:
    """处理单个 BLAST 文件.

    Args:
        blast_file: BLAST 文件路径
        config: 分析配置
        chunk_size: 数据块大小

    Returns:
        处理后的数据框
    """
    # 使用 chunks 分块读取大文件
    chunks = pd.read_table(
        blast_file,
        usecols=[0, 2, 4, 5, 6, 7],
        names=[
            "id",
            "identity",
            "mismatch",
            "gapopen",
            "qstart",
            "qend",
        ],
        chunksize=chunk_size,
    )

    blast_dfs = []
    for chunk in chunks:
        chunk["match_len"] = chunk["qend"] - chunk["qstart"] + 1
        if not config.output_all:
            chunk = filter_blast_results(chunk, config)
        blast_dfs.append(chunk)

    return pd.concat(blast_dfs) if blast_dfs else pd.DataFrame()


def filter_blast_results(
    df: pd.DataFrame, config: BlastConfig
) -> pd.DataFrame:
    """根据配置过滤 BLAST 结果.

    Args:
        df: BLAST 结果数据框
        config: 分析配置

    Returns:
        过滤后的数据框
    """
    mask = df["match_len"] >= config.min_match_length

    if config.min_identity is not None:
        mask &= df["identity"] >= config.min_identity
    if config.max_mismatch_count is not None:
        mask &= df["mismatch"] <= config.max_mismatch_count
    if config.max_gap_count is not None:
        mask &= df["gapopen"] <= config.max_gap_count

    return df[mask]


def calculate_match_statistics(
    blast_df: pd.DataFrame, config: BlastConfig
) -> pd.DataFrame:
    """计算匹配统计信息.

    Args:
        blast_df: BLAST 结果数据框
        config: 分析配置

    Returns:
        包含统计信息的数据框
    """
    if blast_df.empty:
        return pd.DataFrame(columns=["id", "blast_match", "second_max_length"])

    # 计算匹配次数
    id_count_df = blast_df["id"].value_counts()
    if not config.output_all:
        id_count_df = id_count_df[id_count_df <= config.max_match_count]
    id_count_df = id_count_df.reset_index()
    id_count_df.columns = ["id", "blast_match"]

    # 计算实际匹配长度
    blast_df = blast_df.groupby("id").head(2).copy()
    blast_df["real_match_length"] = (
        blast_df["match_len"] - blast_df["mismatch"] - blast_df["gapopen"]
    )
    # 计算次优匹配长度
    best_match_idx = blast_df.groupby("id")["real_match_length"].idxmax()
    other_match_df = blast_df[~blast_df.index.isin(best_match_idx)]
    second_max_length_df = (
        other_match_df.groupby("id")["real_match_length"]
        .max()
        .reset_index()
        .rename(columns={"real_match_length": "second_max_length"})
    )

    # 合并结果
    result_df = pd.merge(
        id_count_df, second_max_length_df, on="id", how="left"
    )
    result_df["second_max_length"] = (
        result_df["second_max_length"].fillna(0).astype(int)
    )

    if config.show_max_length:
        max_length_df = (
            blast_df.groupby("id")["real_match_length"]
            .max()
            .reset_index()
            .rename(columns={"real_match_length": "max_length"})
        )
        result_df = pd.merge(result_df, max_length_df, on="id")

    return result_df


@CommandRegistry.register
class BlastCount(CommandBase):
    """Calculate basic statistics for FASTA files."""

    # 作为类属性定义 meta
    meta = CommandMeta(
        name="blast-count",
        category=ToolCategory.ALIGNMENT,
        description="统计blast比对次数, 最大长度",
        version="1.0.0",
    )

    def execute(
        self,
        blast_dir: Path = BLAST_DIR_ARG,
        out_file: Path = OUT_FILE_ARG,
        min_match_length: int = MIN_MATCH_LENGTH_OPTION,
        max_match_count: int = MAX_MATCH_COUNT_OPTION,
        output_all: bool = OUTPUT_ALL_OPTION,
        show_max_length: bool = SHOW_MAX_LENGTH_OPTION,
        min_identity: Optional[int] = MIN_IDENTITY_OPTION,
        max_mismatch_count: Optional[int] = MAX_MISMATCH_COUNT_OPTION,
        max_gap_count: Optional[int] = MAX_GAP_COUNT_OPTION,
    ) -> None:
        """处理 BLAST 结果文件并生成统计报告."""
        try:
            # 初始化配置
            config = BlastConfig(
                min_match_length=min_match_length,
                max_match_count=max_match_count,
                output_all=output_all,
                show_max_length=show_max_length,
                min_identity=min_identity,
                max_mismatch_count=max_mismatch_count,
                max_gap_count=max_gap_count,
            )

            # 获取文件列表
            blast_files = get_blast_files(blast_dir)

            # 处理文件
            with tqdm(blast_files, desc="Processing BLAST files") as pbar:
                for n, blast_file in enumerate(pbar):
                    pbar.set_postfix({"file": blast_file.name})

                    # 处理单个文件
                    blast_df = process_blast_file(blast_file, config)
                    result_df = calculate_match_statistics(blast_df, config)

                    # 写入结果
                    mode = "w" if n == 0 else "a"
                    header = n == 0
                    result_df.to_csv(
                        out_file,
                        sep="\t",
                        index=False,
                        mode=mode,
                        header=header,
                    )

            typer.echo(f"结果已保存至: {out_file}")

        except Exception as e:
            typer.echo(f"处理过程中出现错误: {str(e)}", err=True)
            raise typer.Exit(1)
