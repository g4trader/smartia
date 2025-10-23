#!/usr/bin/env python3
"""
Reminder job runner script
Can be executed via Cloud Run jobs, Cloud Scheduler, or cron
"""

import sys
import argparse
import json
from datetime import datetime
from jobs import ReminderJob

def main():
    parser = argparse.ArgumentParser(description="Run reminder jobs")
    parser.add_argument("--job", choices=["24h", "2h", "no-show", "metrics"], required=True,
                       help="Type of job to run")
    parser.add_argument("--output", choices=["json", "text"], default="json",
                       help="Output format")
    
    args = parser.parse_args()
    
    # Initialize job
    job = ReminderJob()
    
    try:
        # Run the specified job
        if args.job == "24h":
            result = job.send_reminders_24h()
        elif args.job == "2h":
            result = job.send_reminders_2h()
        elif args.job == "no-show":
            result = job.handle_no_shows()
        elif args.job == "metrics":
            result = job.get_metrics()
        
        # Output result
        if args.output == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"Job: {result.get('job', 'unknown')}")
            print(f"Timestamp: {result.get('timestamp', 'unknown')}")
            if result.get('success'):
                print("Status: SUCCESS")
                for key, value in result.items():
                    if key not in ['job', 'timestamp', 'success']:
                        print(f"{key}: {value}")
            else:
                print("Status: FAILED")
                print(f"Error: {result.get('error', 'Unknown error')}")
        
        # Exit with appropriate code
        sys.exit(0 if result.get('success', False) else 1)
        
    except Exception as e:
        error_result = {
            "job": args.job,
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "success": False
        }
        
        if args.output == "json":
            print(json.dumps(error_result, indent=2))
        else:
            print(f"Job: {args.job}")
            print("Status: FAILED")
            print(f"Error: {str(e)}")
        
        sys.exit(1)
    
    finally:
        job.close()

if __name__ == "__main__":
    main()
