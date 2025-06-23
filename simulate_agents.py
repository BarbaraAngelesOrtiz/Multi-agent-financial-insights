import subprocess
import json

def run_agent(name, path):
    print(f"🚀 Running {name}...")
    subprocess.run(["python", path], check=True)
    print(f"✅ {name} finalized.\n")

def show_final_recommendation():
    try:
        with open("data/processed_data.json", "r") as f:
            data = json.load(f)
            print("📊 Agent 3's Final Recommendation:")
            print(json.dumps(data, indent=2))
    except FileNotFoundError:
        print("❌ Final output file not found.")

if __name__ == "__main__":
    print("🌐 Multi-agent simulation started\n")
    
    run_agent("Agent 1 - Download from Alpha Vantage", "agent_1/agent_1_main.py")
    run_agent("Agent 2 - Calculation of indicators", "agent_2/agent_2_main.py")
    run_agent("Agent 3 - Recommendation Generation", "agent_3/agent_3_main.py")
    
    show_final_recommendation()
