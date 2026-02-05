import pandas as pd
import matplotlib.pyplot as plt
import json
import glob
import os
import sys

# --- CONFIGURATION ---
LOG_DIR = "logs"
OUTPUT_DIR = "assets/charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_jsonl(file_path):
    """Load JSONL file and flatten nested latency dict."""
    data = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                record = json.loads(line)
                # Flatten latency_ms
                if "latency_ms" in record:
                    for k, v in record["latency_ms"].items():
                        record[f"latency_{k}"] = v
                    del record["latency_ms"]
                data.append(record)
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return pd.DataFrame()

def plot_single_run(df, run_name="latest"):
    """Generate standard v1.0 plots for a single run."""
    if df.empty:
        print("No data to plot.")
        return

    print(f"Generating plots for {run_name}...")
    
    # 1. End-to-End Latency Over Time
    plt.figure(figsize=(10, 5))
    plt.plot(df['frame'], df['latency_e2e'], label='E2E Latency', color='tab:blue')
    plt.axhline(y=df['latency_e2e'].mean(), color='red', linestyle='--', label=f"Avg: {df['latency_e2e'].mean():.1f}ms")
    plt.xlabel('Frame Index')
    plt.ylabel('Latency (ms)')
    plt.title(f'End-to-End Latency ({run_name})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(f"{OUTPUT_DIR}/latency_e2e_over_time.png")
    plt.close()

    # 2. FPS Over Time
    plt.figure(figsize=(10, 5))
    plt.plot(df['frame'], df['fps'], label='FPS', color='tab:green')
    plt.axhline(y=df['fps'].mean(), color='red', linestyle='--', label=f"Avg: {df['fps'].mean():.1f} FPS")
    plt.xlabel('Frame Index')
    plt.ylabel('FPS')
    plt.title(f'FPS Stability ({run_name})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(f"{OUTPUT_DIR}/fps_over_time.png")
    plt.close()

    # 3. Latency Breakdown (Stacked)
    plt.figure(figsize=(10, 5))
    components = ['latency_inference', 'latency_tracking', 'latency_postprocess']
    # Filter columns that actually exist
    components = [c for c in components if c in df.columns]
    
    plt.stackplot(df['frame'], [df[c] for c in components], labels=[c.replace('latency_', '') for c in components], alpha=0.7)
    plt.xlabel('Frame Index')
    plt.ylabel('Latency (ms)')
    plt.title(f'Latency Breakdown ({run_name})')
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.savefig(f"{OUTPUT_DIR}/latency_breakdown.png")
    plt.close()

    # 4. Memory Usage
    plt.figure(figsize=(10, 5))
    plt.plot(df['frame'], df['memory_mb'], label='Memory (MB)', color='tab:purple')
    plt.xlabel('Frame Index')
    plt.ylabel('Memory (MB)')
    plt.title(f'Memory Footprint ({run_name})')
    plt.grid(True, alpha=0.3)
    plt.savefig(f"{OUTPUT_DIR}/memory_usage.png")
    plt.close()

    # Print Stats
    print("-" * 30)
    print(f"STATS FOR {run_name}")
    print(f"Avg FPS: {df['fps'].mean():.2f}")
    print(f"P50 Latency: {df['latency_e2e'].median():.2f} ms")
    print(f"P95 Latency: {df['latency_e2e'].quantile(0.95):.2f} ms")
    print(f"Peak Memory: {df['memory_mb'].max():.2f} MB")
    print("-" * 30)

def plot_comparison(cpu_df, cuda_df):
    """Generate comparison charts if both logs exist."""
    print("Generating CPU vs CUDA comparison...")

    # FPS Comparison
    plt.figure(figsize=(10, 5))
    plt.plot(cpu_df['frame'], cpu_df['fps'], label='CPU FPS', alpha=0.7)
    plt.plot(cuda_df['frame'], cuda_df['fps'], label='CUDA FPS', alpha=0.7)
    plt.xlabel('Frame Index')
    plt.ylabel('FPS')
    plt.title('Performance Comparison: CPU vs CUDA')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(f"{OUTPUT_DIR}/comparison_fps.png")
    plt.close()

    # Inference Latency Comparison
    plt.figure(figsize=(10, 5))
    plt.plot(cpu_df['frame'], cpu_df['latency_inference'], label='CPU Inference', alpha=0.7)
    plt.plot(cuda_df['frame'], cuda_df['latency_inference'], label='CUDA Inference', alpha=0.7)
    plt.xlabel('Frame Index')
    plt.ylabel('Latency (ms)')
    plt.title('Inference Latency: CPU vs CUDA')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(f"{OUTPUT_DIR}/comparison_inference.png")
    plt.close()

def main():
    # 1. Find latest log
    list_of_files = glob.glob(f'{LOG_DIR}/*.jsonl')
    if not list_of_files:
        print("No logs found in logs/")
        return

    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"Processing latest log: {latest_file}")
    
    df = load_jsonl(latest_file)
    plot_single_run(df, run_name="Latest Run")

    # 2. Check for CPU/CUDA specific logs for comparison
    cpu_log = os.path.join(LOG_DIR, "cpu_run.jsonl")
    cuda_log = os.path.join(LOG_DIR, "cuda_run.jsonl")

    if os.path.exists(cpu_log) and os.path.exists(cuda_log):
        print("\nFound cpu_run.jsonl and cuda_run.jsonl. Generating comparison...")
        cpu_df = load_jsonl(cpu_log)
        cuda_df = load_jsonl(cuda_log)
        plot_comparison(cpu_df, cuda_df)
        
        # Print comparison summary
        print(f"CPU Avg FPS: {cpu_df['fps'].mean():.2f}")
        print(f"CUDA Avg FPS: {cuda_df['fps'].mean():.2f}")
        print(f"Speedup: {cuda_df['fps'].mean() / cpu_df['fps'].mean():.2f}x")

if __name__ == "__main__":
    main()
