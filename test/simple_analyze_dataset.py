#!/usr/bin/env python3
"""
Simple Dataset Analysis Script for NER Training
Analyzes the Label Studio dataset to understand label distribution and data characteristics.
"""

import json
from collections import Counter

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
        percentage = (count / sum(label_counts.values())) * 100
        print(f"  {label}: {count} ({percentage:.1f}%)")
    
    # Text statistics
    if text_lengths:
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
    
    # Class imbalance analysis
    print(f"\nClass Imbalance Analysis:")
    total_entities = sum(label_counts.values())
    most_common = label_counts.most_common()[0][1]
    least_common = label_counts.most_common()[-1][1]
    imbalance_ratio = most_common / least_common if least_common > 0 else float('inf')
    print(f"  Imbalance ratio (most/least common): {imbalance_ratio:.1f}")
    
    # Show some examples
    print(f"\nSample Entities by Label:")
    for label in label_counts.keys():
        examples = []
        for sample in samples_with_entities:
            for entity in sample['entities']:
                if entity['label'] == label and len(examples) < 3:
                    examples.append(entity['text'][:50] + ('...' if len(entity['text']) > 50 else ''))
        if examples:
            print(f"  {label}: {examples}")
    
    return {
        'total_samples': len(data),
        'annotated_samples': annotated_samples,
        'samples_with_entities': len(samples_with_entities),
        'label_counts': label_counts,
        'unique_labels': len(label_counts),
        'total_entities': sum(label_counts.values()),
        'imbalance_ratio': imbalance_ratio
    }

if __name__ == "__main__":
    stats = analyze_dataset("../data/dataset/full/dataset.json")