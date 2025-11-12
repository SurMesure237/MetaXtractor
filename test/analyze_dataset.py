#!/usr/bin/env python3
"""
Dataset Analysis Script for NER Training
Analyzes the Label Studio dataset to understand label distribution and data characteristics.
"""

import json
import pandas as pd
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_dataset(file_path):
    """Analyze the Label Studio dataset"""
    
    # Load data
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Total samples: {len(data)}")
    
    # Extract annotations
    annotated_samples = 0
    label_counts = Counter()
    text_lengths = []
    entity_lengths = []
    samples_with_entities = []
    
    for item in data:
        text = item['data'].get('text', '')
        text_lengths.append(len(text))
        
        if item.get('annotations') and item['annotations'][0].get('result'):
            annotated_samples += 1
            result = item['annotations'][0]['result']
            
            entities = []
            for annotation in result:
                if annotation.get('type') == 'labels' and 'value' in annotation:
                    value = annotation['value']
                    if all(k in value for k in ['start', 'end', 'text', 'labels']) and value['labels']:
                        label = value['labels'][0]
                        label_counts[label] += 1
                        entity_text = value['text']
                        entity_lengths.append(len(entity_text))
                        entities.append({
                            'label': label,
                            'text': entity_text,
                            'length': len(entity_text)
                        })
            
            if entities:
                samples_with_entities.append({
                    'text': text,
                    'entities': entities,
                    'num_entities': len(entities)
                })
    
    print(f"Annotated samples: {annotated_samples}")
    print(f"Samples with entities: {len(samples_with_entities)}")
    print(f"Unique labels: {len(label_counts)}")
    print(f"Total entities: {sum(label_counts.values())}")
    
    # Label distribution
    print("\nLabel Distribution:")
    for label, count in label_counts.most_common():
        print(f"  {label}: {count}")
    
    # Text statistics
    print(f"\nText Length Statistics:")
    print(f"  Mean: {sum(text_lengths)/len(text_lengths):.1f}")
    print(f"  Min: {min(text_lengths)}")
    print(f"  Max: {max(text_lengths)}")
    
    if entity_lengths:
        print(f"\nEntity Length Statistics:")
        print(f"  Mean: {sum(entity_lengths)/len(entity_lengths):.1f}")
        print(f"  Min: {min(entity_lengths)}")
        print(f"  Max: {max(entity_lengths)}")
    
    # Entities per sample
    entities_per_sample = [item['num_entities'] for item in samples_with_entities]
    if entities_per_sample:
        print(f"\nEntities per Sample:")
        print(f"  Mean: {sum(entities_per_sample)/len(entities_per_sample):.1f}")
        print(f"  Min: {min(entities_per_sample)}")
        print(f"  Max: {max(entities_per_sample)}")
    
    # Create visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Label distribution
    labels, counts = zip(*label_counts.most_common())
    axes[0, 0].bar(range(len(labels)), counts)
    axes[0, 0].set_xticks(range(len(labels)))
    axes[0, 0].set_xticklabels(labels, rotation=45, ha='right')
    axes[0, 0].set_title('Label Distribution')
    axes[0, 0].set_ylabel('Count')
    
    # Text length distribution
    axes[0, 1].hist(text_lengths, bins=50, alpha=0.7)
    axes[0, 1].set_title('Text Length Distribution')
    axes[0, 1].set_xlabel('Text Length (characters)')
    axes[0, 1].set_ylabel('Frequency')
    
    # Entity length distribution
    if entity_lengths:
        axes[1, 0].hist(entity_lengths, bins=30, alpha=0.7)
        axes[1, 0].set_title('Entity Length Distribution')
        axes[1, 0].set_xlabel('Entity Length (characters)')
        axes[1, 0].set_ylabel('Frequency')
    
    # Entities per sample
    if entities_per_sample:
        axes[1, 1].hist(entities_per_sample, bins=max(entities_per_sample), alpha=0.7)
        axes[1, 1].set_title('Entities per Sample Distribution')
        axes[1, 1].set_xlabel('Number of Entities')
        axes[1, 1].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig('dataset_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return {
        'total_samples': len(data),
        'annotated_samples': annotated_samples,
        'samples_with_entities': len(samples_with_entities),
        'label_counts': label_counts,
        'unique_labels': len(label_counts),
        'total_entities': sum(label_counts.values()),
        'text_lengths': text_lengths,
        'entity_lengths': entity_lengths,
        'entities_per_sample': entities_per_sample
    }

if __name__ == "__main__":
    stats = analyze_dataset("data/dataset/full/dataset.json")