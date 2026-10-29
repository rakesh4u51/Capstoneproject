"""Platform entry point."""

from dotenv import load_dotenv

from bfsi.batch_fraud import run_batch
from bfsi.transactions import process

load_dotenv()


def main():
    print("=== End-to-end banking workflow ===")
    settled = process("R1001", "C5001", "Asha Rao", "AC5001", "AC5002", 750.0, "IN")
    print("  R1001:", settled["status"])

    blocked = process("R1002", "C5002", "Ivan Petrov", "AC5002", "AC5001", 5000.0, "RU")
    print("  R1002:", blocked["status"], "->", blocked.get("reason"))

    print("=== Batch fraud pipeline ===")
    for item in run_batch():
        print(f"  {item['id']}: risk={item['risk']} ({item['engine']})")


if __name__ == "__main__":
    main()
