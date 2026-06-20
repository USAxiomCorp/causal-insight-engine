# app.py — Render entry point for Causal Insight Engine

import sys
import os
import uvicorn

# Add src to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

if __name__ == "__main__":
    # Get port from environment (Render sets this automatically)
    port = int(os.getenv("PORT", 8000))
    
    # Run the API server
    uvicorn.run(
        "causal_insight.api.server:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Set to True for development only
    )
