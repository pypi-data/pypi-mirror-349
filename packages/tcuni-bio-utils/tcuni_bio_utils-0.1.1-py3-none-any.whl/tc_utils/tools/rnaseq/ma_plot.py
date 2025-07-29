"""MA plot generation module for RNA-seq analysis.

This module implements functionality for creating MA plots (Mean-Difference
plots) from RNA-seq differential expression data. It processes EdgeR output
files to visualize the relationship between mean expression levels and log
fold changes, helping identify differentially expressed genes. The plots
include categorization of genes based on significance and fold change
thresholds.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import typer

from tc_utils.core.command import CommandBase, CommandMeta, ToolCategory
from tc_utils.core.registry import CommandRegistry

EDGER_INPUT = typer.Argument(..., help="EdgeR结果文件路径")
OUTDIR = typer.Argument(..., help="输出目录")


@dataclass
class MaPlotConfig:
    """Configuration settings for MA plot generation.

    This class defines the configuration parameters for MA plot visualization,
    including column specifications, plot categories and their colors, figure
    dimensions, and display settings.

    Attributes:
        ANN_COLS: List of column names for gene annotations and statistics
        PLOT_CATEGORIES: List of tuples defining categories and their colors
        FIGURE_SIZE: Tuple of width and height for the plot
        DPI: Resolution (dots per inch) for saved images
        ALPHA: Transparency level for plot elements
        POINT_SIZE: Size of scatter plot points
    """

    ANN_COLS = [
        "Gene_ID",
        "Locus",
        "gene_name",
        "gene_description",
        "logFC",
        "PValue",
        "FDR",
    ]
    PLOT_CATEGORIES = [
        ("Up", "red"),
        ("Down", "blue"),
        ("Normal", "gray"),
    ]
    FIGURE_SIZE = (8, 6)
    DPI = 300
    ALPHA = 0.6
    POINT_SIZE = 20


def prepare_data(df: pd.DataFrame, exp_cols: List[str]) -> pd.DataFrame:
    """准备绘图数据，添加分类标签."""
    df = df.copy()
    # 计算log TPM
    df["log_tpm"] = df[exp_cols].mean(1).map(lambda x: np.log10(x + 1))

    # 设置类别
    sig_mask = df["FDR"] <= 0.05
    up_mask = df["logFC"] >= 1
    down_mask = df["logFC"] <= -1

    df["Category"] = "Normal"
    df.loc[sig_mask & up_mask, "Category"] = "Up"
    df.loc[sig_mask & down_mask, "Category"] = "Down"

    return df


def plot(df: pd.DataFrame, out_prefix: Path) -> None:
    """绘制MA图并保存."""
    plt.style.use("default")
    _, ax = plt.subplots(figsize=MaPlotConfig.FIGURE_SIZE)

    # 绘制散点图
    for category, color in MaPlotConfig.PLOT_CATEGORIES:
        subset = df[df["Category"] == category]
        subset.plot.scatter(
            x="log_tpm",
            y="logFC",
            c=color,
            s=MaPlotConfig.POINT_SIZE,
            label=category,
            ax=ax,
        )

    # 设置图形属性
    ax.set_title("MA plot")
    ax.set_xlabel("log10(TPM)")
    ax.set_ylabel("log2(FC)")

    # 添加图例
    ax.legend(title="Category")

    # 保存图形
    plt.tight_layout()

    # 保存不同格式
    for ext in [".png", ".pdf"]:
        out_path = out_prefix.with_suffix(f".MAplot{ext}")
        try:
            if ext == ".png":
                plt.savefig(
                    out_path, dpi=MaPlotConfig.DPI, bbox_inches="tight"
                )
            else:
                plt.savefig(out_path, bbox_inches="tight")
        except Exception as e:
            typer.echo(f"Error saving {out_path}: {e}", err=True)

    plt.close()


@CommandRegistry.register
class MaPlot(CommandBase):
    """Calculate basic statistics for FASTA files."""

    # 作为类属性定义 meta
    meta = CommandMeta(
        name="ma-plot",
        category=ToolCategory.RNASEQ,
        description="使用edgeR差异分析表格绘制MAplot",
        version="1.0.0",
    )

    def execute(
        self,
        edger_input: Path = EDGER_INPUT,
        outdir: Path = OUTDIR,
    ) -> None:
        """处理EdgeR结果文件并生成MA图."""
        # 检查输入文件
        if not edger_input.exists():
            raise typer.BadParameter(f"输入文件不存在: {edger_input}")

        # 确保输出目录存在
        outdir.mkdir(parents=True, exist_ok=True)

        try:
            # 读取数据
            df = pd.read_csv(edger_input, sep="\t")

            # 获取表达量列名
            exp_cols = [
                col for col in df.columns if col not in MaPlotConfig.ANN_COLS
            ]
            if not exp_cols:
                raise ValueError("未找到表达量数据列")

            # 准备数据
            df = prepare_data(df, exp_cols)

            # 设置输出路径
            out_prefix = outdir / edger_input.stem

            # 绘图
            plot(df, out_prefix)

            typer.echo(f"MA图已保存至: {out_prefix}.MAplot.png/pdf")

        except Exception as e:
            typer.echo(f"处理过程中出错: {e}", err=True)
            raise typer.Exit(1)
