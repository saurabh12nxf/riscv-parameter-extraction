#!/usr/bin/env python3
"""
LLM Parameter Extraction Comparison Script

This script compares LLM-extracted parameters against the RISC-V Unified Database
ground truth to calculate accuracy metrics.

Usage:
    python compare_with_udb.py --llm-output experiments/chatgpt4_results.json \
                                --udb-file ../riscv-unified-db/spec/std/isa/csr/mstatus.yaml \
                                --report analysis/accuracy_report.md
"""

import json
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Set
from dataclasses import dataclass


@dataclass
class Parameter:
    """Represents a single architectural parameter"""
    name: str
    bit_range: str
    type: str  # NAMED, UNNAMED, CONFIG_DEPENDENT
    config_dependency: str = None
    description: str = ""
    confidence: int = 100


@dataclass
class ComparisonResult:
    """Results of comparing LLM output with UDB ground truth"""
    total_udb_params: int
    total_llm_params: int
    correctly_identified: List[str]
    missed: List[str]
    hallucinations: List[str]
    misclassified: List[Dict]
    precision: float
    recall: float
    f1_score: float


def load_udb_yaml(filepath: Path) -> Dict:
    """Load and parse UDB YAML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_llm_output(filepath: Path) -> Dict:
    """Load LLM JSON output"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_udb_parameters(udb_data: Dict) -> List[Parameter]:
    """Extract parameters from UDB YAML structure"""
    parameters = []
    
    if 'fields' not in udb_data:
        return parameters
    
    for field_name, field_data in udb_data['fields'].items():
        # Determine if config-dependent
        config_dep = None
        param_type = "NAMED"
        
        if 'definedBy' in field_data:
            config_dep = str(field_data['definedBy'])
            param_type = "CONFIG_DEPENDENT"
        
        # Get bit location
        bit_range = field_data.get('location', '')
        if not bit_range:
            # Check for RV32/RV64 specific locations
            loc_rv32 = field_data.get('location_rv32', '')
            loc_rv64 = field_data.get('location_rv64', '')
            bit_range = f"RV32:{loc_rv32}, RV64:{loc_rv64}" if loc_rv32 or loc_rv64 else "unknown"
        
        parameters.append(Parameter(
            name=field_name,
            bit_range=str(bit_range),
            type=param_type,
            config_dependency=config_dep,
            description=field_data.get('description', '').strip()[:100]
        ))
    
    return parameters


def extract_llm_parameters(llm_data: Dict) -> List[Parameter]:
    """Extract parameters from LLM JSON output"""
    parameters = []
    
    for param_data in llm_data.get('parameters', []):
        parameters.append(Parameter(
            name=param_data['name'],
            bit_range=f"RV32:{param_data.get('bit_range_rv32', 'N/A')}, RV64:{param_data.get('bit_range_rv64', 'N/A')}",
            type=param_data['type'],
            config_dependency=param_data.get('config_dependency'),
            description=param_data.get('description', '')[:100],
            confidence=param_data.get('confidence', 100)
        ))
    
    return parameters


def compare_parameters(udb_params: List[Parameter], llm_params: List[Parameter]) -> ComparisonResult:
    """Compare LLM parameters against UDB ground truth"""
    
    udb_names = {p.name for p in udb_params}
    llm_names = {p.name for p in llm_params}
    
    # Calculate matches
    correctly_identified = list(udb_names & llm_names)
    missed = list(udb_names - llm_names)
    hallucinations = list(llm_names - udb_names)
    
    # Check for misclassifications
    misclassified = []
    udb_dict = {p.name: p for p in udb_params}
    llm_dict = {p.name: p for p in llm_params}
    
    for name in correctly_identified:
        udb_param = udb_dict[name]
        llm_param = llm_dict[name]
        
        if udb_param.type != llm_param.type:
            misclassified.append({
                'name': name,
                'udb_type': udb_param.type,
                'llm_type': llm_param.type,
                'confidence': llm_param.confidence
            })
    
    # Calculate metrics
    true_positives = len(correctly_identified)
    false_positives = len(hallucinations)
    false_negatives = len(missed)
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return ComparisonResult(
        total_udb_params=len(udb_params),
        total_llm_params=len(llm_params),
        correctly_identified=correctly_identified,
        missed=missed,
        hallucinations=hallucinations,
        misclassified=misclassified,
        precision=precision,
        recall=recall,
        f1_score=f1_score
    )


