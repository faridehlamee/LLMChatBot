import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from business_config import SYSTEM_PROMPT_TEMPLATE
    print("SUCCESS: Business config loaded successfully!")
    print(f"System prompt length: {len(SYSTEM_PROMPT_TEMPLATE)} characters")
    print(f"First 200 chars: {SYSTEM_PROMPT_TEMPLATE[:200]}...")
except Exception as e:
    print(f"ERROR: Error loading business config: {e}")
