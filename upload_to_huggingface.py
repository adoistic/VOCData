#!/usr/bin/env python3
"""
Upload VOC Data merged manifests to Hugging Face Datasets.

Usage:
    python3 upload_to_huggingface.py --token YOUR_HF_TOKEN --repo-id your-username/voc-data
"""

import argparse
import os
from pathlib import Path
from huggingface_hub import HfApi, create_repo

def upload_dataset(token, repo_id, data_dir="merged_manifests"):
    """Upload the dataset to Hugging Face."""
    
    # Initialize API
    api = HfApi(token=token)
    
    # Create repository (will not fail if it already exists)
    try:
        create_repo(
            repo_id=repo_id,
            repo_type="dataset",
            token=token,
            private=False,
            exist_ok=True
        )
        print(f"✓ Repository created/verified: https://huggingface.co/datasets/{repo_id}")
    except Exception as e:
        print(f"Error creating repository: {e}")
        return False
    
    # Upload all files from merged_manifests directory
    data_path = Path(data_dir)
    if not data_path.exists():
        print(f"Error: Directory '{data_dir}' not found!")
        return False
    
    print(f"\nUploading files from {data_path}...")
    print("This will take a while for 19GB of data...")
    
    try:
        # Upload the entire folder
        api.upload_folder(
            folder_path=str(data_path),
            repo_id=repo_id,
            repo_type="dataset",
            token=token,
            commit_message="Upload VOC Data IIIF Manifests with Transcriptions"
        )
        print(f"\n✓ Upload complete!")
        print(f"\n🎉 Your dataset is now available at:")
        print(f"   https://huggingface.co/datasets/{repo_id}")
        print(f"\nUsers can access your data with:")
        print(f"   from huggingface_hub import hf_hub_download")
        print(f"   hf_hub_download(repo_id='{repo_id}', filename='combined_all_manifests.json', repo_type='dataset')")
        return True
        
    except Exception as e:
        print(f"Error during upload: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload VOC Data to Hugging Face")
    parser.add_argument("--token", required=True, help="Your Hugging Face API token")
    parser.add_argument("--repo-id", required=True, help="Repository ID (username/repo-name)")
    parser.add_argument("--data-dir", default="merged_manifests", help="Directory containing data files")
    
    args = parser.parse_args()
    
    # Verify data directory exists
    if not os.path.exists(args.data_dir):
        print(f"Error: Data directory '{args.data_dir}' not found!")
        print(f"Current directory: {os.getcwd()}")
        exit(1)
    
    print("=" * 70)
    print("VOC Data - Hugging Face Dataset Uploader")
    print("=" * 70)
    print(f"Repository: {args.repo_id}")
    print(f"Data directory: {args.data_dir}")
    print("=" * 70)
    
    success = upload_dataset(args.token, args.repo_id, args.data_dir)
    exit(0 if success else 1)