def generate_report(result: ComparisonResult, llm_name: str, output_path: Path):
    """Generate markdown report of comparison results"""
    
    report = f"""# LLM Parameter Extraction Accuracy Report

## LLM: {llm_name}

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total UDB Parameters | {result.total_udb_params} |
| Total LLM Parameters | {result.total_llm_params} |
| Correctly Identified | {len(result.correctly_identified)} |
| Missed | {len(result.missed)} |
| Hallucinations | {len(result.hallucinations)} |
| Misclassified | {len(result.misclassified)} |
| **Precision** | **{result.precision:.2%}** |
| **Recall** | **{result.recall:.2%}** |
| **F1 Score** | **{result.f1_score:.3f}** |

## Correctly Identified Parameters ({len(result.correctly_identified)})

{chr(10).join(f"- {name}" for name in sorted(result.correctly_identified))}

## Missed Parameters ({len(result.missed)})

{chr(10).join(f"- {name}" for name in sorted(result.missed))}

## Hallucinations ({len(result.hallucinations)})

{chr(10).join(f"- {name}" for name in sorted(result.hallucinations))}

## Misclassifications ({len(result.misclassified)})

{chr(10).join(f"- **{m['name']}**: UDB={m['udb_type']}, LLM={m['llm_type']} (confidence: {m['confidence']}%)" for m in result.misclassified)}

## Analysis

### Strengths
- Precision of {result.precision:.1%} indicates low hallucination rate
- Recall of {result.recall:.1%} shows good coverage of actual parameters

### Weaknesses
- Missed {len(result.missed)} parameters ({len(result.missed)/result.total_udb_params:.1%} of total)
- {len(result.hallucinations)} hallucinated parameters need filtering

### Recommendations
1. Add negative examples for hallucinated parameters
2. Provide UDB examples for missed parameters in few-shot learning
3. Refine prompt to reduce misclassifications

---
*Generated by compare_with_udb.py*
"""
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Report generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Compare LLM parameter extraction with UDB ground truth')
    parser.add_argument('--llm-output', type=Path, required=True, help='Path to LLM JSON output file')
    parser.add_argument('--udb-file', type=Path, required=True, help='Path to UDB YAML file')
    parser.add_argument('--report', type=Path, required=True, help='Output path for markdown report')
    parser.add_argument('--llm-name', type=str, default='Unknown LLM', help='Name of the LLM tested')
    
    args = parser.parse_args()
    
    # Load data
    print(f"📂 Loading UDB file: {args.udb_file}")
    udb_data = load_udb_yaml(args.udb_file)
    udb_params = extract_udb_parameters(udb_data)
    print(f"   Found {len(udb_params)} parameters in UDB")
    
    print(f"📂 Loading LLM output: {args.llm_output}")
    llm_data = load_llm_output(args.llm_output)
    llm_params = extract_llm_parameters(llm_data)
    print(f"   Found {len(llm_params)} parameters in LLM output")
    
    # Compare
    print("🔍 Comparing parameters...")
    result = compare_parameters(udb_params, llm_params)
    
    # Display results
    print(f"\n📊 Results:")
    print(f"   Precision: {result.precision:.2%}")
    print(f"   Recall: {result.recall:.2%}")
    print(f"   F1 Score: {result.f1_score:.3f}")
    print(f"   Correctly Identified: {len(result.correctly_identified)}/{result.total_udb_params}")
    print(f"   Missed: {len(result.missed)}")
    print(f"   Hallucinations: {len(result.hallucinations)}")
    
    # Generate report
    print(f"\n📝 Generating report...")
    generate_report(result, args.llm_name, args.report)
    
    print("\n✨ Done!")


if __name__ == '__main__':
    main()
