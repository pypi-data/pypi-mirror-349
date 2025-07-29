from pathlib import Path

import pandas as pd
import typer
from pysam.libcbcf import VariantFile
from tqdm import tqdm

from tc_utils.core.command import CommandBase, CommandMeta, ToolCategory
from tc_utils.core.registry import CommandRegistry

VCF_FILE_ARG = typer.Argument(..., help="VCF 文件路径")
OUT_FILE_ARG = typer.Argument(..., help="输出csv文件路径")
USE_CN = typer.Option(
    True,
    help="是否输出中文表头",
)


EN_TO_ZH = {
    "ref_hom": "参考纯合",
    "alt_hom": "变异纯合",
    "het": "杂合",
    "total": "总数",
    "similarity": "相似性",
}


def classify_genotype(gt):
    if gt is None or any(allele is None for allele in gt):
        return None
    allele_set = set(gt)
    if len(allele_set) == 1:
        if 0 in allele_set:
            return "ref_hom"
        return "alt_hom"
    else:
        return "het"


def compute_similarity(row: pd.Series) -> float:
    total = row["total"]
    if total == 0:
        return 0
    return (row["ref_hom"] + 0.5 * row["het"]) / total


def analyze_vcf_to_table(vcf_path: Path) -> pd.DataFrame:
    vcf = VariantFile(str(vcf_path))
    stats = {
        sample: {"ref_hom": 0, "alt_hom": 0, "het": 0} for sample in vcf.header.samples
    }

    for rec in tqdm(vcf, desc="Processing VCF"):
        for sample in vcf.header.samples:
            gt = rec.samples[sample].get("GT")
            category = classify_genotype(gt)
            if category:
                stats[sample][category] += 1

    # 整理为 pandas DataFrame
    df = pd.DataFrame.from_dict(stats, orient="index")
    df["total"] = df["ref_hom"] + df["alt_hom"] + df["het"]
    df["similarity"] = df.apply(
        compute_similarity,
        axis=1,
    )

    # 调整列顺序
    df = df[["ref_hom", "alt_hom", "het", "total", "similarity"]]
    return df


@CommandRegistry.register
class GenomeSimilarity(CommandBase):
    """Calculate genome similarity from a VCF file."""

    # 作为类属性定义 meta
    meta = CommandMeta(
        name="genome-similarity",
        category=ToolCategory.VCF,
        description="通过VCF变异位点计算样品与基因组相似性",
        version="1.0.0",
    )

    def execute(
        self,
        vcf_file: Path = VCF_FILE_ARG,
        out_csv: Path = OUT_FILE_ARG,
        use_cn: bool = USE_CN,
    ) -> None:
        """通过VCF变异位点计算样品与基因组相似性."""
        try:
            df = analyze_vcf_to_table(vcf_file)
            if use_cn:
                # 将列名转换为中文
                df.rename(columns=EN_TO_ZH, inplace=True)
            df.to_csv(out_csv, index=True)
            typer.echo(f"结果已保存至: {out_csv}")

        except Exception as e:
            typer.echo(f"处理过程中出现错误: {str(e)}", err=True)
            raise typer.Exit(1)
