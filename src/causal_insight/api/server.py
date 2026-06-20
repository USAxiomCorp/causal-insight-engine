"""
═══════════════════════════════════════════════════════════════════════════════
CAUSAL INSIGHT ENGINE API — WAD-GROUNDED REST API
═══════════════════════════════════════════════════════════════════════════════
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
import uvicorn
import logging

from ..core.constitution import *
from ..domains.clinical_trials import ClinicalTrialSimulator

# ═══════════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS — REQUEST/RESPONSE SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class TrialSimulationRequest(BaseModel):
    """Request for trial simulation."""
    dosing: float = 1.0
    n_patients: int = 1000

class TrialSimulationResponse(BaseModel):
    """Response from trial simulation."""
    efficacy: float
    safety: float
    survival: float
    efficacy_wad: int
    safety_wad: int
    survival_wad: int
    confidence: float
    confidence_wad: int
    dosing: float
    n_patients: int

class DosingOptimizationRequest(BaseModel):
    """Request for dosing optimization."""
    efficacy_weight: float = 0.5
    safety_weight: float = 0.5
    n_patients: int = 1000

class DosingOptimizationResponse(BaseModel):
    """Response from dosing optimization."""
    optimal_dose: float
    optimal_score_wad: int
    optimal_score: float
    recommendation: str
    confidence_wad: int
    results: List[Dict[str, Any]]

class PredictionRequest(BaseModel):
    """Request for outcome prediction."""
    intervention: Dict[str, float]
    target_variable: str = "efficacy_endpoint"

class PredictionResponse(BaseModel):
    """Response from outcome prediction."""
    predicted_wad: int
    predicted: float
    identifiable: bool
    adjustment_set: Optional[List[str]]
    confidence_wad: int

class CounterfactualRequest(BaseModel):
    """Request for counterfactual reasoning."""
    actual_world: Dict[str, float]
    intervention: Dict[str, float]
    target_variable: str

class CounterfactualResponse(BaseModel):
    """Response from counterfactual reasoning."""
    actual_outcome_wad: int
    counterfactual_outcome_wad: int
    effect_size_wad: int
    confidence_wad: int
    explanation: str
    causal_pathway: List[Dict]
    alternatives: List[str]

class GraphResponse(BaseModel):
    """Response containing the causal graph."""
    graph: Dict[str, Any]
    visualization: str

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    wad_precision: int
    wad_precision_formatted: str

# ═══════════════════════════════════════════════════════════════════════════════
# INITIALIZE THE APP
# ═══════════════════════════════════════════════════════════════════════════════

# Create the FastAPI app
app = FastAPI(
    title="Causal Insight Engine API",
    description="WAD-grounded causal reasoning for pharmaceutical applications",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the simulator
simulator = ClinicalTrialSimulator()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CausalInsightAPI")

# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Causal Insight Engine",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="operational",
        wad_precision=WAD,
        wad_precision_formatted=f"{WAD:,}"
    )

@app.post("/simulate_trial", response_model=TrialSimulationResponse)
async def simulate_trial(request: TrialSimulationRequest):
    """
    Simulate a clinical trial with given dosing regimen.
    
    Returns efficacy, safety, and survival outcomes with WAD precision.
    """
    try:
        result = simulator.simulate_trial(
            dosing=request.dosing,
            n_patients=request.n_patients
        )
        
        return TrialSimulationResponse(
            efficacy=result['efficacy'],
            safety=result['safety'],
            survival=result['survival'],
            efficacy_wad=result['efficacy_wad'],
            safety_wad=result['safety_wad'],
            survival_wad=result['survival_wad'],
            confidence=result['confidence'],
            confidence_wad=result['confidence_wad'],
            dosing=result['dosing'],
            n_patients=result['n_patients']
        )
    except Exception as e:
        logger.error(f"Error in simulate_trial: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimize_dosing", response_model=DosingOptimizationResponse)
async def optimize_dosing(request: DosingOptimizationRequest):
    """
    Find the optimal dosing regimen balancing efficacy and safety.
    """
    try:
        result = simulator.optimize_dosing(
            efficacy_weight=request.efficacy_weight,
            safety_weight=request.safety_weight,
            n_patients=request.n_patients
        )
        
        return DosingOptimizationResponse(
            optimal_dose=result['optimal_dose'],
            optimal_score_wad=result['optimal_score_wad'],
            optimal_score=result['optimal_score'],
            recommendation=result['recommendation'],
            confidence_wad=result['confidence_wad'],
            results=result['results']
        )
    except Exception as e:
        logger.error(f"Error in optimize_dosing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict", response_model=PredictionResponse)
async def predict_outcome(request: PredictionRequest):
    """
    Predict outcome under intervention.
    """
    try:
        result = simulator.predict_outcome(
            intervention=request.intervention,
            target_variable=request.target_variable
        )
        
        return PredictionResponse(
            predicted_wad=result['predicted_wad'],
            predicted=result['predicted'],
            identifiable=result['identifiable'],
            adjustment_set=list(result['adjustment_set']) if result['adjustment_set'] else None,
            confidence_wad=result['confidence_wad']
        )
    except Exception as e:
        logger.error(f"Error in predict_outcome: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/counterfactual", response_model=CounterfactualResponse)
async def counterfactual(request: CounterfactualRequest):
    """
    Answer "why" questions using counterfactual reasoning.
    """
    try:
        result = simulator.answer_why(
            actual_world=request.actual_world,
            intervention=request.intervention,
            target_variable=request.target_variable
        )
        
        return CounterfactualResponse(
            actual_outcome_wad=result['actual_outcome_wad'],
            counterfactual_outcome_wad=result['counterfactual_outcome_wad'],
            effect_size_wad=result['effect_size_wad'],
            confidence_wad=result['confidence_wad'],
            explanation=result['explanation'],
            causal_pathway=result['causal_pathway'],
            alternatives=result['alternatives']
        )
    except Exception as e:
        logger.error(f"Error in counterfactual: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/graph", response_model=GraphResponse)
async def get_graph():
    """
    Get the causal graph structure.
    """
    try:
        graph_dict = simulator.get_graph_dict()
        visualization = simulator.get_graph_visualization()
        
        return GraphResponse(
            graph=graph_dict,
            visualization=visualization
        )
    except Exception as e:
        logger.error(f"Error in get_graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/wad_info")
async def get_wad_info():
    """
    Get information about WAD arithmetic.
    """
    return {
        "precision": WAD,
        "precision_formatted": f"{WAD:,}",
        "description": "1e18 fixed-point arithmetic",
        "examples": {
            "to_wad(0.85)": to_wad(0.85),
            "from_wad(850e15)": from_wad(850_000_000_000_000_000),
            "wmul(0.85, 0.70)": {
                "input_a": to_wad(0.85),
                "input_b": to_wad(0.70),
                "result": wmul(to_wad(0.85), to_wad(0.70)),
                "result_formatted": wformat(wmul(to_wad(0.85), to_wad(0.70)))
            }
        }
    }

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Run the API server."""
    print("═" * 80)
    print("🔬 CAUSAL INSIGHT ENGINE — WAD CONSTITUTIONAL MATHEMATICS")
    print(f"📐 Precision: {WAD:,} (1e18)")
    print("═" * 80)
    print("📡 Starting API server...")
    print("📖 API docs available at http://localhost:8000/docs")
    print("📊 Graph visualization ready")
    print("✅ Server is operational")
    print("═" * 80)
    
    uvicorn.run(
        "src.causal_insight.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main()
